"""Pytest coverage for the main PawPal+ backend behaviors."""

from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_sets_task_status_to_true() -> None:
    """Task.mark_complete should flip the completion flag to True."""
    task = Task(
        "Feed breakfast",
        "8:00 AM",
        datetime(2026, 3, 29, 8, 0),
        10,
        "daily",
        1,
    )

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    """Pet.add_task should store the exact task instance on the pet."""
    pet = Pet("Bella", "Dog", 4)
    task = Task(
        "Evening walk",
        "6:00 PM",
        datetime(2026, 3, 29, 18, 0),
        30,
        "daily",
        2,
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task


def test_filter_tasks_by_pet_name_returns_tasks_in_chronological_order() -> None:
    """Filtering one pet's tasks should return them ordered by due datetime."""
    owner = Owner("Alex", available_time=60)
    pet = Pet("Bella", "Dog", 4)
    owner.add_pet(pet)

    evening = Task(
        "Evening walk",
        "6:00 PM",
        datetime(2026, 3, 29, 18, 0),
        30,
        "daily",
        2,
    )
    morning = Task(
        "Feed breakfast",
        "8:00 AM",
        datetime(2026, 3, 29, 8, 0),
        10,
        "daily",
        1,
    )
    noon = Task(
        "Give medicine",
        "12:30 PM",
        datetime(2026, 3, 29, 12, 30),
        5,
        "daily",
        1,
    )

    pet.add_task(evening)
    pet.add_task(morning)
    pet.add_task(noon)

    scheduler = Scheduler(owner)
    tasks = scheduler.filter_tasks_by_pet_name("Bella")

    assert [task.description for task in tasks] == [
        "Feed breakfast",
        "Give medicine",
        "Evening walk",
    ]


def test_get_todays_schedule_includes_incomplete_tasks_due_today_or_earlier_within_available_time() -> None:
    """Today's schedule should include overdue and due-today tasks that fit the time budget."""
    owner = Owner("Alex", available_time=30)
    pet = Pet("Bella", "Dog", 4)
    owner.add_pet(pet)

    now = datetime.now()
    overdue_high = Task(
        "Give medicine",
        "7:00 AM",
        now - timedelta(days=1),
        5,
        "daily",
        1,
    )
    today_medium = Task(
        "Feed breakfast",
        "8:00 AM",
        now.replace(hour=8, minute=0, second=0, microsecond=0),
        10,
        "daily",
        2,
    )
    today_low = Task(
        "Brush fur",
        "6:00 PM",
        now.replace(hour=18, minute=0, second=0, microsecond=0),
        20,
        "daily",
        3,
    )
    future_task = Task(
        "Vet visit",
        "9:00 AM",
        now + timedelta(days=1),
        15,
        "weekly",
        1,
    )
    completed_task = Task(
        "Clean bowl",
        "9:00 AM",
        now.replace(hour=9, minute=0, second=0, microsecond=0),
        5,
        "daily",
        1,
        completed=True,
    )

    pet.add_task(overdue_high)
    pet.add_task(today_medium)
    pet.add_task(today_low)
    pet.add_task(future_task)
    pet.add_task(completed_task)

    scheduler = Scheduler(owner)
    schedule = scheduler.get_todays_schedule()

    assert [task.description for task in schedule["Bella"]] == [
        "Give medicine",
        "Feed breakfast",
    ]


def test_complete_task_creates_next_daily_task_for_following_day() -> None:
    """Completing a daily task should add the next day's recurring task."""
    pet = Pet("Bella", "Dog", 4)
    original_task = Task(
        "Feed breakfast",
        "8:00 AM",
        datetime(2026, 3, 29, 8, 0),
        10,
        "daily",
        1,
    )
    pet.add_task(original_task)

    pet.complete_task(original_task)

    assert original_task.completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1].description == "Feed breakfast"
    assert pet.tasks[1].due_datetime == datetime(2026, 3, 30, 8, 0)


def test_get_conflict_warnings_flags_duplicate_times() -> None:
    """Same-datetime tasks for different pets should produce one conflict warning."""
    owner = Owner("Alex", available_time=60)
    bella = Pet("Bella", "Dog", 4)
    milo = Pet("Milo", "Cat", 2)
    owner.add_pet(bella)
    owner.add_pet(milo)

    shared_time = datetime(2026, 3, 29, 12, 30)
    bella_task = Task("Give medicine", "12:30 PM", shared_time, 5, "daily", 1)
    milo_task = Task("Clean litter box", "12:30 PM", shared_time, 15, "daily", 2)

    schedule = {
        "Bella": [bella_task],
        "Milo": [milo_task],
    }

    scheduler = Scheduler(owner)
    warnings = scheduler.get_conflict_warnings(schedule)

    assert len(warnings) == 1
    assert "Conflict at 2026-03-29 12:30 PM" in warnings[0]
    assert "Bella - Give medicine" in warnings[0]
    assert "Milo - Clean litter box" in warnings[0]


def test_get_conflict_warnings_skips_valid_shared_species_walk_or_feed_tasks() -> None:
    """Matching shared walk or feed tasks for one species should not warn."""
    owner = Owner("Alex", available_time=60)
    bella = Pet("Bella", "Dog", 4)
    rocky = Pet("Rocky", "Dog", 5)
    owner.add_pet(bella)
    owner.add_pet(rocky)

    shared_time = datetime(2026, 3, 29, 18, 0)
    bella_task = Task("Evening walk", "6:00 PM", shared_time, 30, "weekly", 3)
    rocky_task = Task("Evening walk", "6:00 PM", shared_time, 30, "weekly", 3)

    schedule = {
        "Bella": [bella_task],
        "Rocky": [rocky_task],
    }

    scheduler = Scheduler(owner)
    warnings = scheduler.get_conflict_warnings(schedule)

    assert warnings == []
