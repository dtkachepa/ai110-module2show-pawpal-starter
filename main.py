from datetime import datetime

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
            f"- {task.time} | {pet_name} | {task.description} | "
            f"{task.duration} min | {task.frequency} | priority {task.priority}"
        )


def main() -> None:
    """Create sample data and print today's schedule."""
    owner = Owner("Alex", available_time=60, preferences=["short tasks first"])

    bella = Pet("Bella", "Dog", 4)
    milo = Pet("Milo", "Cat", 2)

    bella.add_task(Task("Feed breakfast", "8:00 AM", 10, "daily", 1))
    bella.add_task(Task("Evening walk", "6:00 PM", 30, "daily", 3))
    milo.add_task(Task("Clean litter box", "12:30 PM", 15, "daily", 2))

    owner.add_pet(bella)
    owner.add_pet(milo)

    scheduler = Scheduler(owner)
    schedule = scheduler.get_todays_schedule()

    print_schedule(owner, schedule)


if __name__ == "__main__":
    main()
