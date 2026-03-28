from datetime import datetime

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def parse_task_time(time_text: str) -> datetime:
    return datetime.strptime(time_text, "%I:%M %p")


def priority_label(priority_value: int) -> str:
    priority_labels = {1: "high", 2: "medium", 3: "low"}
    return priority_labels.get(priority_value, str(priority_value))

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input(
    "Available time (minutes)", min_value=1, max_value=1440, value=60
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
custom_species = ""
if species == "other":
    custom_species = st.text_input("Enter pet species", value="")
pet_age = st.number_input("Pet age", min_value=0, max_value=50, value=2)

# Streamlit reruns the script on each interaction, so session state keeps the owner alive.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time=int(available_time))
else:
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_time = int(available_time)

if st.button("Add pet"):
    pet_species = custom_species.strip() if species == "other" else species
    new_pet = Pet(name=pet_name, species=pet_species, age=int(pet_age))
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added pet: {pet_name}")

st.markdown("### Tasks")
st.caption("Add tasks to a pet. These will feed into your scheduler.")

pet_options = [pet.name for pet in st.session_state.owner.pets]

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.text_input("Task time", value="8:00 AM")
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"], index=0)
with col5:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if pet_options:
    selected_pet_name = st.selectbox("Assign task to pet", pet_options)
    priority_map = {"high": 1, "medium": 2, "low": 3}

    if st.button("Add task"):
        selected_pet = next(
            pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name
        )
        new_task = Task(
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

st.markdown("### Current Pets and Tasks")
if st.session_state.owner.pets:
    for pet in st.session_state.owner.pets:
        st.write(f"**{pet.name}** ({pet.species}, age {pet.age})")
        if pet.tasks:
            sorted_pet_tasks = sorted(
                pet.tasks,
                key=lambda task: (parse_task_time(task.time), task.priority),
            )
            for task in sorted_pet_tasks:
                st.write(
                    f"- {task.time} | {task.description} | "
                    f"{task.duration} min | {task.frequency} | priority {priority_label(task.priority)}"
                )
        else:
            st.write("- No tasks yet.")
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule from the pets and tasks stored in the backend objects.")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    schedule = scheduler.get_todays_schedule()

    if any(schedule.values()):
        st.markdown("### Today's Schedule")
        scheduled_tasks = []
        for pet_name, tasks in schedule.items():
            for task in tasks:
                scheduled_tasks.append((pet_name, task))

        scheduled_tasks.sort(
            key=lambda item: parse_task_time(item[1].time)
        )

        for pet_name, task in scheduled_tasks:
            st.write(
                f"- {task.time} | {pet_name} | {task.description} | "
                f"{task.duration} min | {task.frequency} | priority {priority_label(task.priority)}"
            )
    else:
        st.info("No tasks fit into today's schedule yet.")
