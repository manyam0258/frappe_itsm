frappe.ui.form.on("ITSM Incident", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Create Problem"), () => {
				frappe.model.with_doctype("ITSM Problem", () => {
					let problem = frappe.model.get_new_doc("ITSM Problem");
					problem.category = frm.doc.category;
					problem.description = frm.doc.description;
					problem.title = `Problem caused by: ${frm.doc.title}`;
					problem.priority = frm.doc.priority.includes("P1") ? "P1-Critical" :
					                   frm.doc.priority.includes("P2") ? "P2-High" :
					                   frm.doc.priority.includes("P3") ? "P3-Moderate" : "P4-Low";
					
					// Set linked incidents
					let child = frappe.model.add_child(problem, "linked_incidents");
					child.incident = frm.doc.name;
					
					frappe.set_route("Form", "ITSM Problem", problem.name);
				});
			}, __("Actions"));
			
			frm.add_custom_button(__("Create Change"), () => {
				frappe.model.with_doctype("ITSM Change", () => {
					let change = frappe.model.get_new_doc("ITSM Change");
					change.category = frm.doc.category;
					change.description = frm.doc.description;
					change.title = `Change Request for Incident: ${frm.doc.title}`;
					
					// Map Incident priority (P1-Critical, P2-High, etc.) to Change priority (Low, Medium, High, Critical)
					change.priority = frm.doc.priority.includes("P1") ? "Critical" :
					                  frm.doc.priority.includes("P2") ? "High" :
					                  frm.doc.priority.includes("P3") ? "Medium" : "Low";
					
					// Map Incident impact to Change impact
					change.impact = frm.doc.impact;
					change.change_type = "Normal";
					change.risk_level = "Medium";
					change.justification = `Fixing incident ${frm.doc.name}`;
					change.implementation_plan = "Deploy permanent fix.";
					change.change_initiator = frappe.session.user;
					change.change_owner = frappe.session.user;
					change.assigned_team = frm.doc.assigned_team || "";
					
					frappe.set_route("Form", "ITSM Change", change.name);
				});
			}, __("Actions"));
		}
	}
});
