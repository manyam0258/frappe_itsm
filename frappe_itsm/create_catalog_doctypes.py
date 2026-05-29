import frappe

def create_doctypes():
	doctypes = [
		{
			"doctype": "DocType",
			"name": "ITSM Catalog Item",
			"module": "Frappe ITSM",
			"custom": 1,
			"autoname": "field:item_name",
			"naming_rule": "By fieldname",
			"permissions": [
				{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Agent", "read": 1, "write": 1, "create": 1},
				{"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Employee", "read": 1},
				{"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
			],
			"fields": [
				{"fieldname": "item_name", "fieldtype": "Data", "label": "Item Name", "reqd": 1, "unique": 1, "in_list_view": 1},
				{"fieldname": "category", "fieldtype": "Link", "label": "Category", "options": "ITSM Category", "reqd": 1, "in_list_view": 1},
				{"fieldname": "cost", "fieldtype": "Currency", "label": "Cost (USD)", "default": 0},
				{"fieldname": "description", "fieldtype": "Text Editor", "label": "Description"}
			]
		},
		{
			"doctype": "DocType",
			"name": "ITSM Request Item",
			"module": "Frappe ITSM",
			"custom": 1,
			"autoname": "RITM-.YYYY.-.#####",
			"naming_rule": "Expression",
			"permissions": [
				{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Agent", "read": 1, "write": 1, "create": 1},
				{"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Employee", "read": 1, "create": 1},
				{"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
			],
			"fields": [
				{"fieldname": "catalog_item", "fieldtype": "Link", "label": "Requested Item", "options": "ITSM Catalog Item", "reqd": 1, "in_list_view": 1},
				{"fieldname": "requester", "fieldtype": "Link", "label": "Requester", "options": "User", "reqd": 1, "default": "session_user", "in_list_view": 1},
				{"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Pending Approval\nApproved\nFulfilling\nClosed", "default": "Pending Approval", "in_list_view": 1},
				{"fieldname": "quantity", "fieldtype": "Int", "label": "Quantity", "default": 1, "reqd": 1},
				{"fieldname": "cost", "fieldtype": "Currency", "label": "Estimated Cost", "read_only": 1}
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
