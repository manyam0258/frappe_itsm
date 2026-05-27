frappe.ui.form.on("ITSM Problem", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Create Change"), () => {
				frappe.model.with_doctype("ITSM Change", () => {
					let change = frappe.model.get_new_doc("ITSM Change");
					change.category = frm.doc.category;
					change.description = frm.doc.description;
					change.title = `Change Request for Problem: ${frm.doc.title}`;
					change.priority = frm.doc.priority.includes("P1") ? "Critical" :
					                  frm.doc.priority.includes("P2") ? "High" :
					                  frm.doc.priority.includes("P3") ? "Medium" : "Low";
					
					change.change_type = "Normal";
					change.risk_level = "Medium";
					change.justification = `Fixing root cause for problem ${frm.doc.name}`;
					change.implementation_plan = "Deploy permanent fix.";
					change.change_initiator = frappe.session.user;
					change.change_owner = frappe.session.user;
					change.assigned_team = frm.doc.assigned_team || "";
					change.linked_problem = frm.doc.name;
					
					frappe.set_route("Form", "ITSM Change", change.name);
				});
			}, __("Actions"));
		}
	}
});
