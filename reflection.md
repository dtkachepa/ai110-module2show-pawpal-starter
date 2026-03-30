# PawPal+ Project Reflection

## 1. System Design

Three core user actions:
The user should be able to add and manage their pet's information, such as the pet's name, species, and age.
The user should be able to create and manage pet care tasks, such as feeding, walking, medication, grooming, or enrichment, including duration and priority.
The user should be able to generate and view a daily care plan based on available time and task priority, with a short explanation of why certain tasks were selected.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For my initial design, I chose four main classes: Owner, Pet, Task, and Scheduler.

The Owner class is responsible for storing information about the pet owner, including their name, available time, and the pets they manage. I included this class because the scenario says the schedule should consider the owner's time.

The Pet class is responsible for storing information about the pet, such as its name, species, age, and care tasks. This class acts as the main container for the tasks related to a specific pet.

The Task class represents an individual pet care activity, such as feeding, walking, medication, grooming, or enrichment. It stores important scheduling information like duration, priority, completion status, and optional notes.

The Scheduler class is responsible for generating a daily plan. It uses the owner's available time and the pet's task list to decide which tasks should be included in the final daily schedule. I also gave it an explanation method so the system can describe why certain tasks were chosen.

**b. Design changes**

- Did your design change during implementation?
No, it hasn't changed yet.
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time and priority)?
- How did you decide which constraints mattered most?

My scheduler mainly considers three things: whether a task is incomplete, whether it is due today or overdue, and how important it is based on priority and the owner's available time. In `get_todays_schedule()`, the system first filters out completed tasks and future tasks, then sorts the remaining tasks by priority, and finally keeps only the tasks that fit inside the time budget. I decided these constraints mattered most because they matched the real goal of the app: helping a busy pet owner focus on what still needs attention today without overloading the plan.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff in my scheduler is that when a recurring task is completed, the system creates a new task instance for the next occurrence instead of updating the same task repeatedly. I chose this because it makes each completed task easy to track and keeps the recurrence logic simple. The downside is that the task list can grow over time, since old completed tasks remain in memory. A more advanced version might store recurrence separately from task history, but that would be harder to build and explain in this project.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

The most effective AI features for this project were codebase-aware debugging, quick refactoring help, and back-and-forth design iteration. AI was especially useful when I needed to compare the backend and frontend, clean up unused code, and make sure the UI actually surfaced the smarter scheduling logic in a readable way.
The best prompts were the ones that were specific, structured and grounded in the code. Also specifying what I wanted from the AI, whether a plan or diff etc.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

AI was adding too much information in the frontend detail, making the app feel crowded and less intentional. I chose to keep the main page focused on the core actions.
I evaluated that decision by comparing it to the actual user flow in the app: add pet, add task, generate schedule, then mark tasks complete.This is one example I can easily explain.

Also, using separate chat sessions for different phases also helped a lot. It kept brainstorming, implementation, UI polishing, and reflection work from getting mixed together. That made it easier to stay focused and also made it easier to spot when an older idea no longer matched the final codebase.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested the most important backend behaviors: marking a task complete, adding tasks to a pet, returning one pet's tasks in chronological order, building today's schedule from incomplete tasks that are due today or overdue, creating the next recurring daily task, detecting schedule conflicts, and allowing valid shared same-species walk or feed tasks without warning. These tests mattered because they covered the core logic that makes PawPal+ more than just a task list. If those behaviors were wrong, the schedule would be incorrect and error prone.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I feel fairly confident in the scheduler because the main logic paths are tested and the UI now uses the backend methods directly instead of duplicating too much logic in the frontend. I would still want more edge-case coverage if I had more time. The next cases I would test are invalid time input from the UI, recurring weekly tasks across longer time gaps, tasks with the same priority competing for limited available time, and what happens after multiple completions over several days as the recurring task list grows.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with how the backend and frontend ended up matching each other. By the end of the project, the UI was no longer just a thin demo layer. It actually exposed the useful parts of the system, like schedule generation, conflict warnings, recurring task completion, and filtered task browsing, without becoming too cluttered.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, the first thing I would improve is conflict handling. Right now, the scheduler can detect a clash and notify the user, but it does not actually resolve the overlap or change the final plan. A better solution would be to add a clear conflict-resolution rule during scheduling, such as keeping the higher-priority task and excluding the lower-priority one. That would make the schedule more actionable instead of only informative.

I would also improve input validation and make scheduling date-aware instead of only supporting today's schedule. I would consider a cleaner way to manage recurring task history over time, because the current design keeps completed tasks and adds new future tasks, which is simple but can make the task list grow.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

My biggest takeaway is that even with strong AI tools, I still had to act as the lead architect. The AI could generate options quickly, but it did not automatically know which tradeoffs fit the project best. I had to decide what belonged in the backend, what should stay out of the UI, when a feature was becoming overengineered, and when to simplify the design. I learned that good AI collaboration is less about accepting fast answers and more about giving direction, checking alignment, and making the final system coherent. Essentially the driver-navigator framework which is taught at Codepath.
