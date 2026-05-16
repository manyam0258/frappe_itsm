# Phase 1: ITSM Core — Local Testing Walkthrough

This walkthrough covers the foundation, Incident Management, and SLA modules built during Phase 1 (Sprints 1–3) based on the PRD. The application `frappe_itsm` has been scaffolded, installed on your local `aaa` site, and populated with all the necessary DocTypes and business logic.

## What Was Implemented

### 1. Application & Foundation
- Created the new `frappe_itsm` application and installed it on site `aaa`.
- Created **Core DocTypes**:
  - `ITSM Category` & `ITSM Sub Category`
  - `ITSM Team` & `ITSM Location`
  - `ITSM Tag`
- Generated all the foundational **Roles** required for permissions (`ITSM Admin`, `ITSM Manager`, `ITSM Agent`, etc.).

### 2. Incident Management (Sprint 2)
- Created the `ITSM Priority Matrix` DocType to configure Impact/Urgency mappings for different companies.
- Created the massive `ITSM Incident` DocType adhering to ITIL v4 standards.
- Implemented **Auto-Calculation Logic** in the Python controller to determine the `Priority` based on the matrix whenever an Incident is saved.
- Created the **Incident Workflow**:
  - Automatically configured Frappe `Workflow State`, `Workflow Action Master`, and the core `Workflow` mapping the transitions: `New -> Assigned -> In Progress -> Pending -> Resolved -> Closed`.

### 3. SLA Engine (Sprint 3)
- Scaffolded all SLA configuration structures: `ITSM Working Hours`, `ITSM Holiday List`, and `ITSM SLA Policy` (with Condition, Target, and Escalation child tables).
- Created the `ITSM SLA Instance` to track individual SLAs assigned to incidents.
- Developed the Python Background Job (`sla_evaluator.py`) and wired it into `hooks.py` to periodically check response and resolution times against active SLAs.

> [!TIP]
> **Getting Started with Testing**
> 1. Start your local bench (`bench start`).
> 2. Create an `ITSM Priority Matrix` record (or use the hardcoded fallbacks that take over if no matrix is found).
> 3. Create a new `ITSM Incident` and test the auto-calculation of Priority based on your selected Impact and Urgency.
> 4. Test the Incident Workflow state transitions.

> [!NOTE]
> For the SLA Evaluation, since it is a background task, you can test it by manually running `bench --site aaa execute frappe_itsm.frappe_itsm.sla_evaluator.evaluate_slas`.

## Next Steps
Once you validate the local functionality for the Incident and SLA features, we can move on to completing the Portal/Dashboard portions of Phase 1 or transition straight to the Change/Problem modules. Let me know your feedback on the local test!
