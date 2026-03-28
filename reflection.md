# PawPal+ Project Reflection

## 1. System Design

Three core user actions:
The user should be able to add and manage their pet’s information, such as the pet’s name, species, age, and care preferences.
The user should be able to create and manage pet care tasks, such as feeding, walking, medication, grooming, or enrichment, including duration and priority.
The user should be able to generate and view a daily care plan based on available time, task priority, and owner preferences, with a short explanation of why certain tasks were selected.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For my initial design, I chose four main classes: Owner, Pet, Task, and Scheduler.

The Owner class is responsible for storing information about the pet owner, including their name, available time, preferences, and the pets they manage. I included this class because the scenario says the schedule should consider the owner's time and preferences.

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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
