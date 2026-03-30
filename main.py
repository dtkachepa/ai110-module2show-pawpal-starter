"""Command-line demo helpers for previewing PawPal+ schedules."""

from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def sort_tasks_by_time(
    scheduled_tasks: list[tuple[str, Task]],
) -> list[tuple[str, Task]]:
    """Return scheduled pet-task pairs ordered by due datetime."""
    return sorted(scheduled_tasks, key=lambda item: item[1].due_datetime)


def print_schedule(owner: Owner, schedule: dict[str, list[Task]]) -> None:
    """Print the scheduled tasks in chronological order for the terminal demo."""
    print("PawPal+ Today's Schedule")
    print(f"Owner: {owner.name}")
    print(f"Available Time: {owner.available_time} minutes")
    print("Selected by priority within available time, displayed by start time.")
    print()

    scheduled_tasks: list[tuple[str, Task]] = []
    for pet_name, tasks in schedule.items():
        for task in tasks:
            scheduled_tasks.append((pet_name, task))

    if not scheduled_tasks:
        print("No tasks scheduled today.")
        return

    for pet_name, task in sort_tasks_by_time(scheduled_tasks):
        print(
            f"- {task.due_datetime.strftime('%Y-%m-%d %I:%M %p')} | "
            f"{pet_name} | {task.description} | "
            f"{task.duration} min | {task.frequency} | priority {task.priority}"
        )


def print_filtered_tasks(title: str, tasks: list[Task]) -> None:
    """Print a labeled list of filtered tasks and their completion status."""
    print()
    print(title)
    if not tasks:
        print("No matching tasks found.")
        return

    for task in tasks:
        status = "Complete" if task.completed else "Incomplete"
        print(
            f"- {task.due_datetime.strftime('%Y-%m-%d %I:%M %p')} | "
            f"{task.description} | "
            f"{task.duration} min | {task.frequency} | {status}"
        )


def print_conflict_warnings(warnings: list[str]) -> None:
    """Print formatted conflict warnings for the terminal demo."""
    print()
    print("Conflict Warnings")
    if not warnings:
        print("No conflicts found.")
        return

    for warning in warnings:
        print(f"- {warning}")


def main() -> None:
    """Build sample PawPal+ data and print a demo schedule summary."""
    owner = Owner("Alex", available_time=60)

    bella = Pet("Bella", "Dog", 4)
    rocky = Pet("Rocky", "Dog", 5)
    milo = Pet("Milo", "Cat", 2)

    bella_breakfast = Task.create_task("Feed breakfast", "8:00 AM", 10, "daily", 1)
    bella_walk = Task.create_task("Evening walk", "6:00 PM", 30, "weekly", 3)
    rocky_walk = Task.create_task("Evening walk", "6:00 PM", 30, "weekly", 3)
    milo_litter = Task.create_task("Clean litter box", "12:30 PM", 15, "daily", 2)
    milo_medicine = Task.create_task("Give medicine", "12:30 PM", 5, "daily", 1)

    bella.add_task(bella_breakfast)
    bella.add_task(bella_walk)
    rocky.add_task(rocky_walk)
    milo.add_task(milo_litter)
    milo.add_task(milo_medicine)

    owner.add_pet(bella)
    owner.add_pet(rocky)
    owner.add_pet(milo)

    bella.complete_task(bella_breakfast)

    scheduler = Scheduler(owner)
    schedule = scheduler.get_todays_schedule()
    conflict_warnings = scheduler.get_conflict_warnings(schedule)
    bella_complete_tasks = scheduler.filter_tasks_by_pet_name(
        "Bella"
    )

    # bella_complete_tasks = scheduler.filter_tasks_by_pet_name(
    #     "Bella", completed=True
    # )

    print_schedule(owner, schedule)
    print_conflict_warnings(conflict_warnings)
    print_filtered_tasks(
        "Filtered Tasks: Bella", bella_complete_tasks
    )


if __name__ == "__main__":
    main()
