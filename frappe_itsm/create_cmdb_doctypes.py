import frappe

def create_doctypes():
	doctypes = [
		{
			"doctype": "DocType",
			"name": "ITSM CI",
			"module": "Frappe ITSM",
			"custom": 1,
			"autoname": "field:ci_name",
			"naming_rule": "By fieldname",
			"permissions": [
				{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Agent", "read": 1, "write": 1, "create": 1},
				{"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
			],
			"fields": [
				{"fieldname": "ci_name", "fieldtype": "Data", "label": "CI Name", "reqd": 1, "unique": 1, "in_list_view": 1},
				{"fieldname": "ci_type", "fieldtype": "Select", "label": "CI Type", "options": "Hardware\nVM\nNetwork\nDatabase\nApplication\nCloud Resource", "reqd": 1, "in_list_view": 1},
				{"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Active\nInactive\nStale\nRetired", "default": "Active", "in_list_view": 1},
				{"fieldname": "ip_address", "fieldtype": "Data", "label": "IP Address"},
				{"fieldname": "ci_owner", "fieldtype": "Link", "label": "Owner", "options": "User"},
				{"fieldname": "description", "fieldtype": "Small Text", "label": "Description"}
			]
		},
		{
			"doctype": "DocType",
			"name": "ITSM CI Relationship",
			"module": "Frappe ITSM",
			"custom": 1,
			"autoname": "naming_series:",
			"permissions": [
				{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Agent", "read": 1, "write": 1, "create": 1},
				{"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
			],
			"fields": [
				{"fieldname": "naming_series", "fieldtype": "Select", "label": "Naming Series", "options": "CIR-.#####", "default": "CIR-.#####", "hidden": 1},
				{"fieldname": "parent_ci", "fieldtype": "Link", "label": "Parent CI (Dependent)", "options": "ITSM CI", "reqd": 1, "in_list_view": 1},
				{"fieldname": "relationship_type", "fieldtype": "Select", "label": "Relationship Type", "options": "Runs On\nDepends On\nConnects To\nHoused In", "reqd": 1, "in_list_view": 1},
				{"fieldname": "child_ci", "fieldtype": "Link", "label": "Child CI (Dependency)", "options": "ITSM CI", "reqd": 1, "in_list_view": 1}
			]
		}
	]

	for d in doctypes:
		if not frappe.db.exists("DocType", d["name"]):
			doc = frappe.get_doc(d)
			doc.insert(ignore_permissions=True)
			print(f"Created DocType {d['name']}")
		else:
			doc = frappe.get_doc("DocType", d["name"])
			doc.fields = []
			for f in d.get("fields", []):
				doc.append("fields", f)
			doc.permissions = []
			for p in d.get("permissions", []):
				doc.append("permissions", p)
			doc.save(ignore_permissions=True)
			print(f"Updated DocType {d['name']}")
			
	frappe.db.commit()
