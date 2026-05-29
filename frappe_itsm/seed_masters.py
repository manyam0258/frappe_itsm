import frappe

def run():
	print("Starting master data seeding...")
	
	# 1. Company
	company_name = "Mindgraph Technologies Pvt Ltd"
	if not frappe.db.exists("Company", company_name):
		company = frappe.get_doc({
			"doctype": "Company",
			"company_name": company_name,
			"default_currency": "USD"
		})
		company.insert(ignore_permissions=True)
		print(f"Created Company: {company_name}")

	# 2. Categories
	for cat in ["Hardware", "Software", "Network", "Database", "Cloud"]:
		if not frappe.db.exists("ITSM Category", cat):
			frappe.get_doc({
				"doctype": "ITSM Category",
				"category_name": cat,
				"description": f"Category for {cat} systems"
			}).insert(ignore_permissions=True)
			print(f"Created Category: {cat}")

	# 3. Sub Categories
	sub_categories = [
		{"sub_category_name": "Laptops", "category": "Hardware", "description": "User laptops"},
		{"sub_category_name": "Printers", "category": "Hardware", "description": "Office printers"},
		{"sub_category_name": "Operating System", "category": "Software", "description": "OS issues"},
		{"sub_category_name": "Email", "category": "Software", "description": "Email access and outlook"},
		{"sub_category_name": "VPN", "category": "Network", "description": "Remote network access"},
		{"sub_category_name": "PostgreSQL", "category": "Database", "description": "Database server issues"}
	]
	for sc in sub_categories:
		if not frappe.db.exists("ITSM Sub Category", sc["sub_category_name"]):
			frappe.get_doc({
				"doctype": "ITSM Sub Category",
				"sub_category_name": sc["sub_category_name"],
				"category": sc["category"],
				"description": sc["description"]
			}).insert(ignore_permissions=True)
			print(f"Created Sub Category: {sc['sub_category_name']}")

	# 4. Locations
	locations = [
		{"location_name": "New York HQ", "address": "120 Broadway, New York, NY 10271"},
		{"location_name": "London Office", "address": "30 St Mary Axe, London EC3A 8BF"},
		{"location_name": "Bangalore Development Center", "address": "Outer Ring Rd, Bangalore 560103"}
	]
	for loc in locations:
		if not frappe.db.exists("ITSM Location", loc["location_name"]):
			frappe.get_doc({
				"doctype": "ITSM Location",
				"location_name": loc["location_name"],
				"address": loc["address"]
			}).insert(ignore_permissions=True)
			print(f"Created Location: {loc['location_name']}")

	# 5. Teams
	teams = [
		{"team_name": "IT Service Desk", "description": "First-line support"},
		{"team_name": "Network Team", "description": "Network infrastructure support"},
		{"team_name": "Software Team", "description": "Software applications support"},
		{"team_name": "Database Team", "description": "Database administration support"},
		{"team_name": "Hardware Team", "description": "Hardware diagnostics and repair"}
	]
	for team in teams:
		if not frappe.db.exists("ITSM Team", team["team_name"]):
			frappe.get_doc({
				"doctype": "ITSM Team",
				"team_name": team["team_name"],
				"description": team["description"]
			}).insert(ignore_permissions=True)
			print(f"Created Team: {team['team_name']}")

	# 6. Tags
	tags = [
		{"tag_name": "Critical", "color": "#FF0000"},
		{"tag_name": "VIP", "color": "#800080"},
		{"tag_name": "Security", "color": "#FFA500"}
	]
	for tag in tags:
		if not frappe.db.exists("ITSM Tag", tag["tag_name"]):
			frappe.get_doc({
				"doctype": "ITSM Tag",
				"tag_name": tag["tag_name"],
				"color": tag["color"]
			}).insert(ignore_permissions=True)
			print(f"Created Tag: {tag['tag_name']}")

	# 7. Priority Matrix
	impacts = ["1-Enterprise Wide", "2-Department Wide", "3-Group Wide", "4-Individual"]
	urgencies = ["1-Critical", "2-High", "3-Medium", "4-Low"]
	
	priority_mapping = {
		("1-Enterprise Wide", "1-Critical"): "P1-Critical",
		("1-Enterprise Wide", "2-High"): "P1-Critical",
		("1-Enterprise Wide", "3-Medium"): "P2-High",
		("1-Enterprise Wide", "4-Low"): "P3-Moderate",
		("2-Department Wide", "1-Critical"): "P1-Critical",
		("2-Department Wide", "2-High"): "P2-High",
		("2-Department Wide", "3-Medium"): "P3-Moderate",
		("2-Department Wide", "4-Low"): "P4-Low",
		("3-Group Wide", "1-Critical"): "P2-High",
		("3-Group Wide", "2-High"): "P3-Moderate",
		("3-Group Wide", "3-Medium"): "P3-Moderate",
		("3-Group Wide", "4-Low"): "P4-Low",
		("4-Individual", "1-Critical"): "P3-Moderate",
		("4-Individual", "2-High"): "P4-Low",
		("4-Individual", "3-Medium"): "P4-Low",
		("4-Individual", "4-Low"): "P5-Planning"
	}
	
	for (imp, urg), prio in priority_mapping.items():
		matrix_name = f"{company_name} - {imp} - {urg}"
		if not frappe.db.exists("ITSM Priority Matrix", matrix_name):
			frappe.get_doc({
				"doctype": "ITSM Priority Matrix",
				"matrix_name": matrix_name,
				"company": company_name,
				"impact": imp,
				"urgency": urg,
				"priority": prio
			}).insert(ignore_permissions=True)
			print(f"Created Priority Matrix Entry: {matrix_name} -> {prio}")

	# 8. Holiday List
	hlName = "Standard Holidays"
	if not frappe.db.exists("ITSM Holiday List", hlName):
		hl = frappe.get_doc({
			"doctype": "ITSM Holiday List",
			"list_name": hlName,
			"holidays": [
				{ "holiday_date": "2026-01-01", "description": "New Year's Day" },
				{ "holiday_date": "2026-12-25", "description": "Christmas Day" },
				{ "holiday_date": "2026-06-01", "description": "Summer Bank Holiday" }
			]
		})
		hl.insert(ignore_permissions=True)
		print(f"Created Holiday List: {hlName}")

	# 9. Working Hours
	whName = "Standard Working Hours"
	if not frappe.db.exists("ITSM Working Hours", whName):
		wh = frappe.get_doc({
			"doctype": "ITSM Working Hours",
			"schedule_name": whName,
			"timezone": "UTC",
			"monday_start": "09:00:00", "monday_end": "17:00:00",
			"tuesday_start": "09:00:00", "tuesday_end": "17:00:00",
			"wednesday_start": "09:00:00", "wednesday_end": "17:00:00",
			"thursday_start": "09:00:00", "thursday_end": "17:00:00",
			"friday_start": "09:00:00", "friday_end": "17:00:00"
		})
		wh.insert(ignore_permissions=True)
		print(f"Created Working Hours: {whName}")

	wh247 = "24x7 Support Hours"
	if not frappe.db.exists("ITSM Working Hours", wh247):
		wh = frappe.get_doc({
			"doctype": "ITSM Working Hours",
			"schedule_name": wh247,
			"timezone": "UTC",
			"monday_start": "00:00:00", "monday_end": "23:59:59",
			"tuesday_start": "00:00:00", "tuesday_end": "23:59:59",
			"wednesday_start": "00:00:00", "wednesday_end": "23:59:59",
			"thursday_start": "00:00:00", "thursday_end": "23:59:59",
			"friday_start": "00:00:00", "friday_end": "23:59:59",
			"saturday_start": "00:00:00", "saturday_end": "23:59:59",
			"sunday_start": "00:00:00", "sunday_end": "23:59:59"
		})
		wh.insert(ignore_permissions=True)
		print(f"Created Working Hours: {wh247}")

	# 10. SLA Policy
	policyName = "Standard SLA Policy"
	if not frappe.db.exists("ITSM SLA Policy", policyName):
		policy = frappe.get_doc({
			"doctype": "ITSM SLA Policy",
			"policy_name": policyName,
			"document_type": "ITSM Incident",
			"is_default": 1,
			"working_hours": whName,
			"holiday_list": hlName,
			"pause_statuses": "Pending",
			"fulfilled_statuses": "Resolved, Closed",
			"conditions": [
				{ "field": "company", "operator": "=", "value": company_name }
			],
			"targets": [
				{ "priority": "P1-Critical", "response_time_mins": 15, "resolution_time_mins": 60 },
				{ "priority": "P2-High", "response_time_mins": 60, "resolution_time_mins": 240 },
				{ "priority": "P3-Moderate", "response_time_mins": 120, "resolution_time_mins": 480 },
				{ "priority": "P4-Low", "response_time_mins": 240, "resolution_time_mins": 960 },
				{ "priority": "P5-Planning", "response_time_mins": 480, "resolution_time_mins": 1920 }
			],
			"escalation_rules": [
				{ "trigger_at_percent": 50, "action": "Notify Only", "notify_users": "admin@example.com" },
				{ "trigger_at_percent": 75, "action": "Escalate Priority", "priority_upgrade": "P1-Critical", "notify_users": "admin@example.com" },
				{ "trigger_at_percent": 100, "action": "Reassign + Notify", "reassign_to_team": "Hardware Team", "notify_users": "admin@example.com" }
			]
		})
		policy.insert(ignore_permissions=True)
		print(f"Created SLA Policy: {policyName}")

	# 11. SLA Instance and Test Incidents
	scenarios = [
		{
			"title": "SLA Scenario Happy Flow",
			"impact": "3-Group Wide",
			"urgency": "3-Medium",
			"status": "Assigned",
			"desc": "Happy path testing within SLA"
		},
		{
			"title": "SLA Scenario Paused Exception Flow",
			"impact": "2-Department Wide",
			"urgency": "2-High",
			"status": "Pending",
			"desc": "Exception path testing - Paused SLA status"
		},
		{
			"title": "SLA Scenario Breached Exception Flow",
			"impact": "1-Enterprise Wide",
			"urgency": "1-Critical",
			"status": "In Progress",
			"desc": "Exception path testing - SLA Target Breached"
		}
	]

	for i, sc in enumerate(scenarios, 1):
		inc_title = f"PW_TEST_{sc['title']}"
		existing_inc = frappe.get_all("ITSM Incident", filters={"title": inc_title}, pluck="name")
		for name in existing_inc:
			sla_inst = frappe.get_all("ITSM SLA Instance", filters={"document_type": "ITSM Incident", "document_name": name}, pluck="name")
			for s_name in sla_inst:
				frappe.delete_doc("ITSM SLA Instance", s_name, ignore_permissions=True, force=True)
			frappe.delete_doc("ITSM Incident", name, ignore_permissions=True, force=True)
			print(f"Cleaned old scenario incident: {name}")

		doc = frappe.get_doc({
			"doctype": "ITSM Incident",
			"title": inc_title,
			"category": "Hardware",
			"caller": "Administrator",
			"raised_by": "Administrator",
			"impact": sc["impact"],
			"urgency": sc["urgency"],
			"status": sc["status"],
			"description": sc["desc"],
			"company": company_name
		})
		doc.insert(ignore_permissions=True)
		print(f"Created Scenario Incident {i}: {doc.name} (Priority: {doc.priority}, Status: {doc.status})")

		sla_status = "Within SLA"
		if sc["status"] == "Pending":
			sla_status = "Paused"
		elif "Breached" in sc["title"]:
			sla_status = "Breached"

		if not frappe.db.exists("ITSM SLA Instance", {"document_type": "ITSM Incident", "document_name": doc.name}):
			from frappe.utils import now_datetime
			import datetime
			now = now_datetime()
			if sla_status == "Breached":
				res_due = now - datetime.timedelta(hours=2)
				rep_due = now - datetime.timedelta(hours=3)
			else:
				res_due = now + datetime.timedelta(hours=4)
				rep_due = now + datetime.timedelta(hours=1)

			sla_inst = frappe.get_doc({
				"doctype": "ITSM SLA Instance",
				"document_type": "ITSM Incident",
				"document_name": doc.name,
				"sla_policy": policyName,
				"priority": doc.priority,
				"start_time": now - datetime.timedelta(hours=1),
				"response_due": rep_due,
				"resolution_due": res_due,
				"sla_status": sla_status,
				"hold_duration": 0.0
			})
			sla_inst.insert(ignore_permissions=True)
			print(f"Seeded SLA Instance for Scenario Incident {doc.name} (Status: {sla_status})")

	frappe.db.commit()
	print("Seeding completed successfully!")
