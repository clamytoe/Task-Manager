# **Updated Implementation Plan (Current Project State)**

## **Overview**

This document updates and replaces the original implementation plan included in PR #7. The project has evolved significantly, and this plan reflects the *current*, accurate state of all implemented features, along with optional future enhancements.

---

## **Completed Features**

### **1. Priority Feature**

**Status:** ✔ Implemented (creation‑time only)

- Priority is assigned when creating a task.
- Valid values: `"Low"`, `"Medium"`, `"High"`.
- Priority is displayed in the UI using colored labels.
- Priority **cannot be edited after creation** (current design).
- Priority does **not** affect sorting order.
- API validates priority on creation and update:
  - Invalid values fall back to `"Medium"`.
- Full test coverage for priority validation and storage.

---

### **2. Due Date Feature**

**Status:** ✔ Fully implemented

- Due dates stored as Python `date` objects.
- Accepted format: ISO‑8601 (`YYYY-MM-DD`).
- Display format: `DD/MM`.
- “Unassigned” shown when no due date exists.
- Inline editing via native date picker.
- Clearing the date sets it to `None`.
- Overdue detection:
  - A task is overdue if `due_date < today`.
  - Tasks due **today** are *not* overdue.
- Overdue tasks highlighted in red.
- Full API support for create/update.
- Full test coverage for all due‑date behaviors.

---

### **3. Inline Editing**

**Status:** ✔ Fully implemented

- Description editing (existing).
- Due date editing (new).
- Priority editing is **not** implemented (by design).
- All inline edits use AJAX and update without page reload.
- “Unassigned” appears immediately when clearing a date.

---

### **4. API Enhancements**

**Status:** ✔ Fully implemented

- `/api/tasks` (POST): create tasks with optional priority and due date.
- `/api/tasks/<id>` (PUT): update description, status, priority, and due date.
- Missing fields leave existing values unchanged.
- Empty string clears due date.
- Invalid date returns `400`.
- Task not found returns `404`.
- Full test coverage.

---

### **5. UI/UX Improvements**

**Status:** ✔ Fully implemented

- Pencil icons for editing description and due date.
- Flexbox layout ensures icons stay aligned.
- Overdue highlighting.
- “Unassigned” display for missing dates.
- Smooth inline editing experience.
- No sorting by priority or due date yet.

---

### **6. Test Suite**

**Status:** ✔ Fully implemented

- 82 passing tests.
- 100% coverage across all modules.
- Tests include:
  - Priority validation
  - Due date validation
  - Overdue logic
  - API create/update routes
  - UI routes
  - Error handling
  - Clearing due dates
  - Invalid date formats

---

## **Current Limitations (By Design)**

### **Priority Editing**

- Priority cannot be changed after creation.
- No UI or API endpoint exists for updating priority.
- This is intentional and matches current workflow.

### **Sorting**

- Tasks are **not** sorted by priority or due date.
- They appear in default query order (creation order).
- Sorting may be added in a future enhancement.

---

## **Optional Future Enhancements**

These items are not required for the current PR but may be added later.

### **1. Priority Editing**

- Add dropdown to change priority inline.
- Add API route to update priority.

### **2. Sorting**

- Sort tasks by:
  - Priority (High → Medium → Low)
  - Due date (earliest first)
  - Description (alphabetical)

### **3. Recurring Tasks**

- Weekly/monthly recurrence.
- Auto‑generation of next due date.

### **4. Reminder System**

- Email or in‑app notifications.
- “Remind me tomorrow” quick actions.

### **5. Calendar View**

- Monthly calendar showing tasks.
- Drag‑and‑drop rescheduling.

### **6. Bulk Editing**

- Multi‑select tasks.
- Bulk delete, bulk priority change, bulk due date change.

### **7. Project-Level Due Dates**

- Deadlines for entire projects.
- Overdue project highlighting.

### **8. Dark Mode**

- Theme toggle.
- Persistent user preference.

---

## **Summary**

The original implementation plan focused primarily on adding priority support. The project has since expanded to include a complete due‑date system, overdue detection, inline editing, UI improvements, and full test coverage.

This updated plan accurately reflects the current state of the project and provides a clear roadmap for future enhancements.
