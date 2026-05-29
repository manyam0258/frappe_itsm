# Phase 1, Sprint 1: ITSM Core Setup

- `[x]` **App Setup**
  - `[x]` Scaffold `frappe_itsm` app via bench
  - `[x]` Install `frappe_itsm` app on site `aaa`
  - `[x]` Configure initial app settings (hooks.py, naming series setup structure)
- `[x]` **Core DocTypes Setup**
  - `[x]` Create `ITSM Category` DocType
  - `[x]` Create `ITSM Sub Category` DocType
  - `[x]` Create `ITSM Team` DocType
  - `[x]` Create `ITSM Location` DocType
  - `[x]` Create `ITSM Tag` DocType
- `[x]` **Role Setup**
  - `[x]` Create base roles (`ITSM Admin`, `ITSM Agent`, `ITSM Manager`, etc.)

# Phase 1, Sprint 2: Incident Management Setup

- `[x]` **ITSM Incident DocType**
  - `[x]` Create `ITSM Priority Matrix` DocType
  - `[x]` Create `ITSM Incident` DocType with all fields
  - `[x]` Configure naming series `INC-{YYYY}-{#####}`
  - `[x]` Set up Impact × Urgency auto-calc (Server Script or Client Script)
- `[x]` **State Machine / Workflow**
  - `[x]` Set up Incident Workflow (New -> Assigned -> In Progress -> Pending -> Resolved -> Closed)

# Phase 1, Sprint 3: SLA Engine Setup

- `[x]` **SLA Base DocTypes**
  - `[x]` Create `ITSM Working Hours` DocType
  - `[x]` Create `ITSM Holiday List` DocType
- `[x]` **SLA Engine Configuration DocTypes**
  - `[x]` Create `ITSM SLA Target` DocType (Child)
  - `[x]` Create `ITSM SLA Escalation` DocType (Child)
  - `[x]` Create `ITSM SLA Condition` DocType (Child)
  - `[x]` Create `ITSM SLA Policy` DocType (Parent)
- `[x]` **SLA Instance & Logic**
  - `[x]` Create `ITSM SLA Instance` DocType
  - `[x]` Create `ITSM SLA Hold Log` DocType
  - `[x]` Implement Python SLA Evaluator Background Job
  - `[x]` Implement Python logic for SLA due calculation

# Phase 1, Sprint 4: Frontend Portals & Vue SPA

- `[x]` **Frontend Scaffold & Setup**
  - `[x]` Setup `frappe-ui-starter` in `frontend/`
  - `[x]` Configure `site_config.json` with `ignore_csrf = 1`
  - `[x]` Resolve `yarn` missing peer dependencies (`@tiptap/core`, `prosemirror-*`)
- `[x]` **Agent Portal (Vue SPA)**
  - `[x]` Setup Vue Router & Main Layout (Sidebar, Topbar)
  - `[x]` Create Incident List View (using Frappe UI `ListView` or custom table)
  - `[x]` Create Incident Detail View (Form, Timeline, Workflow actions)
- `[x]` **Employee Self-Service Portal**
  - `[x]` Create Self-Service Dashboard / Landing Page
  - `[x]` Create "My Tickets" view for Employees
  - `[x]` Create "Raise a Ticket" form component
- `[x]` **Playwright E2E Tests**
  - `[x]` Write Playwright test for creating an Incident via UI
  - `[x]` Write Playwright test for Agent resolving an Incident

# Phase 1, Sprint 5: Problem & Change Management

- `[x]` **Problem Management DocTypes**
  - `[x]` Create `ITSM Problem` DocType
  - `[x]` Create `ITSM Problem Incident` (Child)
  - `[x]` Create `ITSM Problem Task` (Child)
- `[x]` **Problem Management Logic**
  - `[x]` Problem State Machine / Workflow
  - `[x]` Python KEDB integration (Workaround publish -> KB Draft)
- `[x]` **Change Management DocTypes**
  - `[x]` Create `ITSM Change` DocType
  - `[x]` Create `ITSM Change Task` (Child)
  - `[x]` Create `ITSM CAB Meeting` DocType (plus Agenda and Member children)
  - `[x]` Create `ITSM Blackout Window` DocType
  - `[x]` Create `ITSM Change Risk Question` DocType
- `[x]` **Change Management Logic**
  - `[x]` Change State Machine / Workflow
  - `[x]` Python Risk Score Calculation
  - `[x]` Python Blackout Window Validation
- `[x]` **E2E Testing (Backend & API)**
  - `[x]` Write tests for Problem and Change logic

# Phase 1, Sprint 6: Workflow-Assignment Engine

- `[x]` **Workflow-Assignment Hook**
  - `[x]` Create `apps/frappe_itsm/frappe_itsm/frappe_itsm/utils/assignment.py` with dynamic assignment logic
  - `[x]` Register `before_save` hooks in `hooks.py`
- `[x]` **E2E Testing**
  - `[x]` Write Playwright test verifying that workflow transition triggers assignment rules

# Phase 2 Transition & Phase 1 Gaps

- `[x]` **SLA Engine Calculations**
  - `[x]` Update `ITSM SLA Instance` to include `triggered_escalations` field
  - `[x]` Implement timezone and calendar-aware business hour calculation in `calculate_sla_due`
  - `[x]` Implement `At Risk` state update and SLA breach evaluation
  - `[x]` Trigger escalations (email, prioritize, reassign) and store triggered states
- `[x]` **Knowledge Base Integration**
  - `[x]` Define and register `ITSM Knowledge Article` DocType
  - `[x]` Link workaround publish trigger in `itsm_problem.py` to create real draft articles
  - `[x]` Seed KB articles detailing Incident, SLA, Change, and Workflow developments
- `[x]` **Duplicate Scanning**
  - `[x]` Implement `check_for_duplicates` in `itsm_incident.py` to check categories/callers
  - `[x]` Warning alerts and linking duplicates via `parent_incident`
- `[x]` **CAB Email Voting**
  - `[x]` Add HMAC-SHA256 signature voting URL generation and verification logic
  - `[x]` Implement whitelisted guest api `record_cab_vote` to check quorum and change decisions
  - `[x]` Implement hook to automatically email members when Change is `CAB Scheduled`
- `[x]` **CMDB Structure & BFS Traversal**
  - `[x]` Define and register `ITSM CI` and `ITSM CI Relationship` DocTypes
  - `[x]` Write BFS traversal logic to find all upstream dependencies
- `[x]` **Service Catalog**
  - `[x]` Define and register `ITSM Catalog Item` and `ITSM Request Item` (RITM) DocTypes
- `[x]` **Playwright Config & Spec Refactoring**
  - `[x]` Create `.env` file in tests directory
  - `[x]` Refactor `playwright.config.js` to load `.env` variables
  - `[x]` Update all test spec files to use environment variables
- `[x]` **E2E Testing & Verification**
  - `[x]` Add test cases for SLA, duplicate scanning, guest voting, and CMDB
  - `[x]` Run test suite to verify success
