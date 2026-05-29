import frappe
from frappe.utils import now_datetime, get_datetime
import datetime
import pytz

@frappe.whitelist()
def evaluate_slas():
	"""Background job to evaluate SLA status for open SLAs"""
	active_slas = frappe.get_all(
		"ITSM SLA Instance",
		filters={"sla_status": ["in", ["Within SLA", "At Risk", "Paused"]]},
		fields=["name", "document_type", "document_name", "sla_policy", "priority", "start_time", "response_due", "resolution_due", "sla_status", "triggered_escalations", "hold_duration"]
	)
	
	now = now_datetime()
	
	for sla in active_slas:
		try:
			doc = frappe.get_doc(sla.document_type, sla.document_name)
			policy = frappe.get_doc("ITSM SLA Policy", sla.sla_policy)
			pause_statuses = [s.strip() for s in (policy.pause_statuses or "").split(",") if s.strip()]
			fulfilled_statuses = [s.strip() for s in (policy.fulfilled_statuses or "").split(",") if s.strip()]
			
			# 1. Check if fulfilled
			if doc.status in fulfilled_statuses:
				frappe.db.set_value("ITSM SLA Instance", sla.name, {
					"sla_status": "Fulfilled",
					"closed_at": now
				})
				continue
				
			# 2. Check if paused
			if doc.status in pause_statuses:
				if sla.sla_status != "Paused":
					# Mark active SLA as Paused
					frappe.db.set_value("ITSM SLA Instance", sla.name, "sla_status", "Paused")
					# Create Hold Log entry
					frappe.get_doc({
						"doctype": "ITSM SLA Hold Log",
						"sla_instance": sla.name,
						"hold_start": now
					}).insert(ignore_permissions=True)
				continue
			else:
				if sla.sla_status == "Paused":
					# Resumed! Close latest open Hold Log
					hold_logs = frappe.get_all(
						"ITSM SLA Hold Log",
						filters={"sla_instance": sla.name, "hold_end": ["is", "not set"]},
						fields=["name", "hold_start"]
					)
					duration = 0
					for log in hold_logs:
						start = get_datetime(log.hold_start)
						duration = (now - start).total_seconds() / 60.0
						frappe.db.set_value("ITSM SLA Hold Log", log.name, {
							"hold_end": now,
							"duration_mins": duration
						})
					
					# Add duration to SLA instance hold duration
					hold_duration = frappe.db.get_value("ITSM SLA Instance", sla.name, "hold_duration") or 0.0
					new_hold_duration = hold_duration + duration
					
					# Re-calculate due dates (postpone by the pause duration)
					new_response_due = get_datetime(sla.response_due) + datetime.timedelta(minutes=duration) if sla.response_due else None
					new_resolution_due = get_datetime(sla.resolution_due) + datetime.timedelta(minutes=duration) if sla.resolution_due else None
					
					frappe.db.set_value("ITSM SLA Instance", sla.name, {
						"sla_status": "Within SLA",
						"hold_duration": new_hold_duration,
						"response_due": new_response_due,
						"resolution_due": new_resolution_due
					})
					
					# Refresh local variables for evaluation
					sla.response_due = new_response_due
					sla.resolution_due = new_resolution_due
					sla.sla_status = "Within SLA"
			
			# 3. Evaluate targets
			response_breached = False
			if not getattr(doc, "first_response_at", None) and sla.response_due:
				response_due = get_datetime(sla.response_due)
				if response_due < now:
					update_sla_status(sla.name, "Breached")
					response_breached = True
					
			resolution_breached = False
			if not getattr(doc, "resolution_at", None) and sla.resolution_due and not response_breached:
				resolution_due = get_datetime(sla.resolution_due)
				if resolution_due < now:
					update_sla_status(sla.name, "Breached")
					resolution_breached = True
					
			if response_breached or resolution_breached:
				# Trigger 100% breach escalations
				trigger_sla_escalations(sla, policy, doc, 100)
				continue
				
			# Calculate elapsed percentage
			start = get_datetime(sla.start_time)
			due = get_datetime(sla.resolution_due or sla.response_due)
			if due and start and due > start:
				total_duration = (due - start).total_seconds()
				elapsed = (now - start).total_seconds()
				percent = (elapsed / total_duration) * 100.0
				
				# Update status to "At Risk" if > 75%
				if percent >= 75.0 and sla.sla_status != "At Risk":
					frappe.db.set_value("ITSM SLA Instance", sla.name, "sla_status", "At Risk")
					
				# Evaluate and trigger escalations based on percent
				for threshold in [50, 75]:
					if percent >= threshold:
						trigger_sla_escalations(sla, policy, doc, threshold)
						
		except Exception as e:
			frappe.log_error(title="SLA Evaluator Error", message=str(e))

def update_sla_status(sla_name, status):
	frappe.db.set_value("ITSM SLA Instance", sla_name, "sla_status", status)

