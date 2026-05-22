import frappe

def create_doctypes():
    doctypes = [
        {
            "doctype": "DocType",
            "name": "ITSM Category",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:category_name",
            "fields": [
                {"fieldname": "category_name", "label": "Category Name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "description", "label": "Description", "fieldtype": "Text"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Sub Category",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:sub_category_name",
            "fields": [
                {"fieldname": "sub_category_name", "label": "Sub Category Name", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "category", "label": "Category", "fieldtype": "Link", "options": "ITSM Category", "reqd": 1},
                {"fieldname": "description", "label": "Description", "fieldtype": "Text"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Team",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:team_name",
            "fields": [
                {"fieldname": "team_name", "label": "Team Name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "department", "label": "Department", "fieldtype": "Link", "options": "Department"},
                {"fieldname": "description", "label": "Description", "fieldtype": "Text"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Location",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:location_name",
            "fields": [
                {"fieldname": "location_name", "label": "Location Name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "address", "label": "Address", "fieldtype": "Text"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        },
        {
            "doctype": "DocType",
            "name": "ITSM Tag",
            "module": "Frappe ITSM",
            "custom": 0,
            "autoname": "field:tag_name",
            "fields": [
                {"fieldname": "tag_name", "label": "Tag Name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "color", "label": "Color", "fieldtype": "Color"}
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
            print(f"DocType {dt['name']} already exists")
    
    frappe.db.commit()


def seed_data():
    # Insert ITSM Category
    for cat in ["Hardware", "Software", "Network", "Database", "Cloud"]:
        if not frappe.db.exists("ITSM Category", cat):
            frappe.get_doc({"doctype": "ITSM Category", "category_name": cat}).insert(ignore_permissions=True)
            print(f"Created category {cat}")

    # Insert Company if missing
    if not frappe.db.exists("Company", "Mindgraph Technologies Pvt Ltd"):
        frappe.get_doc({"doctype": "Company", "company_name": "Mindgraph Technologies Pvt Ltd", "default_currency": "USD"}).insert(ignore_permissions=True)

    frappe.db.commit()


