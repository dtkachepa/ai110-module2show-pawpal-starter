"""Core backend models and scheduling logic for PawPal+."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time: str
    due_datetime: datetime
    duration: int
    frequency: str
    priority: int
    completed: bool = False

    def mark_complete(self) -> None:
        """Set the task's completion flag to True."""
        self.completed = True

    def update_priority(self, priority: int) -> None:
        """Replace the task's current priority value."""
        self.priority = priority

    @classmethod
    def create_task(
        cls,
        description: str,
        time: str,
        duration: int,
        frequency: str,
        priority: int,
    ) -> Task:
        """Create a task whose first due datetime is not in the past."""
        due_datetime = cls.get_initial_due_datetime(time, frequency)
        return cls(description, time, due_datetime, duration, frequency, priority)

    @staticmethod
    def get_initial_due_datetime(time: str, frequency: str) -> datetime:
        """Return the first valid due datetime based on now and frequency."""
        now = datetime.now()
        task_time = datetime.strptime(time, "%I:%M %p").time()
        due_datetime = datetime.combine(now.date(), task_time)

        if due_datetime >= now:
            return due_datetime

        if frequency == "weekly":
            return due_datetime + timedelta(days=7)

        return due_datetime + timedelta(days=1)

    def create_next_recurring_task(self) -> Task | None:
        """Return the next daily or weekly task instance, if applicable."""
        if self.frequency == "daily":
            next_due_datetime = self.due_datetime + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due_datetime = self.due_datetime + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            time=self.time,
            due_datetime=next_due_datetime,
            duration=self.duration,
            frequency=self.frequency,
            priority=self.priority,
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a new care task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's current task list."""
        return self.tasks

    def complete_task(self, task: Task) -> None:
        """Mark a task complete and add its next recurring instance when needed."""
        if task.completed:
            return

        task.mark_complete()
        next_task = task.create_next_recurring_task()
        if next_task is not None:
            self.add_task(next_task)


class Owner:
    def __init__(
        self,
        name: str,
        available_time: int,
        preferences: List[str] | None = None,
        pets: List[Pet] | None = None,
    ) -> None:
        self.name = name
        self.available_time = available_time
        self.preferences = preferences if preferences is not None else []
        self.pets = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        self.pets.append(pet)

    def get_all_tasks(self) -> dict[str, List[Task]]:
        """Return every pet's tasks grouped by pet name."""
        all_tasks: dict[str, List[Task]] = {}
        for pet in self.pets:
            all_tasks[pet.name] = pet.get_tasks()
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Store the owner whose pets and tasks will be scheduled."""
        self.owner = owner

    def filter_tasks_by_completion(
        self, tasks: List[Task], completed: bool
    ) -> List[Task]:
        """Return only tasks whose completed state matches the request."""
        return [task for task in tasks if task.completed == completed]

    def filter_tasks_by_pet_name(
        self, pet_name: str, completed: bool | None = None
    ) -> List[Task]:
        """Return one pet's tasks sorted by due time, with optional status filtering."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                tasks = pet.get_tasks()
                if completed is not None:
                    tasks = self.filter_tasks_by_completion(tasks, completed)
                    return sorted(tasks, key=lambda task: task.due_datetime)
                return sorted(tasks, key=lambda task: (task.completed, task.due_datetime))
        return []

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered from highest to lowest priority value."""
        return sorted(tasks, key=lambda task: task.priority)

    def filter_tasks_by_available_time(
        self, tasks: List[Task], available_time: int
    ) -> List[Task]:
        """Keep tasks in order until the owner's time budget is filled."""
        selected_tasks: List[Task] = []
        used_time = 0
        for task in tasks:
            if used_time + task.duration <= available_time:
                selected_tasks.append(task)
                used_time += task.duration
        return selected_tasks

    def _is_shared_species_task(
        self, scheduled_items: List[tuple[Pet, Task]]
    ) -> bool:
        """Allow matching walk or feed tasks shared by 2 to 5 pets of one species."""
        if len(scheduled_items) < 2 or len(scheduled_items) > 5:
            return False

        species = {pet.species.lower() for pet, _ in scheduled_items}
        descriptions = {task.description.lower() for _, task in scheduled_items}

        if len(species) != 1 or len(descriptions) != 1:
            return False

        shared_keywords = ("walk", "feed")
        description = scheduled_items[0][1].description.lower()
        return any(keyword in description for keyword in shared_keywords)

    def get_conflict_warnings(
        self, schedule: dict[str, List[Task]]
    ) -> List[str]:
        """Return readable warnings for same-datetime tasks that conflict."""
        tasks_by_time: dict[datetime, List[tuple[Pet, Task]]] = defaultdict(list)

        for pet in self.owner.pets:
            for task in schedule.get(pet.name, []):
                tasks_by_time[task.due_datetime].append((pet, task))

        warnings: List[str] = []
        for due_datetime, scheduled_items in tasks_by_time.items():
            if len(scheduled_items) <= 1:
                continue

            if self._is_shared_species_task(scheduled_items):
                continue

            conflict_details = ", ".join(
                f"{pet.name} - {task.description}" for pet, task in scheduled_items
            )
            display_time = due_datetime.strftime("%Y-%m-%d %I:%M %p")
            warnings.append(f"Conflict at {display_time}: {conflict_details}")

        return warnings

    def get_todays_schedule(self) -> dict[str, List[Task]]:
        """Build today's plan using incomplete tasks due today or earlier."""
        schedule: dict[str, List[Task]] = {}
        now = datetime.now()
        for pet in self.owner.pets:
            incomplete_tasks = [
                task
                for task in pet.get_tasks()
                if not task.completed and task.due_datetime.date() <= now.date()
            ]
            sorted_tasks = self.sort_tasks_by_priority(incomplete_tasks)
            schedule[pet.name] = self.filter_tasks_by_available_time(
                sorted_tasks, self.owner.available_time
            )
        return schedule
