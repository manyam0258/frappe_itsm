import frappe

def create_doctypes():
	doctypes = [
		{
			"doctype": "DocType",
			"name": "ITSM Knowledge Article",
			"module": "Frappe ITSM",
			"custom": 1,
			"autoname": "KBA-.#####",
			"naming_rule": "Expression",
			"permissions": [
				{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Agent", "read": 1, "write": 1, "create": 1},
				{"role": "ITSM Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
				{"role": "ITSM Employee", "read": 1},
				{"role": "ITSM Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
			],
			"fields": [
				{"fieldname": "title", "fieldtype": "Data", "label": "Title", "reqd": 1, "in_list_view": 1},
				{"fieldname": "article_type", "fieldtype": "Select", "label": "Article Type", "options": "Known Error\nWorkaround\nStandard Operating Procedure\nGeneral Info", "reqd": 1, "default": "General Info", "in_list_view": 1},
				{"fieldname": "category", "fieldtype": "Link", "label": "Category", "options": "ITSM Category", "reqd": 1, "in_list_view": 1},
				{"fieldname": "source_problem", "fieldtype": "Link", "label": "Source Problem", "options": "ITSM Problem"},
				{"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nPublished\nArchived", "default": "Draft", "in_list_view": 1},
				{"fieldname": "views", "fieldtype": "Int", "label": "Views", "default": 0, "read_only": 1},
				{"fieldname": "content", "fieldtype": "Text Editor", "label": "Content", "reqd": 1}
			]
		}
	]

	for d in doctypes:
		if not frappe.db.exists("DocType", d["name"]):
			doc = frappe.get_doc(d)
			doc.insert(ignore_permissions=True)
			print(f"Created DocType {d['name']}")
		else:
			doc = frappe.get_doc("DocType", d["name"])
			doc.fields = []
			for f in d.get("fields", []):
				doc.append("fields", f)
			doc.permissions = []
			for p in d.get("permissions", []):
				doc.append("permissions", p)
			doc.save(ignore_permissions=True)
			print(f"Updated DocType {d['name']}")
			
	frappe.db.commit()
	seed_kb_articles()

def seed_kb_articles():
	articles = [
		{
			"title": "Incident Priority Auto-Calculation Matrix",
			"article_type": "Standard Operating Procedure",
			"category": "Hardware",
			"status": "Published",
			"content": """
			<h3>Overview</h3>
			<p>This article describes the Priority auto-calculation mechanism in the ITSM Incident management module.</p>
			<h3>Matrix Definition</h3>
			<p>Priority (P1-P5) is determined dynamically on save based on <strong>Impact</strong> and <strong>Urgency</strong>:</p>
			<ul>
				<li><strong>1-Enterprise Wide x 1-Critical</strong> -> P1-Critical</li>
				<li><strong>2-Department Wide x 2-High</strong> -> P2-High</li>
				<li><strong>3-Group Wide x 3-Medium</strong> -> P3-Moderate</li>
				<li><strong>4-Individual x 4-Low</strong> -> P5-Planning</li>
			</ul>
			"""
		},
		{
			"title": "SLA Engine Policy & Target Guidelines",
			"article_type": "Standard Operating Procedure",
			"category": "Software",
			"status": "Published",
			"content": """
			<h3>Overview</h3>
			<p>This article explains how SLAs are calculated and escalated inside the platform.</p>
			<h3>Key Calculations</h3>
			<p>The system computes due dates using the timezone defined on the linked <strong>ITSM Working Hours</strong> schedule and skips any dates matching the <strong>ITSM Holiday List</strong>.</p>
			<h3>Escalations</h3>
			<ul>
				<li><strong>50% elapsed:</strong> Standard warning notifications sent to managers/agents.</li>
				<li><strong>75% elapsed:</strong> SLA state transitions to 'At Risk'.</li>
				<li><strong>100% elapsed:</strong> SLA breach recorded, reassignment, or priority upgrades fired according to policy rules.</li>
			</ul>
			"""
		},
		{
			"title": "Change Control & Blackout Windows",
			"article_type": "Standard Operating Procedure",
			"category": "Cloud",
			"status": "Published",
			"content": """
			<h3>Overview</h3>
			<p>All Normal and Emergency Changes must check for schedule overlaps against active Blackout Windows prior to approval.</p>
			<h3>Validation</h3>
			<p>The system raises warning notices during Change saves if the proposed start/end times conflict with any registered <strong>ITSM Blackout Window</strong>.</p>
			"""
		},
		{
			"title": "Workflow Auto-Assignment Rules",
			"article_type": "Standard Operating Procedure",
			"category": "Network",
			"status": "Published",
			"content": """
			<h3>Overview</h3>
			<p>Dynamic round-robin and queue assignments are evaluated automatically on Workflow state transitions.</p>
			<h3>Assignment logic</h3>
			<p>Upon transition, standard open ToDo records are cancelled to preserve the audit trail, and the native <strong>Assignment Rule</strong> engine is re-applied to distribute work to the next member of the support group.</p>
			"""
		}
	]

	for art in articles:
		if not frappe.db.exists("ITSM Knowledge Article", {"title": art["title"]}):
			cat = frappe.db.get_value("ITSM Category", {"category_name": art["category"]}, "name") or art["category"]
			kb = frappe.new_doc("ITSM Knowledge Article")
			kb.title = art["title"]
			kb.article_type = art["article_type"]
			kb.category = cat
			kb.status = art["status"]
			kb.content = art["content"]
			kb.insert(ignore_permissions=True)
			print(f"Seeded KB Article: {art['title']}")
			
	frappe.db.commit()
