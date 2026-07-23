# Alarm Clock CLI – Requirements

## Overview

Build a minimal Alarm Clock as a Python CLI application.

This is intentionally scoped as a **20-minute implementation exercise**. The focus is on demonstrating engineering judgment, clean structure, and handling common edge cases—not building a production-ready scheduler.

---

# Goals

Implement a simple command-line alarm clock that allows a user to:

- View existing alarms
- Add a new alarm
- Update an existing alarm
- Delete an alarm
- Wait efficiently until the next alarm rings
- hsoudl create async tasks, or spaun tasks in background wich will run right after adding

The application should not require a database or continuously poll in a loop.

---

# Technology Constraints

- Python **3.13**
- CLI only
- No GUI
- No web server
- No React
- No database
- Store alarm data in a local JSON file

---

# Functional Requirements

## 1. Application Startup

When the application starts it should display:

```
==========================
      Alarm Clock
    Time Format: 24 Hour
==========================

1. View Alarms
2. Add Alarm
3. Update Alarm
4. Delete Alarm
5. Exit
```

The application should clearly indicate that **24-hour time format** is used.

---

## 2. View Alarms

Display all saved alarms.

Example:

```
ID   Time
1    07:30
2    18:45
3    22:00
```

If no alarms exist:

```
No alarms configured.
```

---

## 3. Add Alarm

Allow the user to enter:

```
HH:MM
```

Example

```
Enter alarm time (24-hour): 18:45
```

Validation:

- Must be valid 24-hour format
- Save to JSON
- Confirmation message
- creats task , in background, store task id to delte or update later

```
Alarm added.
```

---

## 4. Update Alarm

Allow the user to:

- Select alarm by ID
- Enter new time
- kills runing task and recreats for update time

Example

```
Select alarm: 2
New time: 19:00
```

Persist changes to JSON.

---

## 5. Delete Alarm

Allow user to delete an alarm by ID.

Example

```
Select alarm to delete: 1
delets background task

Alarm deleted.
```

Persist changes immediately.

---

# Alarm Storage

Use a local JSON file.

Example:

```json
[
    {
        "id": 1,
        "time": "07:30",
        "task_id": 001,
    },
    {
        "id": 2,
        "time": "18:45",
        "task_id": 002,
    }
]
```

The JSON file acts as the application's persistent storage.

---

# Sound

Use:

```
playsound
```

(or another lightweight cross-platform audio library if preferred.)

Requirements:

- Play a bundled sound file
- Ring for approximately **10 seconds**
- After 10 seconds, stop playback (or allow the sound to finish if it is exactly 10 seconds long)

---

# Non-Functional Requirements

- Simple CLI interface
- Minimal dependencies
- Readable code
- Small project structure
- JSON persistence
- Fast startup
- Suitable for completion in approximately 20 minutes

---

# Edge Cases

## Invalid Time Format

Examples:

```
25:00
12:60
abc
7pm
18-30
```

Expected:

```
Invalid time.
Use HH:MM (24-hour).
```

---

## Past Time

Current time:

```
18:00
```

Alarm:

```
17:30
```

Expected:

Schedule alarm for **tomorrow**.

---

## Multiple Alarms

Example:

```
08:00
07:30
09:15
```

Expected:

Scheduler chooses the earliest upcoming alarm.

---

## Duplicate Times

Two alarms may exist with identical times.

This is allowed.

---

## Empty Alarm List

Starting the scheduler with no alarms should display:

```
No alarms configured.
```

---

## Invalid Alarm ID

Updating or deleting a non-existent ID should show:

```
Alarm not found.
```

---

## Corrupted JSON File

If the JSON file cannot be parsed:

- Show an error
- Exit gracefully

---

## Missing JSON File

If the storage file does not exist:

- Create an empty alarm list automatically

---

# Assumptions

- Only one user uses the application.
- Alarm times repeat daily.
- Only one alarm is triggered per scheduler run.
- The user manually starts the scheduler when needed.
- Alarm persistence is limited to a local JSON file.

---

# Out of Scope (Non-Goals)

The following are intentionally excluded to prevent scope creep:

- Multiple recurring schedules
- Weekly alarms
- Custom labels
- Snooze functionality
- Enable/disable alarms
- Time zones
- Daylight Saving Time handling
- Notifications
- Background service or daemon
- Running automatically on system startup
- GUI
- Web interface
- Database
- User authentication
- Logging framework
- Configuration files
- Import/export
- Alarm history
- Multiple concurrent alarm processes
- Cross-device synchronization

---

# Risks

- Audio playback behavior may differ across operating systems.
- The system clock changing while the application is sleeping may affect trigger timing.
- If the application is terminated during sleep, the scheduled alarm will not ring.

---

# Suggested Project Structure

```
alarm_clock/
│
├── main.py
├── alarms.json
├── scheduler.py
├── storage.py
├── audio.py
├── utils.py
└── alarm.wav
```

---

# Success Criteria

The implementation is considered complete if it can:

- Display a CLI menu
- Show alarms
- Add alarms
- Update alarms
- Delete alarms
- Persist alarms in JSON
- Calculate the next alarm correctly
- Sleep until the scheduled time
- Play an alarm sound for approximately 10 seconds
- Exit cleanly