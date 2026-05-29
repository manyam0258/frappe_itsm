# Copyright (c) 2026, Product Team and contributors
# For license information, please see license.txt

import frappe
from collections import deque

def get_upstream_impact(ci_name):
	"""
	Returns a list of all CIs that depend on the given CI (upstream impact).
	Uses BFS to traverse parent relationships.
	"""
	impacted_cis = set()
	queue = deque([ci_name])
	
	while queue:
		current = queue.popleft()
		
		# Find all relationships where the current CI is the child (dependency)
		# We want to find the parent_ci (the dependent item)
		dependents = frappe.get_all(
			"ITSM CI Relationship",
			filters={"child_ci": current},
			fields=["parent_ci"]
		)
		
		for dep in dependents:
			parent = dep.parent_ci
			if parent not in impacted_cis and parent != ci_name:
				impacted_cis.add(parent)
				queue.append(parent)
	return list(impacted_cis)

@frappe.whitelist()
def get_upstream_impact_api(ci_name):
	return get_upstream_impact(ci_name)

