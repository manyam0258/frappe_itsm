import frappe

def create_workflows():
    workflows = [
        {
            "doctype": "Workflow",
            "workflow_name": "Problem Workflow",
            "document_type": "ITSM Problem",
            "is_active": 1,
            "workflow_state_field": "status",
            "states": [
                {"state": "New", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Assess", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Root Cause Analysis", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Fix in Progress", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Known Error", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Resolved", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Closed", "doc_status": 1, "allow_edit": "ITSM Admin"}
            ],
            "transitions": [
                {"state": "New", "action": "Assess", "next_state": "Assess", "allowed": "ITSM Agent"},
                {"state": "Assess", "action": "Start RCA", "next_state": "Root Cause Analysis", "allowed": "ITSM Agent"},
                {"state": "Root Cause Analysis", "action": "Implement Fix", "next_state": "Fix in Progress", "allowed": "ITSM Agent"},
                {"state": "Root Cause Analysis", "action": "Publish Workaround", "next_state": "Known Error", "allowed": "ITSM Agent"},
                {"state": "Known Error", "action": "Implement Fix", "next_state": "Fix in Progress", "allowed": "ITSM Agent"},
                {"state": "Fix in Progress", "action": "Resolve", "next_state": "Resolved", "allowed": "ITSM Agent"},
                {"state": "Resolved", "action": "Close", "next_state": "Closed", "allowed": "ITSM Agent"}
            ]
        },
        {
            "doctype": "Workflow",
            "workflow_name": "Change Workflow",
            "document_type": "ITSM Change",
            "is_active": 1,
            "workflow_state_field": "status",
            "states": [
                {"state": "New", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Draft", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Pending Review", "doc_status": 0, "allow_edit": "ITSM Manager"},
                {"state": "CAB Scheduled", "doc_status": 0, "allow_edit": "ITSM Manager"},
                {"state": "CAB Approved", "doc_status": 0, "allow_edit": "ITSM Manager"},
                {"state": "Authorised", "doc_status": 0, "allow_edit": "ITSM Manager"},
                {"state": "Scheduled", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "In Progress", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Completed", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Failed", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "PIR Pending", "doc_status": 0, "allow_edit": "ITSM Agent"},
                {"state": "Cancelled", "doc_status": 1, "allow_edit": "ITSM Admin"},
                {"state": "Closed", "doc_status": 1, "allow_edit": "ITSM Admin"}
            ],
            "transitions": [
                {"state": "New", "action": "Draft", "next_state": "Draft", "allowed": "ITSM Agent"},
                {"state": "Draft", "action": "Submit for Review", "next_state": "Pending Review", "allowed": "ITSM Agent"},
                {"state": "Pending Review", "action": "Approve Review", "next_state": "CAB Scheduled", "allowed": "ITSM Manager"},
                {"state": "Pending Review", "action": "Reject Review", "next_state": "Draft", "allowed": "ITSM Manager"},
                {"state": "CAB Scheduled", "action": "CAB Approve", "next_state": "CAB Approved", "allowed": "ITSM Manager"},
                {"state": "CAB Scheduled", "action": "CAB Reject", "next_state": "Draft", "allowed": "ITSM Manager"},
                {"state": "CAB Approved", "action": "Authorise", "next_state": "Authorised", "allowed": "ITSM Manager"},
                {"state": "Authorised", "action": "Schedule", "next_state": "Scheduled", "allowed": "ITSM Agent"},
                {"state": "Scheduled", "action": "Start Implementation", "next_state": "In Progress", "allowed": "ITSM Agent"},
                {"state": "In Progress", "action": "Complete", "next_state": "Completed", "allowed": "ITSM Agent"},
                {"state": "In Progress", "action": "Fail", "next_state": "Failed", "allowed": "ITSM Agent"},
                {"state": "Completed", "action": "Require PIR", "next_state": "PIR Pending", "allowed": "ITSM Agent"},
                {"state": "Failed", "action": "Require PIR", "next_state": "PIR Pending", "allowed": "ITSM Agent"},
                {"state": "PIR Pending", "action": "Close", "next_state": "Closed", "allowed": "ITSM Agent"},
                {"state": "Completed", "action": "Close", "next_state": "Closed", "allowed": "ITSM Agent"},
                {"state": "Draft", "action": "Cancel", "next_state": "Cancelled", "allowed": "ITSM Agent"}
            ]
        }
    ]

    for wf in workflows:
        # Create states and actions first
        for s in wf["states"]:
            if not frappe.db.exists("Workflow State", s["state"]):
                frappe.get_doc({"doctype": "Workflow State", "workflow_state_name": s["state"]}).insert(ignore_permissions=True)
                
        for t in wf["transitions"]:
            if not frappe.db.exists("Workflow Action Master", t["action"]):
                frappe.get_doc({"doctype": "Workflow Action Master", "workflow_action_name": t["action"]}).insert(ignore_permissions=True)

        if not frappe.db.exists("Workflow", wf["workflow_name"]):
            doc = frappe.get_doc(wf)
            doc.insert(ignore_permissions=True)
            print(f"Created Workflow: {wf['workflow_name']}")
        else:
            print(f"Workflow {wf['workflow_name']} already exists")
            
    frappe.db.commit()
