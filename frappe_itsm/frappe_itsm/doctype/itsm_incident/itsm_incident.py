# Copyright (c) 2026, Product Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ITSMIncident(Document):
	def before_save(self):
		self.calculate_priority()
		self.check_for_duplicates()
		
	def check_for_duplicates(self):
		if self.is_new() or self.has_value_changed("category") or self.has_value_changed("caller"):
			if not self.category or not self.caller:
				return
			
			duplicate = frappe.db.get_value(
				"ITSM Incident",
				{
					"category": self.category,
					"caller": self.caller,
					"status": ["in", ["New", "Assigned", "In Progress", "Pending"]],
					"name": ["!=", self.name or ""]
				},
				"name"
			)
			
			if duplicate:
				if not self.parent_incident:
					self.parent_incident = duplicate
				frappe.msgprint(f"Warning: A potential duplicate incident was detected ({duplicate}). This incident has been linked to it.", alert=True, indicator="orange")

	def calculate_priority(self):
		if not self.impact or not self.urgency:
			return
		
		# Try to find a priority matrix for the company
		matrix = frappe.db.get_value(
			"ITSM Priority Matrix", 
			{"company": self.company, "impact": self.impact, "urgency": self.urgency},
			"priority"
		)
		
		if not matrix:
			# Fallback to global matrix without company
			matrix = frappe.db.get_value(
				"ITSM Priority Matrix", 
				{"company": ["in", ["", None]], "impact": self.impact, "urgency": self.urgency},
				"priority"
			)
			
		if matrix:
			self.priority = matrix
		else:
			# Hardcoded fallback as per PRD
			priority_map = {
				"1-Enterprise Wide": {"1-Critical": "P1-Critical", "2-High": "P1-Critical", "3-Medium": "P2-High", "4-Low": "P3-Moderate"},
				"2-Department Wide": {"1-Critical": "P1-Critical", "2-High": "P2-High", "3-Medium": "P3-Moderate", "4-Low": "P4-Low"},
				"3-Group Wide": {"1-Critical": "P2-High", "2-High": "P3-Moderate", "3-Medium": "P3-Moderate", "4-Low": "P4-Low"},
				"4-Individual": {"1-Critical": "P3-Moderate", "2-High": "P4-Low", "3-Medium": "P4-Low", "4-Low": "P5-Planning"}
			}
			self.priority = priority_map.get(self.impact, {}).get(self.urgency, "P4-Low")
