import frappe

def create_doctypes():
    doctypes = [
        {
            "doctype": "DocType",
            "name": "ITSM Working Hours",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:schedule_name",
            "fields": [
                {"fieldname": "schedule_name", "label": "Schedule Name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "timezone", "label": "Timezone", "fieldtype": "Data", "default": "UTC"},
                {"fieldname": "monday_start", "label": "Monday Start", "fieldtype": "Time", "default": "09:00:00"},
                {"fieldname": "monday_end", "label": "Monday End", "fieldtype": "Time", "default": "17:00:00"},
                {"fieldname": "tuesday_start", "label": "Tuesday Start", "fieldtype": "Time", "default": "09:00:00"},
                {"fieldname": "tuesday_end", "label": "Tuesday End", "fieldtype": "Time", "default": "17:00:00"},
                {"fieldname": "wednesday_start", "label": "Wednesday Start", "fieldtype": "Time", "default": "09:00:00"},
                {"fieldname": "wednesday_end", "label": "Wednesday End", "fieldtype": "Time", "default": "17:00:00"},
                {"fieldname": "thursday_start", "label": "Thursday Start", "fieldtype": "Time", "default": "09:00:00"},
                {"fieldname": "thursday_end", "label": "Thursday End", "fieldtype": "Time", "default": "17:00:00"},
                {"fieldname": "friday_start", "label": "Friday Start", "fieldtype": "Time", "default": "09:00:00"},
                {"fieldname": "friday_end", "label": "Friday End", "fieldtype": "Time", "default": "17:00:00"},
                {"fieldname": "saturday_start", "label": "Saturday Start", "fieldtype": "Time"},
                {"fieldname": "saturday_end", "label": "Saturday End", "fieldtype": "Time"},
                {"fieldname": "sunday_start", "label": "Sunday Start", "fieldtype": "Time"},
                {"fieldname": "sunday_end", "label": "Sunday End", "fieldtype": "Time"},
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Holiday",
            "module": "Frappe ITSM",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "holiday_date", "label": "Date", "fieldtype": "Date", "reqd": 1},
                {"fieldname": "description", "label": "Description", "fieldtype": "Data"}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Holiday List",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:list_name",
            "fields": [
                {"fieldname": "list_name", "label": "List Name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "holidays", "label": "Holidays", "fieldtype": "Table", "options": "ITSM Holiday"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM SLA Condition",
            "module": "Frappe ITSM",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "field", "label": "Field", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "operator", "label": "Operator", "fieldtype": "Select", "options": "=\n!=\n>\n<\n>=\n<=\nin\nnot in", "reqd": 1},
                {"fieldname": "value", "label": "Value", "fieldtype": "Data", "reqd": 1}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM SLA Target",
            "module": "Frappe ITSM",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "priority", "label": "Priority", "fieldtype": "Select", "options": "P1-Critical\nP2-High\nP3-Moderate\nP4-Low\nP5-Planning", "reqd": 1},
                {"fieldname": "response_time_mins", "label": "Response Time (mins)", "fieldtype": "Int", "reqd": 1},
                {"fieldname": "resolution_time_mins", "label": "Resolution Time (mins)", "fieldtype": "Int", "reqd": 1}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM SLA Escalation",
            "module": "Frappe ITSM",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "trigger_at_percent", "label": "Trigger At (% of SLA)", "fieldtype": "Int", "reqd": 1},
                {"fieldname": "action", "label": "Action", "fieldtype": "Select", "options": "Notify Only\nReassign + Notify\nEscalate Priority\nEscalate Priority + Reassign", "reqd": 1},
                {"fieldname": "notify_roles", "label": "Notify Roles", "fieldtype": "Text", "description": "Comma separated roles"},
                {"fieldname": "notify_users", "label": "Notify Users", "fieldtype": "Text", "description": "Comma separated user emails"},
                {"fieldname": "reassign_to_team", "label": "Reassign To Team", "fieldtype": "Link", "options": "ITSM Team"},
                {"fieldname": "priority_upgrade", "label": "Upgrade Priority To", "fieldtype": "Select", "options": "P1-Critical\nP2-High\nP3-Moderate"}
            ]
        },
        {
            "doctype": "DocType",
            "name": "ITSM SLA Policy",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:policy_name",
            "fields": [
                {"fieldname": "policy_name", "label": "Policy Name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "document_type", "label": "Applies To", "fieldtype": "Select", "options": "ITSM Incident\nITSM Service Request\nITSM Change", "reqd": 1, "default": "ITSM Incident"},
                {"fieldname": "is_default", "label": "Is Default", "fieldtype": "Check"},
                {"fieldname": "working_hours", "label": "Working Hours", "fieldtype": "Link", "options": "ITSM Working Hours", "reqd": 1},
                {"fieldname": "holiday_list", "label": "Holiday List", "fieldtype": "Link", "options": "ITSM Holiday List"},
                
                {"fieldname": "conditions_section", "label": "Conditions", "fieldtype": "Section Break"},
                {"fieldname": "conditions", "label": "Conditions", "fieldtype": "Table", "options": "ITSM SLA Condition"},
                
                {"fieldname": "targets_section", "label": "Targets", "fieldtype": "Section Break"},
                {"fieldname": "targets", "label": "SLA Targets", "fieldtype": "Table", "options": "ITSM SLA Target"},
                
                {"fieldname": "escalations_section", "label": "Escalation Rules", "fieldtype": "Section Break"},
                {"fieldname": "escalation_rules", "label": "Escalation Rules", "fieldtype": "Table", "options": "ITSM SLA Escalation"},
                
                {"fieldname": "statuses_section", "label": "Status Configuration", "fieldtype": "Section Break"},
                {"fieldname": "pause_statuses", "label": "Pause on Status", "fieldtype": "Text", "description": "Comma separated list of statuses where SLA should pause (e.g., Pending)"},
                {"fieldname": "fulfilled_statuses", "label": "Fulfilled on Status", "fieldtype": "Text", "description": "Comma separated list of statuses where SLA is fulfilled (e.g., Resolved, Closed)"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM SLA Instance",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "naming_series:",
            "fields": [
                {"fieldname": "naming_series", "label": "Naming Series", "fieldtype": "Select", "options": "SLA-.YYYY.-.#####", "default": "SLA-.YYYY.-.#####", "hidden": 1},
                {"fieldname": "document_type", "label": "Document Type", "fieldtype": "Link", "options": "DocType", "read_only": 1},
                {"fieldname": "document_name", "label": "Document Name", "fieldtype": "Dynamic Link", "options": "document_type", "read_only": 1},
                {"fieldname": "sla_policy", "label": "SLA Policy", "fieldtype": "Link", "options": "ITSM SLA Policy", "read_only": 1},
                {"fieldname": "priority", "label": "Priority", "fieldtype": "Data", "read_only": 1},
                {"fieldname": "start_time", "label": "Start Time", "fieldtype": "Datetime", "read_only": 1},
                {"fieldname": "response_due", "label": "Response Due", "fieldtype": "Datetime", "read_only": 1},
                {"fieldname": "resolution_due", "label": "Resolution Due", "fieldtype": "Datetime", "read_only": 1},
                {"fieldname": "sla_status", "label": "SLA Status", "fieldtype": "Select", "options": "Within SLA\nAt Risk\nBreached\nPaused\nFulfilled", "read_only": 1},
                {"fieldname": "hold_duration", "label": "Hold Duration (mins)", "fieldtype": "Float", "read_only": 1},
                {"fieldname": "triggered_escalations", "label": "Triggered Escalations", "fieldtype": "Small Text", "read_only": 1}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM SLA Hold Log",
            "module": "Frappe ITSM",
            "custom": 0,
            "fields": [
                {"fieldname": "sla_instance", "label": "SLA Instance", "fieldtype": "Link", "options": "ITSM SLA Instance", "reqd": 1},
                {"fieldname": "hold_start", "label": "Hold Start", "fieldtype": "Datetime", "reqd": 1},
                {"fieldname": "hold_end", "label": "Hold End", "fieldtype": "Datetime"},
                {"fieldname": "duration_mins", "label": "Duration (mins)", "fieldtype": "Float", "read_only": 1}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        }
    ]

    for dt in doctypes:
        if not frappe.db.exists("DocType", dt["name"]):
            doc = frappe.get_doc(dt)
            doc.insert()
            print(f"Created DocType {dt['name']}")
        else:
            doc = frappe.get_doc("DocType", dt["name"])
            doc.fields = []
            for f in dt.get("fields", []):
                doc.append("fields", f)
            doc.permissions = []
            for p in dt.get("permissions", []):
                doc.append("permissions", p)
            doc.save(ignore_permissions=True)
            print(f"Updated DocType {dt['name']}")
    
    frappe.db.commit()
