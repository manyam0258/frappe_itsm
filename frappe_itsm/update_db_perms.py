import frappe

def run():
    print("Running permissions update...")
    
    # 1. ITSM Problem Permissions
    problem_perms = [
        {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Agent", "read": 1, "write": 1, "create": 1, "delete": 0, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Senior Agent", "read": 1, "write": 1, "create": 1, "delete": 0, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1}
    ]
    update_permissions("ITSM Problem", problem_perms)

    # 2. ITSM Change Permissions
    change_perms = [
        {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Agent", "read": 1, "write": 1, "create": 1, "delete": 0, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Change Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1}
    ]
    update_permissions("ITSM Change", change_perms)

    # 3. ITSM CAB Meeting Permissions
    cab_perms = [
        {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Agent", "read": 1, "write": 1, "create": 1, "delete": 0, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Change Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM CAB Member", "read": 1, "write": 1, "create": 0, "delete": 0, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1}
    ]
    update_permissions("ITSM CAB Meeting", cab_perms)

    # 4. ITSM Blackout Window Permissions
    blackout_perms = [
        {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Agent", "read": 1, "write": 0, "create": 0, "delete": 0, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Change Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1},
        {"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "report": 1, "share": 1}
    ]
    update_permissions("ITSM Blackout Window", blackout_perms)

    frappe.db.commit()
    print("Permissions successfully updated in database!")

def update_permissions(doctype_name, perm_list):
    if frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc("DocType", doctype_name)
        doc.permissions = []
        for p in perm_list:
            doc.append("permissions", p)
        doc.save(ignore_permissions=True)
        print(f"Updated permissions for {doctype_name}")
    else:
        print(f"DocType {doctype_name} does not exist!")
