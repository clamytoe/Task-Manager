# **Due Date Specification (`due_date_spec.md`)**

## **Overview**

The Task Manager supports optional due dates for tasks. Due dates allow users to track deadlines, highlight overdue items, and sort tasks more effectively. All due‑date handling is consistent across the UI, backend routes, and API endpoints.

---

## **Data Model**

### **Storage**

- Due dates are stored as `date` objects in the database.
- The column is nullable:
  - `NULL` means “no due date assigned.”

### **Accepted Format**

- All incoming due dates must be ISO‑8601 format:

      YYYY-MM-DD

- Example:

      2026-09-10

### **Invalid Formats**

Any non‑ISO date (e.g., `"09/10/2026"`, `"2026/09/10"`, `"banana"`) results in:

      HTTP 400 Invalid date format, expected YYYY-MM-DD

---

## **Behavior Summary**

- Accepts ISO dates (`YYYY-MM-DD`)
- Stores internally as Python `date` objects
- Displays in UI as `DD/MM`
- Empty string clears the due date
- Missing field leaves the due date unchanged
- Invalid date returns HTTP 400
- Overdue = `due_date < today()`
- No due date = never overdue
- Priority fallback = `"Medium"`
- Sorting: **priority → due date → task name**

---

## **Overdue Logic**

A task is considered **overdue** when:

1. `due_date` is not `None`
2. `due_date < date.today()`
3. Tasks due today are NOT considered overdue.

Tasks with no due date are **never** overdue.

### **UI Behavior**

- Overdue tasks are visually highlighted (red text or icon).
- Overdue status does **not** affect sorting order unless a future feature changes this.

---

## **Routes**

### **1. `/edit_due_date/<id>` (POST)**

Updates the due date for a task.

#### **Route Input Rules**

- `"due_date": "YYYY-MM-DD"` → sets the date
- `"due_date": ""` → clears the date
- `"due_date": null` → clears the date
- Missing `"due_date"` → no change

#### **Route Error Handling**

- Invalid date → `400`
- Task not found → `404`

#### **Route Success**

      204 No Content

---

### **2. `/api/tasks` (POST) — Create Task**

Creates a new task with optional due date.

#### **Create Task Input Rules**

- `"due_date": "YYYY-MM-DD"` → parsed and stored
- `"due_date": ""` → stored as `None`
- Missing `"due_date"` → stored as `None`

#### **Create Task Priority Rules**

- `"priority"` must be `"Low"`, `"Medium"`, or `"High"`
- Anything else → fallback to `"Medium"`

#### **Create Task Error Handling**

- Missing `"task"` or `"project_id"` → `400`
- Invalid date → `400`

#### **Create Task Success**

      201 Created

---

### **3. `/api/tasks/<id>` (PUT) — Update Task**

Updates any combination of task fields, including due date.

#### **Task Update Input Rules**

- Missing fields → leave existing values unchanged
- `"due_date": "YYYY-MM-DD"` → set date
- `"due_date": ""` → clear date
- `"due_date": null` → clear date

#### **Task Update Error Handling**

- Invalid date → `400`
- Task not found → `404`

#### **Task Update Success**

      200 OK

---

## **UI Specification**

### **Display Format**

Due dates are shown as:

      DD/MM

Example:

      10/09

### **Editing**

- Clicking the due date opens a date picker.
- Clearing the field removes the due date.
- The UI sends:
  - `""` to clear
  - `"YYYY-MM-DD"` to set

### **Overdue Highlighting**

- Overdue tasks appear in red.
- Optional: A tooltip such as `title="Overdue" may be added.

---

## **Sorting Rules**

Tasks are sorted in this order:

1. **Priority**
   - High  
   - Medium  
   - Low  
2. **Due Date**
   - Earliest first  
   - Tasks with no due date appear last  
3. **Task Description**
   - Alphabetical

---

## **Database Constraints**

- `due_date` is nullable.
- No restriction on past or future dates.
- Validation occurs at the route/API layer.

---

## **Timezone Assumptions**

- All comparisons use server‑local date (`date.today()`).
- No timezone conversion is performed.
- Due dates are treated as all‑day deadlines.

---

## **Future Extensions**

This spec is designed to support future enhancements:

- Due **time** (datetime instead of date)
- Recurring tasks
- Reminder notifications
- Calendar integration (Google/Outlook)
- Overdue sorting options
- Automatic snooze/reschedule
- Bulk due‑date editing

---

## **Examples**

### **Valid Create Request**

```json
{
  "project_id": 1,
  "task": "Pay rent",
  "priority": "High",
  "due_date": "2026-09-10"
}
```

### **Clear Due Date**

```json
{
  "due_date": ""
}
```

### **Invalid Date**

```json
{
  "due_date": "09-10-2026"
}
```

Response:

      400 Invalid date format, expected YYYY-MM-DD
