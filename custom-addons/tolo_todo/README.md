# Tolo Todo (Odoo 19)

**Candidate:** Cherinet Kebede  
**Company:** Tolo Solutions  
**Module:** `tolo_todo`  
**Odoo Version Tested:** Odoo 19.0 Community / Enterprise (Ubuntu 22.04 LTS / Python 3.12)  

---

## 1. Overview & Business Story

`tolo_todo` is a structured task management application engineered for production use on Odoo 19. It enforces strict data governance, clean lifecycle progression, multi-tier security, and real-time integration with Odoo's core communication and partner ecosystems.

---

## 2. Implemented Requirements Mapping

### 1. Required Fields & Data Quality
- **Mandatory Fields:** `name` (Task Title), `state` (Workflow Status), and `company_id` (Multi-company safe).
- **Relational Integrity:** `assignee_id` (`res.users`), `partner_id` (`res.partner`), and `deadline` (`Date`).
- **Defaults & Tracking:** Assignee defaults to current user; critical business fields track changes through chatter (`tracking=True`).

### 2. Status Workflow & Header Actions
- **Workflow Lifecycle:** `Draft` (`draft`) ➔ `In Progress` (`in_progress`) ➔ `Done` (`done`).
- **Action Buttons:** Progression occurs via intentional header actions (`Start Task`, `Mark as Done`, `Reset to Draft`). Direct manual state tampering is discouraged via UI statusbar widgets.

### 3. Cancel Rules (User vs. Manager)
- **Draft State:** Both **Todo Users** and **Todo Managers** can cancel tasks via `Cancel Task`.
- **In-Progress State:** Only **Todo Managers** are authorized to cancel active work. This is enforced both visually (conditional button visibility) and programmatically in Python (`action_cancel` raises `UserError` if unauthorized).
- **Done/Cancelled:** Cannot be cancelled; cancelled tasks can be reset to draft via `Reset to Draft`.

### 4. High-Visibility List View
- Distinct badge widgets for `state` (`draft` = info, `in_progress` = primary, `done` = success, `cancelled` = secondary).
- List-level dynamic row highlighting:
  - Overdue In-Progress tasks are highlighted with `decoration-warning`.
  - Overdue Draft tasks are highlighted with `decoration-danger`.
  - Done tasks show `decoration-success`; Cancelled tasks show `decoration-muted`.

### 5. Security & Access Model (Odoo 19 Architecture)
- **Privilege Architecture:** Built using Odoo 19's `res.groups.privilege` (`privilege_tolo_todo`) referencing `module_category_productivity_tolo_todo`.
- **Todo User (`group_tolo_todo_user`):**
  - **Permissions:** Read, Create, Write own tasks (`perm_unlink=0`).
  - **Record Rule:** Can only view and edit tasks where `assignee_id = user.id` OR `create_uid = user.id`. Cannot delete tasks.
- **Todo Manager (`group_tolo_todo_manager`):**
  - **Permissions:** Full CRUD (`perm_read=1`, `perm_write=1`, `perm_create=1`, `perm_unlink=1`).
  - **Record Rule:** Global domain `[(1, '=', 1)]` allows visibility and management across all organizational tasks.

### 6. QWeb PDF Reporting
- Bound report action **Todo Task Sheet** available on Form and multi-select List views (**Print > Todo Task Sheet**).
- Renders external layout, dynamic status badges, assignee, priority, company, overdue indicators, and rich-text task descriptions.

### 7. Standard App Integrations
- **Discuss / Mail (`mail.thread`, `mail.activity.mixin`):**
  - Full audit chatter trail for updates.
  - **Automated Activity Creation:** Starting a task (`Start Task`) schedules an actionable To-Do activity in Odoo's top systray navigation bar (`mail.activity`) assigned to the task owner.
  - **Email Dispatch:** Dispatches formatted notifications (`message_post`) to the assignee's email on lifecycle milestones.
- **Contacts (`res.partner`):**
  - Optional `partner_id` field on tasks.
  - Extends `res.partner` with a **Smart Button** displaying the count of linked Todo tasks with 1-click drill-down.

### 8. Mid-Level Depth Items Completed (Stretch Deliverables)
1. **Dynamic Overdue Engine:** Unstored computed field `is_overdue` with custom domain searcher (`_search_is_overdue`) ensuring 100% real-time date accuracy without cron latency.
2. **Comprehensive Search View:** Default filters (`My Tasks`, `Open Tasks`), conditional filters (`Overdue`), and Group-By operators (`Assignee`, `State`, `Deadline`).
3. **Chatter & Next-Action Activities:** Automatic activity scheduling linked with core Odoo activity types.
4. **Partner Smart Button & Stats:** Real-time task counting and action window drill-down on `res.partner`.
5. **Automated Unit Test Suite:** `tests/test_todo_task.py` testing workflow progression, security boundaries, and overdue calculations.

---

## 3. How to Install & Upgrade

### Installation
```bash
# Place tolo_todo inside your custom addons directory
./odoo-bin -c odoo.conf -d <database_name> -i tolo_todo