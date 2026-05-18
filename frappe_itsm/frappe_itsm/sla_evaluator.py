import frappe
from frappe.utils import now_datetime, get_datetime

@frappe.whitelist()
def evaluate_slas():
    """Background job to evaluate SLA status for open SLAs"""
    active_slas = frappe.get_all("ITSM SLA Instance", filters={"sla_status": ["in", ["Within SLA", "At Risk", "Paused"]]}, fields=["name", "document_type", "document_name", "response_due", "resolution_due", "sla_status"])
    
    now = now_datetime()
    
    for sla in active_slas:
        try:
            doc = frappe.get_doc(sla.document_type, sla.document_name)
            # Evaluate Response Due
            if not doc.first_response_at and sla.response_due and get_datetime(sla.response_due) < now:
                update_sla_status(sla.name, "Breached")
                continue
                
            # Evaluate Resolution Due
            if not doc.resolution_at and sla.resolution_due and get_datetime(sla.resolution_due) < now:
                update_sla_status(sla.name, "Breached")
                continue
            
            # TODO: Implement At Risk calculation and Escalation Triggering
        except Exception as e:
            frappe.log_error(title="SLA Evaluator Error", message=str(e))

def update_sla_status(sla_name, status):
    frappe.db.set_value("ITSM SLA Instance", sla_name, "sla_status", status)

def calculate_sla_due(start_time, duration_mins, working_hours_name, holiday_list_name=None):
    """Calculates due date based on working hours and holidays."""
    # Placeholder for business hours calculation logic
    # Real implementation would use frappe.utils.add_to_date or custom working hours logic
    import datetime
    return get_datetime(start_time) + datetime.timedelta(minutes=duration_mins)

