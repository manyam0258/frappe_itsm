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
