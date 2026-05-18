import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_doctypes():
    doctypes = [
        {
            "doctype": "DocType",
            "name": "ITSM Problem",
            "module": "Frappe ITSM",
            "custom": 1,
            "autoname": "PRB-.YYYY.-.#####",
            "naming_rule": "Expression",
            "fields": [
                {"fieldname": "title", "fieldtype": "Data", "label": "Problem Summary", "reqd": 1, "in_list_view": 1},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "New\nAssess\nRoot Cause Analysis\nFix in Progress\nKnown Error\nResolved\nClosed", "default": "New", "in_list_view": 1},
                {"fieldname": "priority", "fieldtype": "Select", "label": "Priority", "options": "P1-Critical\nP2-High\nP3-Moderate\nP4-Low", "in_list_view": 1},
                {"fieldname": "category", "fieldtype": "Link", "label": "Category", "options": "ITSM Category", "reqd": 1},
                {"fieldname": "problem_owner", "fieldtype": "Link", "label": "Problem Owner", "options": "User"},
                {"fieldname": "assigned_team", "fieldtype": "Link", "label": "Assigned Team", "options": "ITSM Team"},
                
                {"fieldname": "cb_1", "fieldtype": "Column Break"},
                {"fieldname": "error_code", "fieldtype": "Data", "label": "Known Error Code"},
                {"fieldname": "pir_required", "fieldtype": "Check", "label": "PIR Required"},
                {"fieldname": "workaround_published", "fieldtype": "Check", "label": "Workaround Published"},
                
                {"fieldname": "sb_1", "fieldtype": "Section Break", "label": "Description"},
                {"fieldname": "description", "fieldtype": "Text Editor", "label": "Problem Description", "reqd": 1},
                {"fieldname": "workaround", "fieldtype": "Text Editor", "label": "Workaround"},
                {"fieldname": "permanent_fix", "fieldtype": "Text Editor", "label": "Permanent Fix"},
                
                {"fieldname": "sb_2", "fieldtype": "Section Break", "label": "Root Cause Analysis (RCA)"},
                {"fieldname": "rca_methodology", "fieldtype": "Select", "label": "RCA Methodology", "options": "5-Whys\nFishbone\nFault Tree\nTimeline Analysis\nOther"},
                {"fieldname": "root_cause_category", "fieldtype": "Select", "label": "Root Cause Category", "options": "Hardware Failure\nSoftware Bug\nConfiguration Error\nProcess Gap\nHuman Error\nExternal/Vendor\nUnknown"},
                {"fieldname": "root_cause", "fieldtype": "Text Editor", "label": "Root Cause"},
                {"fieldname": "rca_five_whys", "fieldtype": "Text Editor", "label": "5-Whys Analysis", "depends_on": "eval:doc.rca_methodology=='5-Whys'"},
                
                {"fieldname": "sb_3", "fieldtype": "Section Break", "label": "Resolution & Closure"},
                {"fieldname": "resolution_notes", "fieldtype": "Text Editor", "label": "Resolution Notes"},
                {"fieldname": "closed_at", "fieldtype": "Datetime", "label": "Closed At", "read_only": 1},
                {"fieldname": "pir_completed_at", "fieldtype": "Datetime", "label": "PIR Completed At", "read_only": 1}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Problem Task",
            "module": "Frappe ITSM",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "title", "fieldtype": "Data", "label": "Task Title", "reqd": 1, "in_list_view": 1},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Open\nIn Progress\nCompleted\nCancelled", "default": "Open", "in_list_view": 1},
                {"fieldname": "assignee", "fieldtype": "Link", "label": "Assignee", "options": "User", "in_list_view": 1},
                {"fieldname": "due_date", "fieldtype": "Date", "label": "Due Date"}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Problem Incident",
            "module": "Frappe ITSM",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "incident", "fieldtype": "Link", "label": "Incident", "options": "ITSM Incident", "reqd": 1, "in_list_view": 1}
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

    # Add child tables to ITSM Problem
    problem = frappe.get_doc("DocType", "ITSM Problem")
    has_tasks = any(f.fieldname == "problem_tasks" for f in problem.fields)
    has_incidents = any(f.fieldname == "linked_incidents" for f in problem.fields)
    
    if not has_tasks:
        problem.append("fields", {
            "fieldname": "problem_tasks", "fieldtype": "Table", "label": "Problem Tasks", "options": "ITSM Problem Task", "insert_after": "assigned_team"
        })
    if not has_incidents:
        problem.append("fields", {
            "fieldname": "linked_incidents", "fieldtype": "Table", "label": "Linked Incidents", "options": "ITSM Problem Incident", "insert_after": "problem_tasks"
        })
    
    if not has_tasks or not has_incidents:
        problem.save(ignore_permissions=True)
        print("Updated ITSM Problem with child tables")
        
    frappe.db.commit()

