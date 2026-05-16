import frappe

def create_roles():
    roles = [
        {"role_name": "ITSM Super Admin", "desk_access": 1},
        {"role_name": "ITSM Admin", "desk_access": 1},
        {"role_name": "ITSM Manager", "desk_access": 1},
        {"role_name": "ITSM Change Manager", "desk_access": 1},
        {"role_name": "ITSM CAB Member", "desk_access": 1},
        {"role_name": "ITSM Senior Agent", "desk_access": 1},
        {"role_name": "ITSM Agent", "desk_access": 1},
        {"role_name": "ITSM Knowledge Author", "desk_access": 1},
        {"role_name": "ITSM Field Tech", "desk_access": 1},
        {"role_name": "ITSM Employee", "desk_access": 1},
        {"role_name": "ITSM Customer", "desk_access": 1},
        {"role_name": "ITSM Vendor", "desk_access": 1},
        {"role_name": "ITSM Report Viewer", "desk_access": 1}
    ]

    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.role_name = role_data["role_name"]
            role.desk_access = role_data["desk_access"]
            role.insert(ignore_permissions=True)
            print(f"Created Role: {role_data['role_name']}")
        else:
            print(f"Role already exists: {role_data['role_name']}")
    
    frappe.db.commit()
