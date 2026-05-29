# Copyright (c) 2026, Product Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import hmac
import hashlib
from frappe.utils import get_url

class ITSMCABMeeting(Document):
	def on_update(self):
		if self.status == "Scheduled":
			self.send_voting_emails()
			
	def send_voting_emails(self):
		for member in self.cab_members:
			if member.vote == "Pending":
				agenda_html = "<ul>"
				for item in self.agenda_changes:
					chg = frappe.get_doc("ITSM Change", item.change_request)
					approve_url = generate_signed_vote_url(self.name, member.user, chg.name, "Approve")
					reject_url = generate_signed_vote_url(self.name, member.user, chg.name, "Reject")
					
					agenda_html += f"""
					<li>
						<strong>{chg.name}</strong>: {chg.title} (Risk: {chg.risk_level})<br>
						<a href="{approve_url}" style="color: green; font-weight: bold; margin-right: 15px;">Approve</a>
						<a href="{reject_url}" style="color: red; font-weight: bold;">Reject</a>
					</li>
					"""
				agenda_html += "</ul>"
				
				subject = f"CAB Meeting Action Required: Vote on changes for {self.name}"
				message = f"""
				<h3>CAB Meeting Voting Invitation</h3>
				<p>You are requested to vote on the following changes scheduled for discussion in CAB Meeting <strong>{self.name}</strong> on {self.scheduled_datetime}.</p>
				<p>Please click on the links below to cast your vote (no login required):</p>
				{agenda_html}
				<p>Regards,<br>ITSM CAB System</p>
				"""
				try:
					frappe.sendmail(
						recipients=[member.user],
						subject=subject,
						message=message,
						delayed=False
					)
					frappe.msgprint(f"Sent voting invitation email to {member.user}")
				except frappe.OutgoingEmailError:
					frappe.log_error(title="CAB Meeting Email Error", message="Outgoing email account not configured. Voting links email skipped.")


	def evaluate_votes_and_quorum(self):
		total_members = len(self.cab_members)
		if total_members == 0:
			return
			
		voted_members = len([m for m in self.cab_members if m.vote in ["Approve", "Reject"]])
		quorum_percent = self.quorum_required or 51
		
		if (voted_members / total_members) * 100.0 >= quorum_percent:
			for item in self.agenda_changes:
				approvals = len([m for m in self.cab_members if m.vote == "Approve"])
				rejections = len([m for m in self.cab_members if m.vote == "Reject"])
				
				chg = frappe.get_doc("ITSM Change", item.change_request)
				if approvals > rejections:
					item.decision = "Approved"
					if chg.status == "CAB Scheduled":
						chg.status = "CAB Approved"
						chg.save(ignore_permissions=True)
				elif rejections >= approvals:
					item.decision = "Rejected"
					if chg.status == "CAB Scheduled":
						chg.status = "Draft"
						chg.save(ignore_permissions=True)
						
			self.save(ignore_permissions=True)
			frappe.db.commit()

def generate_signed_vote_url(meeting_name, member_email, change_name, vote):
	secret = frappe.local.conf.get("db_password") or "default_secret"
	msg = f"{meeting_name}:{member_email}:{change_name}:{vote}".encode('utf-8')
	token = hmac.new(secret.encode('utf-8'), msg, hashlib.sha256).hexdigest()
	
	base_url = get_url()
	return f"{base_url}/api/method/frappe_itsm.frappe_itsm.doctype.itsm_cab_meeting.itsm_cab_meeting.record_cab_vote?meeting={meeting_name}&user={member_email}&change={change_name}&vote={vote}&token={token}"

def verify_vote_token(meeting_name, member_email, change_name, vote, token):
	secret = frappe.local.conf.get("db_password") or "default_secret"
	msg = f"{meeting_name}:{member_email}:{change_name}:{vote}".encode('utf-8')
	expected_token = hmac.new(secret.encode('utf-8'), msg, hashlib.sha256).hexdigest()
	return hmac.compare_digest(expected_token, token)

@frappe.whitelist(allow_guest=True)
def record_cab_vote(meeting, user, change, vote, token):
	if not verify_vote_token(meeting, user, change, vote, token):
		frappe.respond_as_web_page("Invalid Token", "The security token for this vote is invalid or expired.", http_status_code=403)
		return
		
	if not frappe.db.exists("ITSM CAB Meeting", meeting):
		frappe.respond_as_web_page("Not Found", f"CAB Meeting {meeting} not found.", http_status_code=404)
		return
		
	cab_meeting = frappe.get_doc("ITSM CAB Meeting", meeting)
	if cab_meeting.status in ["Completed", "Cancelled"]:
		frappe.respond_as_web_page("Meeting Closed", f"CAB Meeting {meeting} is already completed or cancelled.", http_status_code=400)
		return
		
	updated = False
	for member in cab_meeting.cab_members:
		if member.user == user:
			if member.vote not in ["Pending", "", None]:
				frappe.respond_as_web_page("Vote Already Recorded", f"You have already recorded your vote as '{member.vote}'.")
				return
			member.vote = vote
			member.attendance = "Attended"
			updated = True
			break
			
	if not updated:
		frappe.respond_as_web_page("Not Authorized", "You are not a registered member of this CAB meeting.", http_status_code=400)
		return
		
	cab_meeting.save(ignore_permissions=True)
	frappe.db.commit()
	
	cab_meeting.evaluate_votes_and_quorum()
	
	frappe.respond_as_web_page("Vote Recorded", f"Thank you! Your vote to '{vote}' the change {change} has been recorded successfully.")

@frappe.whitelist()
def get_signed_vote_token(meeting, user, change, vote):
	# Only logged in users can request token generation
	if frappe.session.user == "Guest":
		frappe.throw("Access denied", frappe.PermissionError)
	secret = frappe.local.conf.get("db_password") or "default_secret"
	msg = f"{meeting}:{user}:{change}:{vote}".encode('utf-8')
	return hmac.new(secret.encode('utf-8'), msg, hashlib.sha256).hexdigest()

