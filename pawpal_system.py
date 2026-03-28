from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time: str
    due_date: date
    duration: int
    frequency: str
    priority: int
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def update_priority(self, priority: int) -> None:
        """Update the task priority."""
        self.priority = priority

    def create_next_recurring_task(self) -> Task | None:
        """Create the next task instance for daily or weekly recurring tasks."""
        if self.frequency == "daily":
            next_due_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            time=self.time,
            due_date=next_due_date,
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
        """Add a task to the pet."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return the pet's tasks."""
        return self.tasks

    def complete_task(self, task: Task) -> None:
        """Complete a task and add the next recurring task if needed."""
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
        """Add a pet to the owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> dict[str, List[Task]]:
        """Return all tasks grouped by pet name."""
        all_tasks: dict[str, List[Task]] = {}
        for pet in self.pets:
            all_tasks[pet.name] = pet.get_tasks()
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Store the owner used for scheduling."""
        self.owner = owner

    def filter_tasks_by_completion(
        self, tasks: List[Task], completed: bool
    ) -> List[Task]:
        """Return tasks that match the requested completion status."""
        return [task for task in tasks if task.completed == completed]

    def filter_tasks_by_pet_name(
        self, pet_name: str, completed: bool | None = None
    ) -> List[Task]:
        """Return tasks for one pet, with optional completion filtering."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                tasks = pet.get_tasks()
                if completed is None:
                    return tasks
                return self.filter_tasks_by_completion(tasks, completed)
        return []

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority."""
        return sorted(tasks, key=lambda task: task.priority)

    def filter_tasks_by_available_time(
        self, tasks: List[Task], available_time: int
    ) -> List[Task]:
        """Keep tasks that fit within the available time."""
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
        """Allow simple shared tasks for 2 to 5 pets of the same species."""
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
        """Return readable warnings for tasks scheduled at the same time."""
        tasks_by_time: dict[str, List[tuple[Pet, Task]]] = defaultdict(list)

        for pet in self.owner.pets:
            for task in schedule.get(pet.name, []):
                tasks_by_time[task.time].append((pet, task))

        warnings: List[str] = []
        for time, scheduled_items in tasks_by_time.items():
            if len(scheduled_items) <= 1:
                continue

            if self._is_shared_species_task(scheduled_items):
                continue

            conflict_details = ", ".join(
                f"{pet.name} - {task.description}" for pet, task in scheduled_items
            )
            warnings.append(f"Conflict at {time}: {conflict_details}")

        return warnings

    def get_todays_schedule(self) -> dict[str, List[Task]]:
        """Build today's schedule for each pet."""
        schedule: dict[str, List[Task]] = {}
        today = date.today()
        for pet in self.owner.pets:
            incomplete_tasks = [
                task
                for task in pet.get_tasks()
                if not task.completed and task.due_date <= today
            ]
            sorted_tasks = self.sort_tasks_by_priority(incomplete_tasks)
            schedule[pet.name] = self.filter_tasks_by_available_time(
                sorted_tasks, self.owner.available_time
            )
        return schedule
