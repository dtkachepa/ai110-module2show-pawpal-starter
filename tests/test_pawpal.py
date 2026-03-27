from pawpal_system import Pet, Task


def test_mark_complete_sets_task_status_to_true() -> None:
    """Task.mark_complete should set completed to True."""
    task = Task("Feed breakfast", "8:00 AM", 10, "daily", 1)

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    """Pet.add_task should store a new task."""
    pet = Pet("Bella", "Dog", 4)
    task = Task("Evening walk", "6:00 PM", 30, "daily", 2)

    pet.add_task(task)

    assert len(pet.tasks) == 1
