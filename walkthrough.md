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

### 4. Problem Management & Change Management (Sprint 5)
- Created **Problem Management DocTypes**: `ITSM Problem`, `ITSM Problem Task`, `ITSM Problem Incident`.
- Implemented Python logic: Auto-generates a Known Error Database (KEDB) article draft when `workaround_published` is checked.
- Created **Change Management DocTypes**: `ITSM Change`, `ITSM Change Task`, `ITSM Change Risk Question`, `ITSM CAB Meeting`, and `ITSM Blackout Window`.
- Implemented Python logic for Change Management:
  - **Risk Score Calculation**: Dynamically computes risk score (0-100) and automatically assigns a Risk Level (Very Low to Very High) based on the filled risk questions.
  - **Blackout Window Validation**: Warns the user on save if the Change planned dates overlap with a scheduled `ITSM Blackout Window`.
- Generated **State Machine Workflows** for both Problem and Change modules.

### 5. Frontend Portals (Sprint 4)
- Configured a Vue 3 SPA using `frappe-ui-starter` in `/frontend`.
- Built the **Agent Portal**:
  - Main Layout with Sidebar and Topbar.
  - Interactive Dashboard showing KPIs.
  - Incident List View mapping data securely from Frappe REST APIs.
- Built the **Employee Self-Service Portal**:
  - Landing page for end-users to search knowledge or request services.
  - "My Tickets" list component.

> [!TIP]
> **Getting Started with Portals & New Modules**
> 1. Run the frontend development server: `cd apps/frappe_itsm/frontend && yarn dev`
> 2. Open `http://localhost:8080/frontend/agent/dashboard` in your browser.
> 3. To test Problem/Change backend logic, create a new `ITSM Change` and fill out the Risk Assessment section to see the auto-calculated score.

> [!NOTE]
> **Playwright E2E Tests**
> The `frappe-itsm-tests` directory has been scaffolded and a basic `sprint5.spec.js` test suite has been implemented to verify DocType structures and API functionality using Playwright as defined in `PLAYWRIGHT_SETUP.md`.

## Next Steps
Phase 1 is now fully complete! All ITSM core modules (Incident, SLA, Problem, Change) and initial Vue 3 Portals are scaffolded and functional. We are now ready to move onto Phase 2: Catalog and CMDB.
