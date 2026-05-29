# Copyright (c) 2026, Product Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.workflow import get_workflow_name
from frappe.automation.doctype.assignment_rule.assignment_rule import apply

def notify_assignee(doc, assignee):
	try:
		if not assignee:
			return
		
		# Check if the assignee has changed to avoid duplicate emails
		db_assigned_to = doc.get_db_value("assigned_to")
		if db_assigned_to == assignee:
			return

		subject = f"Assigned: {doc.doctype} {doc.name or doc.title}"
		content = f"""
		<p>Hello,</p>
		<p>You have been assigned to the following {doc.doctype}:</p>
		<p><b>ID:</b> {doc.name or 'New'}</p>
		<p><b>Title:</b> {doc.title}</p>
		<p><b>State:</b> {doc.workflow_state or doc.status}</p>
		<p>Please log in to the portal to review and update the ticket.</p>
		"""
		frappe.sendmail(
			recipients=[assignee],
			subject=subject,
			message=content,
			reference_doctype=doc.doctype,
			reference_name=doc.name
		)
	except Exception as e:
		frappe.log_error(f"Error in notify_assignee: {str(e)}", "ITSM Assignment Notification")

def handle_workflow_assignments(doc, method):
	# 1. Dynamically find active Workflow and its state field
	workflow_name = get_workflow_name(doc.doctype)
	if not workflow_name:
		return

	workflow = frappe.get_cached_doc("Workflow", workflow_name)
	state_field = workflow.workflow_state_field or "workflow_state"

	# 2. Run if the workflow state or assigned_team has changed
	if not doc.has_value_changed(state_field) and not doc.has_value_changed("assigned_team"):
		return

	# 3. Cancel existing open assignments instead of deleting them (preserves ITIL audit trail)
	# Using "Cancelled" ensures they are excluded from native active assignments check,
	# allowing new rules to trigger, while preserving the ToDo record in the DB.
	frappe.db.set_value(
		"ToDo",
		{
			"reference_type": doc.doctype,
			"reference_name": doc.name,
			"status": "Open"
		},
		"status",
		"Cancelled"
	)

	# 4. Trigger the native assignment engine to apply rules for the new state
	apply(doc)

	# 5. Capture the assigned user from the open ToDo and update the doc
	todo_user = frappe.db.get_value(
		"ToDo",
		{
			"reference_type": doc.doctype,
			"reference_name": doc.name,
			"status": "Open"
		},
		"allocated_to"
	)
	if todo_user:
		doc.assigned_to = todo_user
		notify_assignee(doc, todo_user)
