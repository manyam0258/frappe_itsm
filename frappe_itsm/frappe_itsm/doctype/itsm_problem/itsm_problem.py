# Copyright (c) 2026, Product Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ITSMProblem(Document):
    def on_update(self):
        self.publish_to_kedb()
        
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
