# Copyright (c) 2026, Product Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class ITSMChange(Document):
    def before_save(self):
        self.calculate_risk_score()
        self.check_blackout_windows()
        
    def calculate_risk_score(self):
        if not self.risk_assessment:
            self.risk_score = 0
            # Don't auto-override risk level if it was manually set without questions
            return
            
        total_score = 0
        for q in self.risk_assessment:
            if q.answer and q.weight:
                try:
                    # Answer format: "1 - Low", "2 - Medium", etc.
                    val = int(q.answer.split(" - ")[0])
                    # PRB: Score = Sum(Factor Score * Weight) * 25
                    # weight is stored as percent (0-100), so divide by 100
                    total_score += (val * (q.weight / 100.0))
                except Exception:
                    pass
                    
        self.risk_score = min(int(total_score * 25), 100)
        
        # Set Risk Level based on score
        if self.risk_score <= 25:
            self.risk_level = "Very Low"
        elif self.risk_score <= 50:
            self.risk_level = "Low"
        elif self.risk_score <= 65:
            self.risk_level = "Medium"
        elif self.risk_score <= 80:
            self.risk_level = "High"
        else:
            self.risk_level = "Very High"
            
    def check_blackout_windows(self):
        if not self.start_datetime or not self.end_datetime:
            return
            
        start = get_datetime(self.start_datetime)
        end = get_datetime(self.end_datetime)
        
        # Find any blackout window that overlaps
        # Overlap condition: WindowStart <= ChangeEnd AND WindowEnd >= ChangeStart
        conflicts = frappe.db.sql("""
            SELECT name, title, start_datetime, end_datetime 
            FROM `tabITSM Blackout Window`
            WHERE start_datetime <= %s AND end_datetime >= %s
        """, (end, start), as_dict=True)
        
        if conflicts:
            self.blackout_conflict = 1
            details = []
            for c in conflicts:
                details.append(f"Conflicts with: {c.title} ({c.start_datetime} to {c.end_datetime})")
            self.conflict_details = "\n".join(details)
            
            # Warn the user, but don't throw an error (allow manager override later)
            frappe.msgprint("Warning: The planned dates overlap with a Blackout Window.", indicator="orange", alert=True)
        else:
            self.blackout_conflict = 0
            self.conflict_details = None

    def on_update(self):
        self.notify_linked_problem()

    def notify_linked_problem(self):
        if self.status in ["Completed", "Closed"] and self.linked_problem:
            if frappe.db.exists("ITSM Problem", self.linked_problem):
                prob = frappe.get_doc("ITSM Problem", self.linked_problem)
                if prob.status not in ["Resolved", "Closed"]:
                    prob.status = "Resolved"
                    prob.permanent_fix = f"{self.close_notes} (Change {self.name})" if self.close_notes else f"Fix deployed and completed in Change {self.name}"
                    prob.resolution_notes = f"Resolved via permanent fix implementation in Change {self.name}"
                    prob.save(ignore_permissions=True)
                    frappe.msgprint(f"Notified and resolved linked Problem: {prob.name}", alert=True)
