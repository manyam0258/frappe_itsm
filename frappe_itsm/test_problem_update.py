import frappe

def run():
    workflow_name = frappe.db.get_value("Workflow", {"document_type": "ITSM Problem"}, "name")
    print(f"Workflow for ITSM Problem: {workflow_name}")
    if workflow_name:
        workflow = frappe.get_doc("Workflow", workflow_name)
        print("States:")
        for state in workflow.states:
            print(f"  - {state.state} (Status: {state.doc_status})")
        print("Transitions:")
        for t in workflow.transitions:
            print(f"  - {t.state} -> {t.action} -> {t.next_state} (Allowed Role: {t.allowed})")
    else:
        print("No workflow found for ITSM Problem.")