@frappe.whitelist()
def calculate_sla_due(start_time, duration_mins, working_hours_name, holiday_list_name=None):
	"""Calculates due date based on working hours and holidays."""
	start_dt = get_datetime(start_time)
	duration_mins = int(duration_mins)
	
	if not working_hours_name or not frappe.db.exists("ITSM Working Hours", working_hours_name):
		# Fallback to standard time if no schedule config is found
		return start_dt + datetime.timedelta(minutes=duration_mins)

	working_hours = frappe.get_doc("ITSM Working Hours", working_hours_name)
	tz_name = working_hours.timezone or "UTC"
	tz = pytz.timezone(tz_name)
	
	# Ensure start_dt is timezone-aware in local timezone
	if not start_dt.tzinfo:
		start_dt = pytz.utc.localize(start_dt)
	local_start = start_dt.astimezone(tz)
	
	# Load holidays
	holidays = set()
	if holiday_list_name and frappe.db.exists("ITSM Holiday List", holiday_list_name):
		h_list = frappe.get_doc("ITSM Holiday List", holiday_list_name)
		for h in h_list.holidays:
			holidays.add(h.holiday_date)
			
	def is_holiday(dt):
		return dt.date() in holidays
		
	def get_working_times_for_day(dt):
		weekday = dt.strftime("%A").lower()
		start_field = f"{weekday}_start"
		end_field = f"{weekday}_end"
		
		start_val = getattr(working_hours, start_field, None)
		end_val = getattr(working_hours, end_field, None)
		
		if not start_val or not end_val:
			return None, None
			
		def convert_to_time(val):
			if isinstance(val, str):
				sh, sm, ss = map(int, val.split(":"))
				return datetime.time(sh, sm, ss)
			elif isinstance(val, datetime.timedelta):
				tot_sec = int(val.total_seconds())
				sh = tot_sec // 3600
				sm = (tot_sec % 3600) // 60
				ss = tot_sec % 60
				return datetime.time(sh, sm, ss)
			elif isinstance(val, datetime.time):
				return val
			return val

		start_time_obj = convert_to_time(start_val)
		end_time_obj = convert_to_time(end_val)
			
		day_start = tz.localize(datetime.datetime.combine(dt.date(), start_time_obj))
		day_end = tz.localize(datetime.datetime.combine(dt.date(), end_time_obj))
		return day_start, day_end


	current_dt = local_start
	remaining_mins = duration_mins
	safety = 0
	
	while remaining_mins > 0 and safety < 1000:
		safety += 1
		
		if is_holiday(current_dt):
			current_dt = tz.localize(datetime.datetime.combine(current_dt.date() + datetime.timedelta(days=1), datetime.time(0, 0)))
			continue
			
		day_start, day_end = get_working_times_for_day(current_dt)
		if not day_start or not day_end or day_start >= day_end:
			current_dt = tz.localize(datetime.datetime.combine(current_dt.date() + datetime.timedelta(days=1), datetime.time(0, 0)))
			continue
			
		if current_dt < day_start:
			current_dt = day_start
			
		if current_dt >= day_end:
			current_dt = tz.localize(datetime.datetime.combine(current_dt.date() + datetime.timedelta(days=1), datetime.time(0, 0)))
			continue
			
		available_mins = (day_end - current_dt).total_seconds() / 60.0
		
		if remaining_mins <= available_mins:
			result_dt = current_dt + datetime.timedelta(minutes=remaining_mins)
			return result_dt.astimezone(pytz.utc).replace(tzinfo=None)
		else:
			remaining_mins -= available_mins
			current_dt = tz.localize(datetime.datetime.combine(current_dt.date() + datetime.timedelta(days=1), datetime.time(0, 0)))
			
	return start_dt.astimezone(pytz.utc).replace(tzinfo=None) + datetime.timedelta(minutes=duration_mins)

def trigger_sla_escalations(sla, policy, doc, threshold):
	triggered = [t.strip() for t in (sla.triggered_escalations or "").split(",") if t.strip()]
	if str(threshold) in triggered:
		return
		
	rules = [r for r in policy.escalation_rules if r.trigger_at_percent == threshold]
	if not rules:
		return
		
	for rule in rules:
		if "Notify" in rule.action:
			recipients = []
			if rule.notify_users:
				recipients.extend([u.strip() for u in rule.notify_users.split(",") if u.strip()])
			if rule.notify_roles:
				roles = [r.strip() for r in rule.notify_roles.split(",") if r.strip()]
				users_with_roles = frappe.get_all(
					"Has Role",
					filters={"role": ["in", roles]},
					fields=["parent"]
				)
				recipients.extend([u.parent for u in users_with_roles])
				
			if recipients:
				subject = f"SLA ALERT: {doc.doctype} {doc.name} has reached {threshold}% of SLA target"
				message = f"""
				<h3>SLA Escalation Triggered</h3>
				<p>The document <strong>{doc.doctype} {doc.name}</strong> ({doc.title}) has reached <strong>{threshold}%</strong> of its SLA limit.</p>
				<p><strong>Priority:</strong> {doc.priority}</p>
				<p><strong>Status:</strong> {doc.status}</p>
				<p><a href="{frappe.utils.get_url_to_form(doc.doctype, doc.name)}">Open Document</a></p>
				"""
				frappe.sendmail(
					recipients=recipients,
					subject=subject,
					message=message,
					delayed=False
				)
				
		if "Reassign" in rule.action and rule.reassign_to_team:
			doc.assigned_team = rule.reassign_to_team
			doc.save(ignore_permissions=True)
			frappe.msgprint(f"SLA Escalation: Reassigned to Team {rule.reassign_to_team}", alert=True)
			
		if "Escalate Priority" in rule.action and rule.priority_upgrade:
			doc.priority = rule.priority_upgrade
			doc.save(ignore_permissions=True)
			frappe.msgprint(f"SLA Escalation: Upgraded Priority to {rule.priority_upgrade}", alert=True)
			
	triggered.append(str(threshold))
	frappe.db.set_value("ITSM SLA Instance", sla.name, "triggered_escalations", ",".join(triggered))
