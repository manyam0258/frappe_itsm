**Statement:** In frappe framework: i have a scenario \- where a document having the workflow \- but we need assignment rule should also come into the picture, Lets say we are developing helpdesk like tool where it have all the features like servicenow, so in the document transition thru the workflow, the user assignment rules plays a key role, how do we pull this into our frappe\_itsm app.


| Doctype | ID | Created by |
| :---- | :---- | :---- |
| Incident | INC-0001 | Any user |

| Roles | ITSM\_AGENT | ITSM\_MANAGER | ITSM\_ADMIN |
| :---- | :---- | :---- | :---- |
| USERS | A | M | X |
|   | B | N | Y |
|   | C | O | Z |

**Workflow:**

| State | Doc Status | Update Field | Update Value | Only Allow Edit For |
| :---- | :---- | :---- | :---- | :---- |
| New |   |   |   | ALL |
| Assigned |   |   |   | ITSM\_AGENT |
| In Progress |   |   |   | ITSM\_AGENT |
| Pending |   |   |   | ITSM\_AGENT |
| Resolved |   |   |   | ITSM\_AGENT |
| Closed |   |   |   | ITSM\_AGENT |
| Cancelled |   |   |   | ITSM\_AGENT |

| Doctype | ID | Created by |
| :---- | :---- | :---- |
| Problem | PRO-0001 | ITSM Agent |

**Workflow:**

| State | Doc Status | Update Field | Update Value | Only Allow Edit For |
| :---- | :---- | :---- | :---- | :---- |
| New |   |   |   | ITSM Agent |
| Assess |   |   |   | ITSM Agent |
| Root Cause Analysis |   |   |   | ITSM Agent |
| Fix in Progress |   |   |   | ITSM Agent |
| Known Error |   |   |   | ITSM Agent |
| Resolved |   |   |   | ITSM Agent |
| Closed |   |   |   | ITSM Agent |

| Doctype | ID | Created by |
| :---- | :---- | :---- |
| Change | CHG-0001 | ITSM Agent |

**Workflow:**

| State | Doc Status | Update Field | Update Value | Only Allow Edit For |
| :---- | :---- | :---- | :---- | :---- |
| New |   |   |   | ITSM Agent |
| Draft |   |   |   | ITSM Agent |
| Pending Review |   |   |   | ITSM Manager |
| CAB Scheduled |   |   |   | ITSM Manager |
| CAB Approved |   |   |   | ITSM Manager |
| Authorised |   |   |   | ITSM Manager |
| Scheduled |   |   |   | ITSM Agent |
| In Progress |   |   |   | ITSM Agent |
| Completed |   |   |   | ITSM Agent |
| Failed |   |   |   | ITSM Agent |
| PIR Pending |   |   |   | ITSM Agent |
| Cancelled |   |   |   | ITSM Admin |
| Closed |   |   |   | ITSM Admin |

Frappe **natively supports Round Robin assignment rules**, but because you are combining them with a strict multi-state Workflow (Incident, Problem, Change), **you will need a minor code customization** to make them work perfectly together.

By default, Frappe's Assignment Rules only trigger on the New state (document creation) or standard Save actions. They do not automatically re-evaluate or distribute load when a document transitions through Workflow states like *Assigned*, *Assess*, or *Pending Review*.

Here is exactly how the default feature works and how you must customize it to handle your matrix.

## ---

**🟢 What Frappe Supports Natively (No Code)**

Frappe's **Assignment Rule** doctype natively has a "Round Robin" rule condition.

* **Load Balancing / Round Robin:** It automatically tracks which agent has the fewest open assignments or who is next in line, distributing **Incident**, **Problem**, and **Change** records equally among the users you specify (Users A, B, C for Agents; M, N, O for Managers).  
* **Role-Based Filtering:** You can create separate rules targeting specific Doctypes based on the roles listed in your image (ITSM\_AGENT, ITSM\_MANAGER, etc.).

## ---

**🔴 Why You Need Customization**

Looking at your workflow image:

1. **Incident Workflow:** Transitions from New $\\rightarrow$ Assigned. If a document is created as New, the assignment rule triggers. But if it needs to route to a new team or update tracking on transition, the Workflow engine bypasses standard assignment logic.  
2. **Problem & Change Workflows:** These involve role handoffs. For example, a **Change** goes from Draft (Agent) $\\rightarrow$ Pending Review (Manager). Frappe’s default assignment rule cannot automatically detect this workflow state shift to clear the Agent's assignment and Round-Robin assign it to Managers (M, N, O).

## ---

**🛠️ The Solution: Generic, Low-Code Customization**

To execute Assignment Rules dynamically when workflow transitions occur (without hardcoding roles or state fields), implement a generic hook structure that integrates with your custom `ITSM Team` queues.

### **1. How ITSM Team and Assignment Rules Integrate**
* **`ITSM Team`** defines the queue/support group (e.g. "Network Team", "Database Team") set on the ticket via the `assigned_team` link field.
* **`Assignment Rule`** is the automation engine. You create rules in the UI where:
  * **Document Type:** `ITSM Incident`
  * **Condition:** `doc.assigned_team == "Network Team" and doc.workflow_state == "Assigned"` (or whatever the state field is called)
  * **Rule Type:** Round Robin or Load Balancing
  * **Users:** User A, User B, User C (the members of the team).

---

### **2. Add the Workflow-Assignment Hook**

Register the dynamic hook in `apps/frappe_itsm/frappe_itsm/hooks.py`:

```python
doc_events = {
    "ITSM Incident": {
        "before_save": "frappe_itsm.frappe_itsm.utils.assignment.handle_workflow_assignments"
    },
    "ITSM Problem": {
        "before_save": "frappe_itsm.frappe_itsm.utils.assignment.handle_workflow_assignments"
    },
    "ITSM Change": {
        "before_save": "frappe_itsm.frappe_itsm.utils.assignment.handle_workflow_assignments"
    }
}
```

---

### **3. Implement the Dynamic Execution Logic**

Create the module `apps/frappe_itsm/frappe_itsm/frappe_itsm/utils/assignment.py`. This script dynamically looks up the active workflow's state field, preserves assignment history by closing open assignments instead of deleting them, and triggers the corrected native `apply` function.

```python
import frappe
from frappe.model.workflow import get_workflow_name
from frappe.automation.doctype.assignment_rule.assignment_rule import apply

def handle_workflow_assignments(doc, method):
    # 1. Dynamically find active Workflow and its state field
    workflow_name = get_workflow_name(doc.doctype)
    if not workflow_name:
        return

    workflow = frappe.get_cached_doc("Workflow", workflow_name)
    state_field = workflow.workflow_state_field or "workflow_state"

    # 2. Only run if the workflow state has actually changed
    if not doc.has_value_changed(state_field):
        return

    # 3. Close existing open assignments instead of deleting them (preserves ITIL audit trail)
    frappe.db.set_value(
        "ToDo",
        {
            "reference_type": doc.doctype,
            "reference_name": doc.name,
            "status": "Open"
        },
        "status",
        "Closed"
    )

    # 4. Trigger the native assignment engine to apply rules for the new state
    apply(doc)
```

---

**💡 Summary of Benefits**  
* **Zero custom distribution math:** Frappe handles the equal distribution of tickets natively.
* **No Hardcoding:** State fields (`status` vs `workflow_state`) are resolved dynamically from active workflow records.
* **Audit-Complete (ITIL Compliant):** Changing assignments preserves history by closing `ToDo` entries instead of deleting them.
* **Complementary Queues:** `ITSM Team` acts as the queue link on the ticket, while `Assignment Rule` dynamically allocates to group members.