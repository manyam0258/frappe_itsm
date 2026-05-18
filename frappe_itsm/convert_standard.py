import frappe

def convert_to_standard():
    doctypes = [
        "ITSM Problem", "ITSM Problem Task", "ITSM Problem Incident",
        "ITSM Change", "ITSM Change Task", "ITSM Change Risk Question", 
        "ITSM Blackout Window", "ITSM CAB Member", "ITSM CAB Agenda Item", "ITSM CAB Meeting"
    ]
    for d in doctypes:
        doc = frappe.get_doc("DocType", d)
        doc.custom = 0
        doc.save(ignore_permissions=True)
    
    # Export them to generate the files
    from frappe.modules.export_file import export_to_files
    export_to_files(record_list=[['DocType', d] for d in doctypes], record_module='Frappe ITSM')
    print("Converted and exported to standard")
