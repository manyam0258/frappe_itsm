# Copyright (c) 2026, Product Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ITSMProblem(Document):
    def before_save(self):
        self.set_problem_owner_from_incident()

    def on_update(self):
        self.publish_to_kedb()
        self.resolve_linked_incidents()

    def set_problem_owner_from_incident(self):
        if not self.problem_owner and self.linked_incidents:
            first_inc = self.linked_incidents[0].incident
            if first_inc:
                owner = frappe.db.get_value("ITSM Incident", first_inc, "owner")
                if owner:
                    self.problem_owner = owner
        
    def publish_to_kedb(self):
        # Only trigger if workaround_published is checked and workaround text exists
        if self.workaround_published and self.workaround:
            # Check if KB Article DocType exists (Phase 2 feature)
            if frappe.db.exists("DocType", "ITSM Knowledge Article"):
                # Check if we already created a draft for this problem
                existing_article = frappe.db.exists("ITSM Knowledge Article", {"source_problem": self.name})
                
                if not existing_article:
                    kb = frappe.new_doc("ITSM Knowledge Article")
                    kb.title = f"Known Error: {self.title}"
                    kb.article_type = "Known Error"
                    kb.content = f"<h3>Description</h3>{self.description}<h3>Workaround</h3>{self.workaround}"
                    kb.source_problem = self.name
                    kb.status = "Draft"
                    kb.category = self.category
                    kb.insert(ignore_permissions=True)
                    frappe.msgprint(f"Created Draft Knowledge Article: {kb.name} from Problem Workaround.", alert=True)
            else:
                # Mock implementation for Phase 1 since KB is Phase 2
                frappe.msgprint("Workaround Published to KEDB. (Phase 2 Knowledge Base will automatically draft an article).", alert=True, indicator="green")

    def resolve_linked_incidents(self):
        if self.status in ["Resolved", "Closed"] and self.linked_incidents:
            res_code = "Resolved by Problem"
            if not frappe.db.exists("ITSM Resolution Code", res_code):
                frappe.get_doc({
                    "doctype": "ITSM Resolution Code",
                    "resolution_code": res_code,
                    "description": "Resolved via root cause fix in linked Problem"
                }).insert(ignore_permissions=True)
                
            for item in self.linked_incidents:
                if frappe.db.exists("ITSM Incident", item.incident):
                    inc = frappe.get_doc("ITSM Incident", item.incident)
                    if inc.status not in ["Resolved", "Closed", "Cancelled"]:
                        inc.status = "Resolved"
                        inc.resolution_code = res_code
                        inc.resolution_notes = f"Resolved via Problem {self.name}. Notes: {self.resolution_notes}" if self.resolution_notes else f"Resolved via linked Problem: {self.name}"
                        inc.save(ignore_permissions=True)
                        frappe.msgprint(f"Automatically resolved linked Incident: {inc.name}", alert=True)
