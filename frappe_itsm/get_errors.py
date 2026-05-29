import frappe
import traceback
from frappe_itsm.frappe_itsm.doctype.itsm_cab_meeting.itsm_cab_meeting import record_cab_vote, get_signed_vote_token

def run():
	# Ensure User exists
	userEmail = 'pw_test_user_1@example.com'
	if not frappe.db.exists("User", userEmail):
		u = frappe.get_doc({
			"doctype": "User",
			"email": userEmail,
			"first_name": "PW_TEST_USER_1",
			"send_welcome_email": 0
		})
		u.insert(ignore_permissions=True)
		u.append("roles", {"role": "ITSM Agent"})
		u.save(ignore_permissions=True)

	# Ensure Change exists
	chg = frappe.get_doc({
		"doctype": "ITSM Change",
		"title": "PW_TEST CAB Change",
		"change_type": "Normal",
		"priority": "Medium",
		"risk_level": "Low",
		"impact": "4-Individual",
		"category": "Software",
		"change_initiator": "Administrator",
		"change_owner": "Administrator",
		"assigned_team": "IT Service Desk",
		"description": "Testing CAB voting",
		"justification": "None",
		"implementation_plan": "None",
		"start_datetime": "2026-06-01 10:00:00",
		"end_datetime": "2026-06-01 12:00:00"
	})
	chg.insert(ignore_permissions=True)
	chgName = chg.name

	meetingName = 'PW_TEST_CAB_Meeting'
	# Clean up if it exists
	if frappe.db.exists("ITSM CAB Meeting", meetingName):
		frappe.delete_doc("ITSM CAB Meeting", meetingName, ignore_permissions=True)

	doc = frappe.get_doc({
		"doctype": "ITSM CAB Meeting",
		"name": meetingName,
		"meeting_type": "Regular CAB",
		"scheduled_datetime": "2026-06-02 14:00:00",
		"duration_minutes": 60,
		"cab_chair": "Administrator",
		"quorum_required": 100,
		"cab_members": [
			{ "user": "pw_test_user_1@example.com", "role": "CAB Member", "vote": "Pending" }
		],
		"agenda_changes": [
			{ "change_request": chgName, "presenter": "Administrator", "decision": "Pending" }
		]
	})
	doc.insert(ignore_permissions=True)
	
	# Generate token
	vote = "Approve"
	token = get_signed_vote_token(meetingName, userEmail, chgName, vote)
	print("Generated Token:", token)

	print("TESTING RECORD CAB VOTE:")
	try:
		# record_cab_vote will respond_as_web_page or raise exception
		# Wait! In python, record_cab_vote calls frappe.respond_as_web_page which raises frappe.ValidationError or redirects.
		# Let's run it directly.
		record_cab_vote(meetingName, userEmail, chgName, vote, token)
		print("record_cab_vote ran successfully!")
	except Exception:
		print("record_cab_vote failed:")
		traceback.print_exc()

	# Teardown
	frappe.delete_doc("ITSM CAB Meeting", meetingName, ignore_permissions=True)
	frappe.delete_doc("ITSM Change", chgName, ignore_permissions=True)
