import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_doctypes():
    doctypes = [
        {
            "doctype": "DocType",
            "name": "ITSM Change",
            "module": "Frappe ITSM",
            "custom": 1,
            "autoname": "CHG-.YYYY.-.#####",
            "naming_rule": "Expression",
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Agent", "read": 1, "write": 1, "create": 1},
                {"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Change Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
            ],
            "fields": [
                {"fieldname": "title", "fieldtype": "Data", "label": "Change Title", "reqd": 1, "in_list_view": 1},
                {"fieldname": "change_type", "fieldtype": "Select", "label": "Change Type", "options": "Standard\nNormal\nEmergency", "reqd": 1, "in_list_view": 1},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "New\nDraft\nPending Review\nCAB Scheduled\nCAB Approved\nAuthorised\nScheduled\nIn Progress\nCompleted\nFailed\nCancelled\nPIR Pending\nClosed", "default": "New", "in_list_view": 1},
                {"fieldname": "priority", "fieldtype": "Select", "label": "Priority", "options": "Low\nMedium\nHigh\nCritical", "reqd": 1},
                {"fieldname": "risk_level", "fieldtype": "Select", "label": "Risk Level", "options": "Very Low\nLow\nMedium\nHigh\nVery High", "reqd": 1, "in_list_view": 1},
                {"fieldname": "risk_score", "fieldtype": "Int", "label": "Risk Score", "read_only": 1},
                {"fieldname": "impact", "fieldtype": "Select", "label": "Impact", "options": "1-Enterprise Wide\n2-Department Wide\n3-Group Wide\n4-Individual", "reqd": 1},
                
                {"fieldname": "cb_1", "fieldtype": "Column Break"},
                {"fieldname": "category", "fieldtype": "Link", "label": "Category", "options": "ITSM Category", "reqd": 1},
                {"fieldname": "change_initiator", "fieldtype": "Link", "label": "Change Initiator", "options": "User", "reqd": 1},
                {"fieldname": "change_owner", "fieldtype": "Link", "label": "Change Owner", "options": "User", "reqd": 1},
                {"fieldname": "assigned_team", "fieldtype": "Link", "label": "Assigned Team", "options": "ITSM Team", "reqd": 1},
                {"fieldname": "technical_reviewer", "fieldtype": "Link", "label": "Technical Reviewer", "options": "User"},
                {"fieldname": "cab_required", "fieldtype": "Check", "label": "CAB Review Required"},
                
                {"fieldname": "sb_1", "fieldtype": "Section Break", "label": "Description & Plans"},
                {"fieldname": "description", "fieldtype": "Text Editor", "label": "Change Description", "reqd": 1},
                {"fieldname": "justification", "fieldtype": "Text Editor", "label": "Business Justification", "reqd": 1},
                {"fieldname": "implementation_plan", "fieldtype": "Text Editor", "label": "Implementation Plan", "reqd": 1},
                {"fieldname": "rollback_plan", "fieldtype": "Text Editor", "label": "Rollback Plan"},
                {"fieldname": "test_plan", "fieldtype": "Text Editor", "label": "Test Plan"},
                
                {"fieldname": "sb_2", "fieldtype": "Section Break", "label": "Schedule & Downtime"},
                {"fieldname": "start_datetime", "fieldtype": "Datetime", "label": "Planned Start", "reqd": 1},
                {"fieldname": "end_datetime", "fieldtype": "Datetime", "label": "Planned End", "reqd": 1},
                {"fieldname": "actual_start", "fieldtype": "Datetime", "label": "Actual Start"},
                {"fieldname": "actual_end", "fieldtype": "Datetime", "label": "Actual End"},
                {"fieldname": "cb_2", "fieldtype": "Column Break"},
                {"fieldname": "downtime_expected", "fieldtype": "Check", "label": "Downtime Expected"},
                {"fieldname": "downtime_start", "fieldtype": "Datetime", "label": "Downtime Start", "depends_on": "eval:doc.downtime_expected==1"},
                {"fieldname": "downtime_end", "fieldtype": "Datetime", "label": "Downtime End", "depends_on": "eval:doc.downtime_expected==1"},
                {"fieldname": "blackout_conflict", "fieldtype": "Check", "label": "Blackout Conflict", "read_only": 1},
                {"fieldname": "conflict_details", "fieldtype": "Small Text", "label": "Conflict Details", "read_only": 1, "depends_on": "eval:doc.blackout_conflict==1"},
                
                {"fieldname": "sb_3", "fieldtype": "Section Break", "label": "Closure & PIR"},
                {"fieldname": "close_code", "fieldtype": "Select", "label": "Close Code", "options": "Successful\nSuccessful with Issues\nUnsuccessful - Rolled Back\nUnsuccessful - Partial\nCancelled"},
                {"fieldname": "close_notes", "fieldtype": "Text Editor", "label": "Close Notes"},
                {"fieldname": "pir_required", "fieldtype": "Check", "label": "PIR Required"},
                {"fieldname": "pir_notes", "fieldtype": "Text Editor", "label": "PIR Notes", "depends_on": "eval:doc.pir_required==1"},
                {"fieldname": "linked_problem", "fieldtype": "Link", "label": "Linked Problem", "options": "ITSM Problem"}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Change Task",
            "module": "Frappe ITSM",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "phase", "fieldtype": "Select", "label": "Phase", "options": "Pre-Implementation\nImplementation\nPost-Implementation\nRollback", "reqd": 1, "in_list_view": 1},
                {"fieldname": "title", "fieldtype": "Data", "label": "Task Title", "reqd": 1, "in_list_view": 1},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Open\nIn Progress\nCompleted\nCancelled", "default": "Open", "in_list_view": 1},
                {"fieldname": "assignee", "fieldtype": "Link", "label": "Assignee", "options": "User", "in_list_view": 1},
                {"fieldname": "due_date", "fieldtype": "Datetime", "label": "Due Date"}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Change Risk Question",
            "module": "Frappe ITSM",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "question", "fieldtype": "Data", "label": "Risk Factor", "read_only": 1, "in_list_view": 1},
                {"fieldname": "answer", "fieldtype": "Select", "label": "Answer", "options": "1 - Low\n2 - Medium\n3 - High\n4 - Very High", "in_list_view": 1},
                {"fieldname": "weight", "fieldtype": "Percent", "label": "Weight", "read_only": 1, "in_list_view": 1}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Blackout Window",
            "module": "Frappe ITSM",
            "custom": 1,
            "autoname": "field:title",
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Agent", "read": 1},
                {"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Change Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
            ],
            "fields": [
                {"fieldname": "title", "fieldtype": "Data", "label": "Title", "unique": 1, "reqd": 1, "in_list_view": 1},
                {"fieldname": "start_datetime", "fieldtype": "Datetime", "label": "Start Date & Time", "reqd": 1, "in_list_view": 1},
                {"fieldname": "end_datetime", "fieldtype": "Datetime", "label": "End Date & Time", "reqd": 1, "in_list_view": 1},
                {"fieldname": "description", "fieldtype": "Text", "label": "Description"}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM CAB Member",
            "module": "Frappe ITSM",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "user", "fieldtype": "Link", "label": "Member", "options": "User", "reqd": 1, "in_list_view": 1},
                {"fieldname": "role", "fieldtype": "Data", "label": "Role", "in_list_view": 1},
                {"fieldname": "attendance", "fieldtype": "Select", "label": "Attendance", "options": "Pending\nAttended\nAbsent", "default": "Pending", "in_list_view": 1},
                {"fieldname": "vote", "fieldtype": "Select", "label": "Vote", "options": "Pending\nApprove\nReject\nAbstain", "default": "Pending", "in_list_view": 1}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM CAB Agenda Item",
            "module": "Frappe ITSM",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "change_request", "fieldtype": "Link", "label": "Change Request", "options": "ITSM Change", "reqd": 1, "in_list_view": 1},
                {"fieldname": "presenter", "fieldtype": "Link", "label": "Presenter", "options": "User", "in_list_view": 1},
                {"fieldname": "decision", "fieldtype": "Select", "label": "Decision", "options": "Pending\nApproved\nRejected\nDeferred", "default": "Pending", "in_list_view": 1}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM CAB Meeting",
            "module": "Frappe ITSM",
            "custom": 1,
            "autoname": "CAB-.YYYY.-.###",
            "naming_rule": "Expression",
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Agent", "read": 1, "write": 1, "create": 1},
                {"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Change Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM CAB Member", "read": 1, "write": 1},
                {"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
            ],
            "fields": [
                {"fieldname": "meeting_type", "fieldtype": "Select", "label": "Meeting Type", "options": "Regular CAB\nEmergency CAB (ECAB)\nPost-Implementation Review", "reqd": 1, "in_list_view": 1},
                {"fieldname": "status", "fieldtype": "Select", "label": "Meeting Status", "options": "Scheduled\nIn Progress\nCompleted\nCancelled", "default": "Scheduled", "in_list_view": 1},
                {"fieldname": "scheduled_datetime", "fieldtype": "Datetime", "label": "Scheduled Date & Time", "reqd": 1, "in_list_view": 1},
                {"fieldname": "duration_minutes", "fieldtype": "Int", "label": "Duration (mins)", "reqd": 1, "default": "60"},
                {"fieldname": "cb_1", "fieldtype": "Column Break"},
                {"fieldname": "location", "fieldtype": "Data", "label": "Location / Link"},
                {"fieldname": "cab_chair", "fieldtype": "Link", "label": "CAB Chair", "options": "User", "reqd": 1},
                {"fieldname": "quorum_required", "fieldtype": "Int", "label": "Quorum Required (%)", "reqd": 1, "default": "51"},
                
                {"fieldname": "sb_1", "fieldtype": "Section Break", "label": "Agenda & Members"},
                {"fieldname": "agenda_changes", "fieldtype": "Table", "label": "Agenda Changes", "options": "ITSM CAB Agenda Item"},
                {"fieldname": "cab_members", "fieldtype": "Table", "label": "CAB Members", "options": "ITSM CAB Member"},
                
                {"fieldname": "sb_2", "fieldtype": "Section Break", "label": "Notes"},
                {"fieldname": "meeting_notes", "fieldtype": "Text Editor", "label": "Meeting Notes"}
            ]
        }
    ]

    for d in doctypes:
        if not frappe.db.exists("DocType", d["name"]):
            doc = frappe.get_doc(d)
            doc.insert(ignore_permissions=True)
            print(f"Created DocType {d['name']}")
        else:
            print(f"DocType {d['name']} already exists")

    # Add child tables to ITSM Change
    change = frappe.get_doc("DocType", "ITSM Change")
    has_tasks = any(f.fieldname == "change_tasks" for f in change.fields)
    has_risk = any(f.fieldname == "risk_assessment" for f in change.fields)
    
    if not has_tasks:
        change.append("fields", {
            "fieldname": "change_tasks", "fieldtype": "Table", "label": "Change Tasks", "options": "ITSM Change Task", "insert_after": "actual_end"
        })
    if not has_risk:
        change.append("fields", {
            "fieldname": "risk_assessment", "fieldtype": "Table", "label": "Risk Assessment", "options": "ITSM Change Risk Question", "insert_after": "impact"
        })
        
    # Also add cab_meeting link to Change
    has_cab = any(f.fieldname == "cab_meeting" for f in change.fields)
    if not has_cab:
        change.append("fields", {
            "fieldname": "cab_meeting", "fieldtype": "Link", "label": "CAB Meeting", "options": "ITSM CAB Meeting", "insert_after": "cab_required"
        })
    
    if not has_tasks or not has_risk or not has_cab:
        change.save(ignore_permissions=True)
        print("Updated ITSM Change with child tables and links")
        
    frappe.db.commit()

