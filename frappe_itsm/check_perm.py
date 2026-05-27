import frappe

def check():
    p = frappe.get_doc("DocType", "ITSM Problem")
    print("Permissions for ITSM Problem:")
    for perm in p.permissions:
        print(f"Role: {perm.role}, Read: {perm.read}, Write: {perm.write}, Create: {perm.create}, Delete: {perm.delete}")
