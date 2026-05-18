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
- `[ ]` **E2E Testing (Backend & API)**
  - `[ ]` Write tests for Problem and Change logic
