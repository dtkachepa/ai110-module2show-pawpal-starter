import pandas as pd
import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def priority_label(priority_value: int) -> str:
    priority_labels = {1: "high", 2: "medium", 3: "low"}
    return priority_labels.get(priority_value, str(priority_value))


def task_rows(
    tasks: list[tuple[str, Task]], include_pet: bool = False
) -> list[dict[str, str | int]]:
    return [
        {
            **({"Pet": pet_name} if include_pet else {}),
            "Due Datetime": task.due_datetime.strftime("%Y-%m-%d %I:%M %p"),
            "Task": task.description,
            "Duration (min)": task.duration,
            "Frequency": task.frequency,
            "Priority": priority_label(task.priority),
            "Status": "complete" if task.completed else "pending",
        }
        for pet_name, task in tasks
    ]


def build_schedule(owner: Owner) -> tuple[dict[str, list[Task]], list[str]]:
    scheduler = Scheduler(owner)
    schedule = scheduler.get_todays_schedule()
    warnings = scheduler.get_conflict_warnings(schedule)
    return schedule, warnings


def scheduled_task_rows(schedule: dict[str, list[Task]]) -> list[dict[str, str | int]]:
    scheduled_tasks: list[tuple[str, Task]] = []
    for pet_name, tasks in schedule.items():
        for task in tasks:
            scheduled_tasks.append((pet_name, task))

    scheduled_tasks.sort(key=lambda item: item[1].due_datetime)
    return [
        {
            "Time": task.due_datetime.strftime("%I:%M %p"),
            "Pet": pet_name,
            "Task": task.description,
            "Duration (min)": task.duration,
            "Frequency": task.frequency,
            "Priority": priority_label(task.priority),
        }
        for pet_name, task in scheduled_tasks
    ]

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
    }
    [data-testid="stSidebar"] {
        min-width: 35vw;
        width: 35vw;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.subheader("Owner and Pet Details")
owner_name = st.text_input("Owner name", value="", placeholder="e.g. Jordan")
available_time = st.number_input(
    "Available time (minutes)", min_value=0, max_value=1440, value=0
)
pet_name = st.text_input("Pet name", value="", placeholder="e.g. Mochi")
species = st.selectbox("Species", ["Select species...", "dog", "cat", "other"], index=0)
custom_species = ""
if species == "other":
    custom_species = st.text_input(
        "Enter pet species", value="", placeholder="e.g. rabbit"
    )
pet_age = st.number_input("Pet age", min_value=0, max_value=50, value=0)

# Streamlit reruns the script on each interaction, so session state keeps the owner alive.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time=int(available_time))
else:
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_time = int(available_time)

if "last_schedule" not in st.session_state:
    st.session_state.last_schedule = None
if "last_conflicts" not in st.session_state:
    st.session_state.last_conflicts = []

if st.button("Add pet"):
    if not owner_name.strip():
        st.warning("Enter the owner's name before adding a pet.")
    elif not pet_name.strip():
        st.warning("Enter a pet name before adding a pet.")
    elif species == "Select species...":
        st.warning("Select a species before adding a pet.")
    elif species == "other" and not custom_species.strip():
        st.warning("Enter the pet species before adding a pet.")
    else:
        pet_species = custom_species.strip() if species == "other" else species
        new_pet = Pet(name=pet_name, species=pet_species, age=int(pet_age))
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added pet: {pet_name}")

st.divider()

st.markdown("### Tasks")
st.caption("Add tasks to a pet. These will feed into your scheduler.")

pet_options = [pet.name for pet in st.session_state.owner.pets]

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="", placeholder="e.g. Morning walk")
with col2:
    task_time = st.text_input("Task time", value="", placeholder="e.g. 8:00 AM")
with col3:
    duration = st.number_input("Duration (minutes)", min_value=0, max_value=240, value=0)
with col4:
    frequency = st.selectbox(
        "Frequency", ["Select frequency...", "daily", "weekly"], index=0
    )
with col5:
    priority = st.selectbox(
        "Priority", ["Select priority...", "low", "medium", "high"], index=0
    )

