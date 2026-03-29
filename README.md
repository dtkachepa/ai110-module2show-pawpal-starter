# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ now includes a few simple scheduling improvements:

- Tasks can be displayed in time order for a clearer daily plan.
- Tasks can be filtered by pet name or by completion status.
- Daily and weekly recurring tasks create the next task instance when completed.
- The scheduler can generate conflict warnings when multiple tasks are scheduled at the same exact time.

The conflict checker also allows a small shared-task exception for 2 to 5 pets of the same species, such as walking or feeding multiple dogs at the same time.

## Testing PawPal+

Run the current test suite with:

```bash
.\.venv\Scripts\python.exe -m pytest tests\test_pawpal.py
```

The tests currently cover core backend behaviors: marking tasks complete, adding tasks to pets, returning tasks in chronological order, building a daily schedule from overdue and due-today incomplete tasks, creating the next daily recurring task, detecting scheduling conflicts, and allowing valid shared walk/feed tasks for pets of the same species.

Current reliability confidence: `★★★★☆` (4/5). The main scheduling rules are covered, but the project still has a small student-project test surface and could use more edge-case coverage over time.
