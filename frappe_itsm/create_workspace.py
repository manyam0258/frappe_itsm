import frappe
import json

def create_workspace():
    workspace_name = "Frappe ITSM"
    
    if not frappe.db.exists("Workspace", workspace_name):
        # We need to define links for the cards
        links = [
            # Core
            {"label": "ITSM Category", "link_type": "DocType", "link_to": "ITSM Category", "type": "Link"},
            {"label": "ITSM Sub Category", "link_type": "DocType", "link_to": "ITSM Sub Category", "type": "Link"},
            {"label": "ITSM Team", "link_type": "DocType", "link_to": "ITSM Team", "type": "Link"},
            {"label": "ITSM Location", "link_type": "DocType", "link_to": "ITSM Location", "type": "Link"},
            {"label": "ITSM Tag", "link_type": "DocType", "link_to": "ITSM Tag", "type": "Link"},
            
            # Incident
            {"label": "ITSM Priority Matrix", "link_type": "DocType", "link_to": "ITSM Priority Matrix", "type": "Link"},
            {"label": "ITSM Incident", "link_type": "DocType", "link_to": "ITSM Incident", "type": "Link"},
            
            # SLA Engine
            {"label": "ITSM Working Hours", "link_type": "DocType", "link_to": "ITSM Working Hours", "type": "Link"},
            {"label": "ITSM Holiday List", "link_type": "DocType", "link_to": "ITSM Holiday List", "type": "Link"},
            {"label": "ITSM SLA Policy", "link_type": "DocType", "link_to": "ITSM SLA Policy", "type": "Link"},
            {"label": "ITSM SLA Instance", "link_type": "DocType", "link_to": "ITSM SLA Instance", "type": "Link"},
        ]
        
        content = [
            {
                "id": "header_1",
                "type": "header",
                "data": {"text": "<span class=\"h4\">Incident Management</span>", "level": 4}
            },
            {
                "id": "card_incident",
                "type": "card",
                "data": {"card_name": "Incident Management"}
            },
            {
                "id": "header_2",
                "type": "header",
                "data": {"text": "<span class=\"h4\">SLA Engine</span>", "level": 4}
            },
            {
                "id": "card_sla",
                "type": "card",
                "data": {"card_name": "SLA Engine"}
            },
            {
                "id": "header_3",
                "type": "header",
                "data": {"text": "<span class=\"h4\">Core</span>", "level": 4}
            },
            {
                "id": "card_core",
                "type": "card",
                "data": {"card_name": "Core Setup"}
            }
        ]
        
        doc = frappe.new_doc("Workspace")
        doc.name = workspace_name
        doc.title = workspace_name
        doc.label = workspace_name
        doc.module = "Frappe ITSM"
        doc.is_standard = 1
        doc.public = 1
        doc.icon = "check"
        doc.content = json.dumps(content)
        
        # Incident Links
        doc.append("links", {"label": "Incident Management", "type": "Card Break", "only_for": ""})
        doc.append("links", {"label": "ITSM Incident", "link_type": "DocType", "link_to": "ITSM Incident", "type": "Link"})
        doc.append("links", {"label": "ITSM Priority Matrix", "link_type": "DocType", "link_to": "ITSM Priority Matrix", "type": "Link"})
        
        # SLA Links
        doc.append("links", {"label": "SLA Engine", "type": "Card Break", "only_for": ""})
        doc.append("links", {"label": "ITSM SLA Policy", "link_type": "DocType", "link_to": "ITSM SLA Policy", "type": "Link"})
        doc.append("links", {"label": "ITSM SLA Instance", "link_type": "DocType", "link_to": "ITSM SLA Instance", "type": "Link"})
        doc.append("links", {"label": "ITSM Working Hours", "link_type": "DocType", "link_to": "ITSM Working Hours", "type": "Link"})
        doc.append("links", {"label": "ITSM Holiday List", "link_type": "DocType", "link_to": "ITSM Holiday List", "type": "Link"})
        
        # Core Links
        doc.append("links", {"label": "Core Setup", "type": "Card Break", "only_for": ""})
        doc.append("links", {"label": "ITSM Category", "link_type": "DocType", "link_to": "ITSM Category", "type": "Link"})
        doc.append("links", {"label": "ITSM Sub Category", "link_type": "DocType", "link_to": "ITSM Sub Category", "type": "Link"})
        doc.append("links", {"label": "ITSM Team", "link_type": "DocType", "link_to": "ITSM Team", "type": "Link"})
        doc.append("links", {"label": "ITSM Location", "link_type": "DocType", "link_to": "ITSM Location", "type": "Link"})
        doc.append("links", {"label": "ITSM Tag", "link_type": "DocType", "link_to": "ITSM Tag", "type": "Link"})
        
        doc.insert(ignore_permissions=True)
        print(f"Created Workspace: {workspace_name}")
    else:
        print(f"Workspace {workspace_name} already exists.")
    
    frappe.db.commit()