if pet_options:
    selected_pet_name = st.selectbox("Assign task to pet", pet_options)
    priority_map = {"high": 1, "medium": 2, "low": 3}

    if st.button("Add task"):
        if not task_title.strip():
            st.warning("Enter a task title before adding a task.")
        elif not task_time.strip():
            st.warning("Enter a task time before adding a task.")
        elif frequency == "Select frequency...":
            st.warning("Select a frequency before adding a task.")
        elif priority == "Select priority...":
            st.warning("Select a priority before adding a task.")
        else:
            selected_pet = next(
                pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name
            )
            new_task = Task.create_task(
                description=task_title,
                time=task_time,
                duration=int(duration),
                frequency=frequency,
                priority=priority_map[priority],
            )
            selected_pet.add_task(new_task)
            st.success(f"Added task to {selected_pet_name}: {task_title}")
else:
    st.info("Add a pet before creating tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule from the pets and tasks stored in the backend objects.")

if st.button("Generate schedule"):
    schedule, warnings = build_schedule(st.session_state.owner)
    st.session_state.last_schedule = schedule
    st.session_state.last_conflicts = warnings

if st.session_state.last_schedule is not None:
    schedule = st.session_state.last_schedule
    conflict_warnings = st.session_state.last_conflicts
    if any(schedule.values()):
        st.success("Schedule generated.")
        st.markdown("### Today's Schedule")
        st.table(scheduled_task_rows(schedule))

        if conflict_warnings:
            for warning in conflict_warnings:
                st.warning(warning)
        else:
            st.success("No task conflicts detected.")
    else:
        st.info("No tasks fit into today's schedule yet.")

st.divider()

st.subheader("Mark Task Complete")
if st.session_state.last_schedule is not None and pet_options:
    scheduler = Scheduler(st.session_state.owner)
    completion_pet_name = st.selectbox("Pet for task completion", pet_options)
    pending_tasks = scheduler.filter_tasks_by_pet_name(
        completion_pet_name, completed=False
    )

    if pending_tasks:
        pending_task_labels = [
            f"{task.due_datetime.strftime('%I:%M %p')} | {task.description}"
            for task in pending_tasks
        ]
        selected_task_label = st.selectbox("Pending task", pending_task_labels)

        if st.button("Mark complete"):
            selected_index = pending_task_labels.index(selected_task_label)
            selected_task = pending_tasks[selected_index]
            selected_pet = next(
                pet
                for pet in st.session_state.owner.pets
                if pet.name == completion_pet_name
            )
            is_recurring = selected_task.frequency in {"daily", "weekly"}
            selected_pet.complete_task(selected_task)
            refreshed_schedule, refreshed_warnings = build_schedule(st.session_state.owner)
            st.session_state.last_schedule = refreshed_schedule
            st.session_state.last_conflicts = refreshed_warnings
            if is_recurring:
                st.success(
                    f"Marked '{selected_task.description}' complete for {completion_pet_name}. "
                    f"The next {selected_task.frequency} task was created and today's schedule was refreshed."
                )
            else:
                st.success(
                    f"Marked '{selected_task.description}' complete for {completion_pet_name} and refreshed today's schedule."
                )
    else:
        st.info("No pending tasks for this pet.")
elif st.session_state.last_schedule is None:
    st.info("Generate a schedule before marking tasks complete.")

with st.sidebar:
    st.subheader("Tasks")

    scheduler = Scheduler(st.session_state.owner)
    pet_filter_options = ["all"] + pet_options
    selected_pet_filter = st.selectbox("Pet", pet_filter_options)
    selected_status_filter = st.selectbox("Status", ["all", "pending", "complete"])
    selected_frequency_filter = st.selectbox("Frequency", ["all", "daily", "weekly"])

    filtered_tasks: list[tuple[str, Task]] = []
    pets_to_show = (
        st.session_state.owner.pets
        if selected_pet_filter == "all"
        else [
            pet for pet in st.session_state.owner.pets if pet.name == selected_pet_filter
        ]
    )

    for pet in pets_to_show:
        pet_tasks = scheduler.filter_tasks_by_pet_name(pet.name)
        if selected_status_filter != "all":
            is_completed = selected_status_filter == "complete"
            pet_tasks = [task for task in pet_tasks if task.completed == is_completed]
        if selected_frequency_filter != "all":
            pet_tasks = [
                task for task in pet_tasks if task.frequency == selected_frequency_filter
            ]
        for task in pet_tasks:
            filtered_tasks.append((pet.name, task))

    if filtered_tasks:
        st.dataframe(
            pd.DataFrame(task_rows(filtered_tasks, include_pet=True)),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("No tasks match the selected filters.")
