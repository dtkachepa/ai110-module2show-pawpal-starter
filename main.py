from datetime import date, datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def sort_tasks_by_time(
    scheduled_tasks: list[tuple[str, Task]],
) -> list[tuple[str, Task]]:
    """Sort scheduled tasks by their start time."""
    return sorted(
        scheduled_tasks,
        key=lambda item: datetime.strptime(item[1].time, "%I:%M %p"),
    )


def print_schedule(owner: Owner, schedule: dict[str, list[Task]]) -> None:
    """Print a readable daily schedule to the terminal."""
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
            f"- {task.due_date} {task.time} | {pet_name} | {task.description} | "
            f"{task.duration} min | {task.frequency} | priority {task.priority}"
        )


def print_filtered_tasks(title: str, tasks: list[Task]) -> None:
    """Print a readable list of filtered tasks."""
    print()
    print(title)
    if not tasks:
        print("No matching tasks found.")
        return

    for task in tasks:
        status = "Complete" if task.completed else "Incomplete"
        print(
            f"- {task.due_date} {task.time} | {task.description} | "
            f"{task.duration} min | {task.frequency} | {status}"
        )


def print_conflict_warnings(warnings: list[str]) -> None:
    """Print any scheduling conflict warnings."""
    print()
    print("Conflict Warnings")
    if not warnings:
        print("No conflicts found.")
        return

    for warning in warnings:
        print(f"- {warning}")


def main() -> None:
    """Create sample data and print today's schedule."""
    owner = Owner("Alex", available_time=60, preferences=["short tasks first"])

    bella = Pet("Bella", "Dog", 4)
    rocky = Pet("Rocky", "Dog", 5)
    milo = Pet("Milo", "Cat", 2)
    today = date.today()

    bella_breakfast = Task("Feed breakfast", "8:00 AM", today, 10, "daily", 1)
    bella_walk = Task("Evening walk", "6:00 PM", today, 30, "weekly", 3)
    rocky_walk = Task("Evening walk", "6:00 PM", today, 30, "weekly", 3)
    milo_litter = Task("Clean litter box", "12:30 PM", today, 15, "daily", 2)
    milo_medicine = Task("Give medicine", "12:30 PM", today, 5, "daily", 1)

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
        "Bella", completed=True
    )

    print_schedule(owner, schedule)
    print_conflict_warnings(conflict_warnings)
    print_filtered_tasks(
        "Filtered Tasks: Bella (Complete Only)", bella_complete_tasks
    )


if __name__ == "__main__":
    main()
