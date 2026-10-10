# Tolo Todo (Odoo 19)

**Author:** Cherinet Kebede  
**Module:** `tolo_todo`  
**Odoo Version Tested:** Odoo 19.0 Community / Enterprise  

---

## 1. Installation & Upgrade

1. Copy the `tolo_todo` folder into your Odoo custom addons directory.
2. Restart the Odoo service.
3. Update App List via **Apps > Update Apps List**.
4. Search for `Tolo Todo` and click **Activate** (or upgrade via CLI: `odoo-bin -c odoo.conf -u tolo_todo -d <database>`).

---

## 2. Implemented Requirements

- **Task Model & Data Integrity:**
  - Required fields: `name`, `state`, `company_id`.
  - Python model constraints prevent invalid dates earlier than creation date.
- **Workflow & Header Action Lifecycle:**
  - Status progression: `Draft` ➔ `In Progress` ➔ `Done`.
  - Explicit header buttons: `Start Task`, `Mark as Done`, `Cancel Task`, `Reset to Draft`.
- **Cancel Rules:**
  - Users can cancel only from `Draft`.
  - Managers can cancel both from `Draft` and `In Progress`.
- **List View Visual Enhancements:**
  - Clear `state` badge widgets.
  - Tree row decorations (`decoration-warning` for overdue in-progress tasks, `decoration-danger` for overdue draft tasks, `decoration-success` for done).
- **Security & Access Story:**
  - **Todo User:** Access to view, create, and edit tasks assigned to them or created by them. Cannot delete records.
  - **Todo Manager:** Full visibility across all tasks across the company, ability to reassign, unlink, and cancel active in-progress tasks.
- **QWeb PDF Report:**
  - Available on individual or multi-select list actions via **Print > Todo Task Sheet**. Cleanly lays out assignment, deadline, priority, overdue status, and rich text notes.
- **Integration with Standard Odoo Modules:**
  - Inherits `mail.thread` and `mail.activity.mixin` (Discuss & Mail integration) providing followers, chatter tracking, and scheduling activities.

---

## 3. Section 8 Stretch Items Completed

1. **Overdue Logic:** Handled via compute/search methods on `is_overdue` field. Dynamically clears when tasks reach `Done` or `Cancelled`.
2. **Search View:** Rich filters for *My Tasks*, *Open Tasks*, *Overdue*, and Group By options (*Assignee*, *State*, *Deadline*).
3. **Activities & Next-Action:** Inherited from `mail.activity.mixin`, fully allowing managers to chase work and schedule calls/deadlines.
4. **Automated Test Suite:** Comprehensive test cases in `tests/test_todo_task.py` testing workflow progression, security constraints, and overdue computations.

---

## 4. Test Users & Groups Setup

1. Go to **Settings > Users & Companies > Users**.
2. Create or open two test users:
   - **User A (Assignee):** Under *Todo Management*, select **Todo User**.
   - **User B (Lead):** Under *Todo Management*, select **Todo Manager**.
3. Log in as **User A**: Verify they only see tasks they create or are assigned to, and cannot cancel in-progress items.
4. Log in as **User B**: Verify they see all tasks and can cancel in-progress items.

---

## 5. Known Limitations

- Multi-company domain rules default to standard Odoo record rule conventions for single company active context unless extended further with explicit multi-company record rules.