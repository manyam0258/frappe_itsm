import frappe

def create_doctypes():
    doctypes = [
        {
            "doctype": "DocType",
            "name": "ITSM Resolution Code",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:resolution_code",
            "fields": [
                {"fieldname": "resolution_code", "label": "Resolution Code", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "description", "label": "Description", "fieldtype": "Text"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Priority Matrix",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:matrix_name",
            "fields": [
                {"fieldname": "matrix_name", "label": "Matrix Name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company"},
                {"fieldname": "impact", "label": "Impact", "fieldtype": "Select", "options": "1-Enterprise Wide\n2-Department Wide\n3-Group Wide\n4-Individual", "reqd": 1},
                {"fieldname": "urgency", "label": "Urgency", "fieldtype": "Select", "options": "1-Critical\n2-High\n3-Medium\n4-Low", "reqd": 1},
                {"fieldname": "priority", "label": "Priority", "fieldtype": "Select", "options": "P1-Critical\nP2-High\nP3-Moderate\nP4-Low\nP5-Planning", "reqd": 1}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Incident CI",
            "module": "Frappe ITSM",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "ci", "label": "Configuration Item", "fieldtype": "Data"} # Since ITSM CI is not yet created
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Watch List",
            "module": "Frappe ITSM",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "user", "label": "User", "fieldtype": "Link", "options": "User", "reqd": 1}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Incident",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "naming_series:",
            "fields": [
                {"fieldname": "naming_series", "label": "Naming Series", "fieldtype": "Select", "options": "INC-.YYYY.-.#####", "default": "INC-.YYYY.-.#####", "hidden": 1},
                {"fieldname": "title", "label": "Subject", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "New\nAssigned\nIn Progress\nPending\nResolved\nClosed\nCancelled", "reqd": 1, "default": "New"},
                {"fieldname": "incident_type", "label": "Incident Type", "fieldtype": "Select", "options": "Service Request\nIncident\nMajor Incident", "reqd": 1, "default": "Incident"},
                {"fieldname": "description", "label": "Description", "fieldtype": "Text Editor", "reqd": 1},
                {"fieldname": "category", "label": "Category", "fieldtype": "Link", "options": "ITSM Category", "reqd": 1},
                {"fieldname": "sub_category", "label": "Sub-Category", "fieldtype": "Link", "options": "ITSM Sub Category"},
                {"fieldname": "item_affected", "label": "Item Affected", "fieldtype": "Data"},
                {"fieldname": "impact", "label": "Impact", "fieldtype": "Select", "options": "1-Enterprise Wide\n2-Department Wide\n3-Group Wide\n4-Individual", "reqd": 1},
                {"fieldname": "urgency", "label": "Urgency", "fieldtype": "Select", "options": "1-Critical\n2-High\n3-Medium\n4-Low", "reqd": 1},
                {"fieldname": "priority", "label": "Priority", "fieldtype": "Select", "options": "P1-Critical\nP2-High\nP3-Moderate\nP4-Low\nP5-Planning", "reqd": 1, "read_only": 1},
                {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "reqd": 1},
                {"fieldname": "department", "label": "Department", "fieldtype": "Link", "options": "Department"},
                {"fieldname": "source_channel", "label": "Source Channel", "fieldtype": "Select", "options": "Email\nWeb Portal\nWhatsApp\nChat\nPhone\nWalk-in\nAPI", "reqd": 1, "default": "Web Portal"},
                
                {"fieldname": "requester_section", "label": "Requester Info", "fieldtype": "Section Break"},
                {"fieldname": "raised_by", "label": "Raised By", "fieldtype": "Link", "options": "User", "reqd": 1},
                {"fieldname": "caller", "label": "Caller", "fieldtype": "Link", "options": "User"},
                {"fieldname": "contact_email", "label": "Contact Email", "fieldtype": "Data", "options": "Email"},
                {"fieldname": "contact_phone", "label": "Contact Phone", "fieldtype": "Data", "options": "Phone"},
                
                {"fieldname": "assignment_section", "label": "Assignment", "fieldtype": "Section Break"},
                {"fieldname": "assigned_team", "label": "Assigned Team", "fieldtype": "Link", "options": "ITSM Team"},
                {"fieldname": "assigned_to", "label": "Assigned To", "fieldtype": "Link", "options": "User"},
                {"fieldname": "is_major_incident", "label": "Is Major Incident", "fieldtype": "Check"},
                {"fieldname": "major_incident_manager", "label": "Major Incident Manager", "fieldtype": "Link", "options": "User", "depends_on": "eval:doc.is_major_incident==1"},
                {"fieldname": "parent_incident", "label": "Parent Incident", "fieldtype": "Link", "options": "ITSM Incident"},
                
                {"fieldname": "resolution_section", "label": "Resolution & Links", "fieldtype": "Section Break"},
                {"fieldname": "workaround", "label": "Workaround", "fieldtype": "Text Editor"},
                {"fieldname": "resolution_code", "label": "Resolution Code", "fieldtype": "Link", "options": "ITSM Resolution Code", "depends_on": "eval:doc.status=='Resolved' || doc.status=='Closed'"},
                {"fieldname": "resolution_notes", "label": "Resolution Notes", "fieldtype": "Text Editor", "depends_on": "eval:doc.status=='Resolved' || doc.status=='Closed'"},
                {"fieldname": "reopened_count", "label": "Reopened Count", "fieldtype": "Int", "read_only": 1},
                
                {"fieldname": "sla_section", "label": "SLA & Metrics", "fieldtype": "Section Break"},
                {"fieldname": "sla_status", "label": "SLA Status", "fieldtype": "Select", "options": "Within SLA\nAt Risk\nBreached\nPaused\nFulfilled", "read_only": 1},
                {"fieldname": "response_due", "label": "Response Due", "fieldtype": "Datetime", "read_only": 1},
                {"fieldname": "resolution_due", "label": "Resolution Due", "fieldtype": "Datetime", "read_only": 1},
                {"fieldname": "first_response_at", "label": "First Response At", "fieldtype": "Datetime", "read_only": 1},
                {"fieldname": "resolution_at", "label": "Resolved At", "fieldtype": "Datetime", "read_only": 1},
                {"fieldname": "closed_at", "label": "Closed At", "fieldtype": "Datetime", "read_only": 1},
                {"fieldname": "on_hold_reason", "label": "On Hold Reason", "fieldtype": "Select", "options": "Awaiting User\nAwaiting Vendor\nAwaiting Change\nScheduled Maintenance\nOther", "depends_on": "eval:doc.status=='Pending'"},
                {"fieldname": "on_hold_since", "label": "On Hold Since", "fieldtype": "Datetime", "read_only": 1},
                {"fieldname": "csat_sent", "label": "CSAT Sent", "fieldtype": "Check", "read_only": 1},
                {"fieldname": "csat_score", "label": "CSAT Score", "fieldtype": "Select", "options": "\n1\n2\n3\n4\n5", "read_only": 1},
                
                {"fieldname": "tables_section", "label": "Watch List & CIs", "fieldtype": "Section Break"},
                {"fieldname": "watch_list", "label": "Watch List", "fieldtype": "Table", "options": "ITSM Watch List"},
                {"fieldname": "linked_cis", "label": "Linked CIs", "fieldtype": "Table", "options": "ITSM Incident CI"},
                
                {"fieldname": "custom_fields_section", "label": "Custom Fields", "fieldtype": "Section Break"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Agent", "read": 1, "write": 1, "create": 1},
                {"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "ITSM Employee", "read": 1, "create": 1}
            ]
        }
    ]

    for dt in doctypes:
        if not frappe.db.exists("DocType", dt["name"]):
            doc = frappe.get_doc(dt)
            doc.insert()
            print(f"Created DocType {dt['name']}")
        else:
            print(f"DocType {dt['name']} already exists")
    
    frappe.db.commit()
