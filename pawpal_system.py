from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time: str
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

    def get_todays_schedule(self) -> dict[str, List[Task]]:
        """Build today's schedule for each pet."""
        schedule: dict[str, List[Task]] = {}
        for pet in self.owner.pets:
            incomplete_tasks = [task for task in pet.get_tasks() if not task.completed]
            sorted_tasks = self.sort_tasks_by_priority(incomplete_tasks)
            schedule[pet.name] = self.filter_tasks_by_available_time(
                sorted_tasks, self.owner.available_time
            )
        return schedule
