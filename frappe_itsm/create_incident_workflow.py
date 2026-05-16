import frappe

def create_workflow():
    states = ["New", "Assigned", "In Progress", "Pending", "Resolved", "Closed", "Cancelled"]
    for state in states:
        if not frappe.db.exists("Workflow State", state):
            doc = frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": state,
                "icon": "check",
                "style": "Primary"
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Workflow State: {state}")

    actions = ["Assign", "Start Work", "Put On Hold", "Resume", "Resolve", "Close", "Reopen", "Cancel"]
    for action in actions:
        if not frappe.db.exists("Workflow Action Master", action):
            doc = frappe.get_doc({
                "doctype": "Workflow Action Master",
                "workflow_action_name": action
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Workflow Action: {action}")

    if not frappe.db.exists("Workflow", "Incident Workflow"):
        doc = frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Incident Workflow",
            "document_type": "ITSM Incident",
            "is_active": 1,
            "send_email_alert": 0,
            "states": [
                {"state": "New", "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "Assigned", "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "In Progress", "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "Pending", "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "Resolved", "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "Closed", "doc_status": 1, "allow_edit": "System Manager"},
                {"state": "Cancelled", "doc_status": 2, "allow_edit": "System Manager"}
            ],
            "transitions": [
                {"state": "New", "action": "Assign", "next_state": "Assigned", "allowed": "System Manager"},
                {"state": "Assigned", "action": "Start Work", "next_state": "In Progress", "allowed": "System Manager"},
                {"state": "In Progress", "action": "Put On Hold", "next_state": "Pending", "allowed": "System Manager"},
                {"state": "Pending", "action": "Resume", "next_state": "In Progress", "allowed": "System Manager"},
                {"state": "In Progress", "action": "Resolve", "next_state": "Resolved", "allowed": "System Manager"},
                {"state": "Resolved", "action": "Close", "next_state": "Closed", "allowed": "System Manager"},
                {"state": "Resolved", "action": "Reopen", "next_state": "In Progress", "allowed": "System Manager"},
                {"state": "New", "action": "Cancel", "next_state": "Cancelled", "allowed": "System Manager"},
                {"state": "Assigned", "action": "Cancel", "next_state": "Cancelled", "allowed": "System Manager"},
                {"state": "In Progress", "action": "Cancel", "next_state": "Cancelled", "allowed": "System Manager"},
                {"state": "Pending", "action": "Cancel", "next_state": "Cancelled", "allowed": "System Manager"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created Workflow: Incident Workflow")
    else:
        print("Incident Workflow already exists")

    frappe.db.commit()
