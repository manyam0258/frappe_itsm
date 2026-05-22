  
**PROCESS FLOWS & INSIGHTS**

frappe\_itsm — All 10 Modules End-to-End

*Actors · Decision Points · Automation Triggers · Cross-Module Connections · KPIs*

| Item | Detail |
| :---- | :---- |
| Source Document | frappe\_itsm PRD v1.0 — ITSM-PRD-2026-001 |
| Covers | 10 Modules \+ SLA Engine \+ Workflow Engine \+ Integration Map |
| Format | Step-by-step flows · Decision points · Automation events · Cross-module matrix |
| Date | May 2026 |
| Classification | CONFIDENTIAL — Internal |

# **Table of Contents**

| Module | Section | Key Contents |
| :---- | :---- | :---- |
| 1 | Incident Management | Submission → Triage → Assignment → Work → SLA → Resolution → Closure |
| 2 | Problem Management | Identification → RCA → KEDB → RFC → Resolution → PIR |
| 3 | Change Management | Standard / Normal / Emergency flows · CAB · Risk · Calendar · PIR |
| 4 | CMDB | CI Lifecycle · Relationship Management · Impact Analysis · Alerts |
| 5 | Service Catalog | Admin Build → User Browse → Submit → Approval → Fulfillment |
| 6 | Knowledge Base | Authoring · Review · Publish · Self-Service Deflection · Maintenance |
| 7 | Omnichannel | Message Ingestion · Inbox · Chat Widget · Bot · Handoff · CSAT |
| 8 | Reporting & Dashboards | Data Flow · Dashboard Render · Scheduled Reports · KPI Alerts |
| 9 | AI / Virtual Agent | Auto-Classification · Reply Assist · Chatbot Flow · Duplicate Detection |
| 10 | Asset Management | Hardware Lifecycle · Software Compliance · Depreciation · Alerts |
| 11 | Integration Map | Cross-module matrix · SLA Engine as shared service · Workflow Engine |

| MODULE 1 INCIDENT MANAGEMENT *End-to-End Process Flow* |
| :---: |

## **1.1  Process Purpose & Scope**

| *Incident Management restores normal service operation as quickly as possible with minimum disruption. It is the front door of ITSM — every service disruption from every channel enters here, gets prioritised, tracked against SLA, and resolved with a documented trail.* |
| :---- |

## **1.2  Process Actors**

| Actor | Role in this process | Portal Used |
| :---- | :---- | :---- |
| End User / Customer | Raises the incident; receives updates; provides CSAT feedback | Employee / Customer Portal |
| ITSM Agent | Owns day-to-day resolution; updates status; communicates with requester | Agent Portal |
| Senior Agent / IT Manager | Handles P1/P2 escalations; approves major incident; reviews SLA breaches | Agent Portal |
| Assignment Engine | Auto-routes new incidents to correct team based on category and routing rules | System (background) |
| SLA Engine | Calculates due dates; monitors timers; triggers escalation events | System (background) |
| Major Incident Manager | Coordinates bridge call; manages stakeholder communication for Major Incidents | Agent Portal |

## **1.3  End-to-End Process Flow**

### **Stage A — Incident Submission**

| 1 | User / System | Incident arrives via one of 6 channels Email (IMAP polling every 2 min) · Web Portal form · WhatsApp inbound · Live Chat · Voice (CTI screen pop) · REST API. The Omnichannel Engine normalises all inputs into a single ITSM Incident record. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Incident Created Naming series assigned: INC-{YYYY}-{\#\#\#\#\#} source\_channel recorded from ingestion metadata raised\_by linked to authenticated user or contact lookup Duplicate check: scan open incidents same category \+ requester → alert banner if found AI classifier suggests Category, Sub-Category, Priority (agent can accept/override) |
| :---- |

### **Stage B — Triage & Classification**

| 2 | Agent / AI | Category and sub-category selected Agent picks or confirms AI-suggested Category (Network, Hardware, Application, etc.) and Sub-Category. Filters available ITSM Categories linked to company. |
| :---: | :---- | :---- |

| 3 | Agent / System | Impact × Urgency evaluated → Priority auto-calculated Agent selects Impact (1-Enterprise Wide → 4-Individual) and Urgency (1-Critical → 4-Low). Server-side hook fires: reads ITSM Priority Matrix for company → sets Priority (P1–P5). P1/P2 also auto-flags for Major Incident review. |
| :---: | :---- | :---- |

| ◆  DECISION: Is this a Major Incident? (Enterprise-wide impact, multiple teams affected) ✅  YES → Agent checks is\_major\_incident → Major Incident Manager assigned → bridge notification sent → child incidents grouped under this parent ❌  NO  → Continue standard incident flow |
| :---- |

### **Stage C — Assignment**

| 4 | Assignment Engine | Routing rules evaluated → team assigned ITSM Automation Rule evaluates conditions (category, priority, company, department) → assigned\_team set. Round-robin or least-loaded assignment picks individual agent within team. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Assignment assigned\_to and assigned\_team fields updated Status transitions: New → Assigned Notification sent to assigned agent (email \+ in-app) SLA Engine creates ITSM SLA Instance: response\_due and resolution\_due calculated using working hours \+ holiday list SLA timer starts; background job evaluates every 5 minutes |
| :---- |

### **Stage D — Active Work**

| 5 | Agent | Acknowledges ticket; first response sent Agent opens ticket (status → In Progress). First public reply sent via original channel. first\_response\_at timestamp recorded. SLA response timer fulfilled. |
| :---: | :---- | :---- |

| 6 | Agent | Investigates; uses KEDB / KB Before working, agent checks right panel: (a) KEDB — any Known Errors matching category? Workaround shown. (b) KB suggestion panel — articles matching subject. If workaround found, applies it and fast-tracks to resolution. |
| :---: | :---- | :---- |

| 7 | Agent | Links affected CIs from CMDB Agent multi-selects impacted Configuration Items from CMDB lookup. ITSM Incident CI child table populated. CI record receives reverse-link showing this incident. |
| :---: | :---- | :---- |

| ◆  DECISION: Waiting on user response / vendor / scheduled change? ✅  YES → Status → Pending. On-hold reason selected (mandatory). SLA timer paused. on\_hold\_since recorded. ❌  NO  → Continue In Progress |
| :---- |

| 8 | System | Pending → In Progress auto-resume When customer replies (email/WhatsApp thread match), status auto-resumes to In Progress. SLA hold duration logged to ITSM SLA Hold Log. Elapsed hold time subtracted from SLA calculation. |
| :---: | :---- | :---- |

### **Stage E — SLA Monitoring & Escalation**

| ⚡  AUTO-TRIGGER: Every 5 minutes — SLA Evaluator Background Job 50% of resolution\_due elapsed → notification to assigned agent 75% of resolution\_due elapsed → notification to agent \+ team lead 100% elapsed (BREACHED) → L1 escalation: reassign to senior agent \+ notify IT Manager 125% elapsed (critical breach) → L2 escalation: notify IT Director \+ priority auto-upgraded sla\_status field updated: Within SLA → At Risk → Breached |
| :---- |

### **Stage F — Resolution**

| 9 | Agent | Marks Resolved; documents resolution Agent selects resolution\_code (required) and fills resolution\_notes (required). Status → Resolved. Validation: both fields mandatory before transition allowed. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Resolution resolution\_at timestamp recorded SLA fulfillment status finalised: Fulfilled or Breached CSAT survey triggered via original channel (email template / WhatsApp Interactive Message) 72-hour auto-close timer starts (background job checks every 30 min) Watch list users notified |
| :---- |

| ◆  DECISION: Requester disputes resolution (replies within 72h)? ✅  YES → Status → In Progress. reopened\_count incremented. New SLA instance created. Reopen metric recorded for KPI tracking. ❌  NO  → Status → Closed after 72h auto-close OR requester confirms resolution |
| :---- |

### **Stage G — Closure**

| 10 | System / Requester | Incident closed Auto-closed 72h after resolution (configurable per priority). Or requester clicks 'Confirm Resolved' on portal. SLA compliance data finalised. KPIs updated. closed\_at recorded. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Closure CSAT score linked to incident and agent performance record Incident metrics updated: MTTR, FCR, SLA compliance If is\_major\_incident: PIR task auto-created, assigned to Major Incident Manager Linked Problem (if any) notified of incident closure |
| :---- |

## **1.4  Exception Flows**

| Exception | Trigger | System Response | Actor |
| :---- | :---- | :---- | :---- |
| Duplicate Incident | New incident matches open incident (same category \+ requester \+ similar subject) | Alert banner shown; agent can Merge or Dismiss | Agent |
| No Agent Available | No agents online in assigned team at routing time | Incident stays in queue; IT Manager notified after 15 min; escalation after 30 min | System / IT Manager |
| Cancel Incident | Ticket is duplicate, test, or requester withdraws | Cancellation reason required; no SLA impact if cancelled within 15 min | Agent (Manager required if already Resolved) |
| Major Incident Bridge Fail | Major Incident Manager not assigned within 30 min of flag | Auto-escalate to IT Manager; send bridge call link to all watch list members | System |

| 🔗  CROSS-MODULE TOUCHPOINTS →  Problem Management: 'Create Problem' button on incident → PRB pre-filled with incident data; bidirectional link →  Change Management: incident linked to change that caused it; change record shows 'Incidents raised' →  CMDB: affected CIs linked; CI record shows linked incidents →  Knowledge Base: KB articles suggested during creation; deflection tracked →  Omnichannel: conversations linked to incidents; all channel history visible on incident →  SLA Engine: SLA Instance created on incident save; escalation rules evaluated continuously →  Reporting: every incident state contributes to FCR, MTTR, SLA compliance, CSAT KPIs →  AI: auto-classification on creation; duplicate detection; reply assist; summarisation |
| :---- |

| 📊  MODULE KPIs ▸  First Call Resolution Rate \= Closed without reassignment / Total incidents (target ≥ 70%) ▸  SLA Compliance Rate \= Incidents within SLA / Total (target ≥ 92%) ▸  Mean Time to Respond (MTTR-R) \= Avg(first\_response\_at − created\_at) (P3 target \< 2h) ▸  Mean Time to Resolve (MTTR) \= Avg(resolution\_at − created\_at) (P3 target \< 24h) ▸  CSAT Score \= Avg post-resolution survey rating (target ≥ 4.2/5.0) ▸  Reopen Rate \= Reopened / Resolved × 100 (target \< 3%) ▸  P1 Response Compliance \= P1 first-responded within 15 min / Total P1 (target ≥ 95%) |
| :---- |

| MODULE 2 PROBLEM MANAGEMENT *Root Cause Analysis · KEDB · Permanent Fix* |
| :---: |

## **2.1  Process Purpose**

| *Problem Management prevents recurrence of incidents by identifying and eliminating root causes. A Problem is a cause of one or more incidents. Once the root cause is known, the problem becomes a Known Error — documented in the KEDB so agents can apply workarounds instantly while the permanent fix is in progress.* |
| :---- |

## **2.2  End-to-End Process Flow**

### **Stage A — Problem Identification**

| 1 | Agent / IT Manager / System | Problem created Three entry points: (1) Agent clicks 'Create Problem' on an incident form — PRB pre-filled with incident category and description, incident auto-linked. (2) IT Manager raises proactively. (3) Auto-suggestion: background job detects 3+ open incidents same category within 2 hours → ITSM Problem Suggestion record → notifies IT Manager. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Problem Created Naming series: PRB-{YYYY}-{\#\#\#\#\#} Linked incident(s) recorded in ITSM Problem Incident child table problem\_owner assigned (mandatory before Assess transition) Status \= New |
| :---- |

| 2 | Problem Owner | Problem assessed for scope and priority Problem Owner reviews linked incidents, determines scope (category, affected services, number of users), and assigns Priority (P1–P4). Status → Assess. |
| :---: | :---- | :---- |

### **Stage B — Root Cause Analysis**

| 3 | Problem Owner | RCA methodology selected and investigation started Problem Owner selects methodology: 5-Whys, Fishbone, Fault Tree, Timeline Analysis. The corresponding structured form section renders in the problem record. Problem tasks created for parallel investigation streams (e.g., Network Team task \+ Application Team task simultaneously). |
| :---: | :---- | :---- |

| 4 | Investigation Team | Root cause identified and documented Team works problem tasks; each task has its own status, assignee, and due date. Once root cause confirmed, root\_cause and root\_cause\_category fields populated. Status → Root Cause Analysis. |
| :---: | :---- | :---- |

| ◆  DECISION: Is a permanent fix immediately achievable? ✅  YES → Create RFC (Change Request) → Status transitions to Fix in Progress → Change Manager notified ❌  NO  → Permanent fix deferred → Status → Known Error → Workaround documented and published to KEDB |
| :---- |

### **Stage C — Known Error & KEDB**

| 5 | Problem Owner | Workaround documented and published workaround field filled with step-by-step instructions. workaround\_published checkbox checked. error\_code assigned (e.g., KEDB-NET-001) for indexing. Workaround now visible in KEDB sidebar during incident creation for matching categories. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Workaround Published KEDB lookup activated: all future incidents in same category will see this workaround in right panel KB article auto-draft created: ITSM Knowledge Article in Draft status, pre-filled with problem title \+ workaround Linked incidents notified: workaround available notification sent to all linked incident agents |
| :---- |

### **Stage D — Permanent Fix**

| 6 | Change Manager | RFC raised from problem Problem Owner or Change Manager clicks 'Create RFC'. ITSM Change record created, pre-filled with problem title, category, linked\_problem reference. Change follows full Change Management lifecycle. Status → Fix in Progress. |
| :---: | :---- | :---- |

| 7 | Change Team | Permanent fix deployed Change implemented and closed. Change record notifies linked problem on closure. Problem Owner verifies fix by checking linked incidents are no longer recurring. resolution\_notes and permanent\_fix documented. |
| :---: | :---- | :---- |

### **Stage E — Resolution & Closure**

| 8 | Problem Owner | Problem marked Resolved permanent\_fix documented. Resolution confirmed against linked incidents. resolution\_notes required. Status → Resolved. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Problem Resolved Auto-close linked incidents still in Resolved state If pir\_required \= 1: PIR task auto-created, assigned to problem\_owner KEDB entry archived (workaround retained but marked Resolved) Problem metrics updated: time-in-state, linked incident count |
| :---- |

| ◆  DECISION: pir\_required \= 1? ✅  YES → PIR task must be completed before Closed transition is allowed ❌  NO  → Problem Owner closes directly → Status \= Closed |
| :---- |

| 9 | Problem Owner | Closure and Post-Implementation Review PIR documents lessons learned, process improvements, and prevention measures. PIR findings optionally converted to KB article. Status → Closed. |
| :---: | :---- | :---- |

| 🔗  CROSS-MODULE TOUCHPOINTS →  Incident Management: linked incidents shown with status rollup; incidents auto-closed on problem resolution →  Change Management: 'Create RFC' button → RFC pre-filled from problem; change closure notifies problem →  Knowledge Base: workaround auto-draft KB article created; PIR findings → KB article →  CMDB: CI impact inherited from linked incidents; problem form can directly link affected CIs →  Reporting: MTTR-P, recurrence rate, incident count per problem tracked on Problem Management dashboard |
| :---- |

| 📊  MODULE KPIs ▸  Problem Resolution Rate \= Problems resolved within target / Total problems ▸  Recurrence Rate \= Problems re-opened same root cause / Total problems (target \< 5%) ▸  Mean Incidents per Problem \= Avg linked incident count ▸  Workaround Coverage \= Problems in Known Error with published workaround / Total Known Errors (target 100%) ▸  Time to Known Error \= Avg time from New to Known Error state |
| :---- |

| MODULE 3 CHANGE MANAGEMENT *Standard · Normal · Emergency RFC · CAB · PIR* |
| :---: |

## **3.1  Process Purpose**

| *Change Management minimises risk from IT changes while enabling delivery speed. Three change types with distinct approval paths ensure that routine changes move fast while high-risk changes receive proper governance. Every change is documented, risk-scored, approved, scheduled on the change calendar, implemented, and reviewed.* |
| :---- |

## **3.2  Three Change Type Flows**

### **3.2.1  Standard Change (Low Risk — Pre-Approved)**

| 1 | Change Initiator | Select Standard Change Template Initiator picks from ITSM Change Template library. Template pre-fills: category, implementation plan, rollback plan, assigned team. Risk auto-set to Very Low. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: Standard Change Created cab\_required \= False (auto-set) Status auto-advances: New → Authorised (no review needed) Technical approver notified (optional, configurable per template) Change calendar entry created for planned window |
| :---- |

| 2 | Change Owner | Implement and Close Owner implements during planned window. Status → In Progress → Completed. close\_code selected. If Completed \= Successful: closed automatically within 24h. |
| :---: | :---- | :---- |

### **3.2.2  Normal Change (Medium-High Risk — Full CAB)**

| 1 | Change Initiator | Draft RFC with all mandatory fields Fills: title, description, business justification, implementation plan, rollback plan (mandatory), test plan, planned start/end, affected CIs, affected services, downtime expected. |
| :---: | :---- | :---- |

| 2 | System | Risk Assessment Questionnaire evaluated Initiator completes 5-factor risk questionnaire: (1) Number of CIs affected, (2) Business criticality, (3) Change failure history, (4) Rollback tested?, (5) Implementation window. Risk Score 0–100 auto-calculated. Risk Level: Very Low / Low / Medium / High / Very High. |
| :---: | :---- | :---- |

| ◆  DECISION: Planned dates overlap a Blackout Window? ✅  YES → Alert banner shown. Manager can override with justification. Blackout conflict flag set. ❌  NO  → Continue — no conflict |
| :---- |

| 3 | Change Initiator | Submit for Technical Review Status → Pending Review. Technical Reviewer assigned (mandatory for Normal changes). Reviewer gets notification. |
| :---: | :---- | :---- |

| 4 | Technical Reviewer | Technical Review Reviewer assesses: implementation plan completeness, rollback plan validity, CI impact accuracy, test plan adequacy. Decision: Approve (→ CAB Scheduled) or Reject with comments (→ Draft for revision). |
| :---: | :---- | :---- |

| 5 | Change Manager | Add to CAB Meeting Agenda Change added to next scheduled CAB meeting. ITSM CAB Meeting record updated. cab\_meeting linked on RFC. Status → CAB Scheduled. All CAB members notified. |
| :---: | :---- | :---- |

| 6 | CAB Members | CAB Review and Vote CAB Chair presents change. Members discuss risk, impact, timing. Each member votes: Approve or Reject. Email-based voting: members receive signed URL → click Approve/Reject without logging in. Quorum required (default 51% of members). |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On CAB Vote Completed (Quorum Met) If majority Approve: Status → CAB Approved If majority Reject: Status → Draft; initiator notified with rejection reasons All voter decisions logged with timestamp and comment |
| :---- |

| 7 | Change Manager | Final Authorisation Change Manager reviews CAB decision, final risk check, confirms implementation window vs change calendar. Status → Authorised. Change calendar entry locked. |
| :---: | :---- | :---- |

| ◆  DECISION: Conflict with another change on same CI in same window? ✅  YES → ITSM Change Conflict alert raised. Both change owners notified. Manual resolution required. ❌  NO  → Continue to Scheduled |
| :---- |

| 8 | Change Owner | Implement Change On planned start date/time: Status → In Progress. actual\_start recorded. Change tasks executed: Pre-Implementation → Implementation → Post-Implementation. Each task has assignee, due time, completion status. |
| :---: | :---- | :---- |

| ◆  DECISION: Implementation successful? ✅  YES → Status → Completed. close\_code \= Successful. PIR triggered if risk\_level was High/Very High. ❌  NO  → Status → Failed. close\_code \= Unsuccessful — Rolled Back. Rollback plan executed. PIR mandatory. |
| :---- |

| 9 | Change Owner / PIR Lead | Post-Implementation Review PIR documents: what happened, what went wrong, lessons learned, process improvements. For Failed changes: problem record created automatically. PIR findings shared with CAB. Status → PIR Pending → Closed. |
| :---: | :---- | :---- |

### **3.2.3  Emergency Change (Urgent — ECAB)**

| 1 | Change Initiator | Emergency RFC raised Justification must document: nature of emergency, business risk if change not made, rollback plan. change\_type \= Emergency. Risk may be variable — not blocked by high risk score. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: Emergency Change Triggered ECAB notification sent to all ECAB members (subset of CAB) immediately Status auto-advances: New → Pending Review (ECAB track) Minimum 2 approvers required (configurable) Approval window: 4 hours (configurable) |
| :---- |

| 2 | ECAB Members | Expedited Approval ECAB members approve/reject via email token or in-app within 4 hours. If 2 approvals received: Authorised immediately. Retrospective CAB review scheduled automatically. |
| :---: | :---- | :---- |

| 3 | Change Owner | Implement (during or after approval) Emergency changes may begin implementation before full authorisation in genuine emergencies — documented exception. Status tracked in parallel. |
| :---: | :---- | :---- |

| 4 | Change Manager | Retrospective CAB Review After emergency change closed, standard CAB reviews: was the emergency justified? Were procedures followed? Findings documented. Unauthorised emergency changes flagged in compliance report. |
| :---: | :---- | :---- |

## **3.3  Change Calendar & Blackout Windows**

The Change Calendar (visual month/week/day view) shows all Authorised and Scheduled changes. Each entry is colour-coded by risk level (green=low, amber=medium, red=high). Blackout windows (e.g., financial year-end, peak trading periods) are configured in ITSM Blackout Window DocType. During freeze periods, only Emergency changes are allowed — Standard and Normal changes are blocked at the Authorised transition.

| 🔗  CROSS-MODULE TOUCHPOINTS →  Incident Management: incidents linked to changes that caused them; failed changes auto-create incidents →  Problem Management: problem → RFC promotion (bidirectional link); change closure notifies problem →  CMDB: affected CIs linked; CI record shows change schedule tab; change failure triggers CI status update →  Service Catalog: Standard change templates usable as catalog fulfillment items →  Reporting: Change success rate, CAB cycle time, unauthorised changes tracked on Change Dashboard →  Workflow Engine: CAB approval email tokens generated by Workflow Engine |
| :---- |

| 📊  MODULE KPIs ▸  Change Success Rate \= Successful changes / Total changes (target ≥ 96%) ▸  Failed Change Rate \= Failed \+ Rolled Back / Total changes (target \< 3%) ▸  CAB Approval Cycle Time \= Avg(Authorised date − Submitted date) for Normal changes ▸  Unauthorised Change Rate \= Retrospective RFCs / Total changes (target \< 1%) ▸  Emergency Change Ratio \= Emergency changes / Total changes (target \< 5%) ▸  Change Freeze Violation Count \= Changes attempted during freeze periods (target \= 0\) |
| :---- |

| MODULE 4 CMDB *Configuration Management Database · CI Lifecycle · Impact Analysis* |
| :---: |

## **4.1  Process Purpose**

| *The CMDB is the authoritative record of every configuration item (CI) in the IT environment — hardware, software, services, network, cloud, and facilities. It is the connective tissue that links incidents, problems, changes, and assets to the business services they support. Without the CMDB, impact analysis is guesswork.* |
| :---- |

## **4.2  CI Lifecycle Flow**

| 1 | Asset Manager / Discovery | CI Record Created Four creation paths: (1) Manual entry via Agent Portal CMDB module. (2) Bulk CSV import with column-mapping wizard. (3) Asset deployment: when ITSM Asset status → In Use, CI auto-created or linked. (4) Cloud API import (AWS/Azure). All paths feed the same ITSM CI DocType. |
| :---: | :---- | :---- |

| 2 | CI Owner | Attributes populated Class-specific attributes filled: Hardware CIs need serial number, model, IP, warranty. Software CIs need version, vendor, license count, EoL date. Service CIs need service owner, SLA policy, business criticality. |
| :---: | :---- | :---- |

| 3 | CI Owner | Relationships defined Relationships created in ITSM CI Relationship DocType: source\_ci → relationship\_type → target\_ci. Examples: 'PROD-WEB-01 Runs on RACK-A3' · 'CRM-APP Hosted on PROD-WEB-01' · 'PROD-DB Depends on PROD-WEB-01'. Bidirectional relationships shown on both CI records. |
| :---: | :---- | :---- |

| 4 | CI Owner | CI Status tracked through lifecycle States: On Order → In Stock → In Use → In Maintenance → Retired → Disposed → Stolen. Each transition logged. CI owner notified on status change. |
| :---: | :---- | :---- |

## **4.3  Impact Analysis Flow**

| 5 | Agent / Change Manager | Select CI and run impact analysis On Incident, Problem, or Change form: agent selects affected CI. System traverses the CI relationship graph (BFS upstream): finds all CIs that depend on the selected CI, all services hosted on it, all users affected by those services. |
| :---: | :---- | :---- |

| 6 | System | Impact result displayed Impact panel shows: affected services (by criticality), upstream CIs, estimated user count, linked open incidents. Change Manager uses this before authorising any change. Agent uses this to determine incident priority. |
| :---: | :---- | :---- |

## **4.4  CMDB Alerts & Maintenance**

| ⚡  AUTO-TRIGGER: Daily Background Job Warranty expiry check: CI owner notified 90 days before warranty\_end (creates ITSM CI Alert) EoL date check: CI owner notified 180 days before end\_of\_life Stale CI detection: CIs not updated in 90+ days flagged on CMDB Health Dashboard Orphan detection: CIs with no relationships flagged (data quality issue) Data completeness scoring: % of mandatory attributes filled per CI class |
| :---- |

| 🔗  CROSS-MODULE TOUCHPOINTS →  Incident Management: CIs linked to incidents; impact analysis during triage →  Problem Management: CIs linked to problems; service impact scoping →  Change Management: affected CIs listed on RFC; change schedule tab on CI record →  Asset Management: deployed asset → CI auto-created; asset and CI stay in sync →  Omnichannel: 'What systems are affected?' answered from CMDB during agent conversation →  Reporting: CMDB health dashboard — completeness, stale CIs, warranty forecast |
| :---- |

| 📊  MODULE KPIs ▸  CMDB Data Completeness \= Mandatory fields filled / Total mandatory fields per CI class (target ≥ 90%) ▸  CI Discovery Coverage \= CIs discovered automatically / Total CIs (target ≥ 70%) ▸  Stale CI Rate \= CIs not updated in 90d / Total CIs (target \< 10%) ▸  Orphaned CI Rate \= CIs with no relationships / Total CIs (target \< 5%) ▸  Warranty Expiry in 90d \= Count of CIs with warranty expiring in 90 days |
| :---- |

| MODULE 5 SERVICE CATALOG *Self-Service Portal · Approval Workflow · Fulfillment* |
| :---: |

## **5.1  Process Purpose**

| *The Service Catalog replaces ad-hoc IT requests via email with a structured, self-service experience. Employees browse a searchable catalog, fill guided forms, and track their requests through approval and fulfillment in real time — without calling anyone.* |
| :---- |

## **5.2  Catalog Administration Flow (Admin)**

| 1 | ITSM Admin / Dept Admin | Create Catalog and Categories Top-level ITSM Catalog created (IT Services, HR Services, Facilities). ITSM Catalog Categories created within each catalog. Hierarchy is 2 levels deep (Category → Sub-Category). Non-IT admins (HR, Facilities) can manage their own catalog section independently. |
| :---: | :---- | :---- |

| 2 | ITSM Admin | Build Catalog Item Item name, description, icon, short description. Fulfillment team assigned. SLA target in business hours. Variable form built using drag-and-drop builder: 13 field types, conditional visibility rules, variable sets imported. Approval rules configured: Sequential / Parallel / Manager-of-Requester. |
| :---: | :---- | :---- |

| 3 | ITSM Admin | Publish Item (Draft → Active) Item status set to Active. Immediately visible in self-service portal for authorised roles/departments. Version tracked — each publish increments version number. |
| :---: | :---- | :---- |

## **5.3  Request Submission Flow (Requester)**

| 4 | Employee / Customer | Browse and select catalog item Portal home shows: Featured items, Popular items (most-requested), search bar, category browse. Requester searches or browses, selects item, reads description and cost. |
| :---: | :---- | :---- |

| 5 | Employee | Fill item form and add to cart Dynamic form renders catalog item variables. Conditional fields show/hide based on other field values. Required fields validated client-side. Multiple items can be added to cart; submitted as one ITSM Service Request. |
| :---: | :---- | :---- |

| 6 | Employee | Submit request One ITSM Service Request created. Each catalog item in cart generates a separate ITSM Request Item (RITM) with its own: approval chain, fulfillment tasks, status, and SLA timer. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Service Request Submitted ITSM Service Request naming: REQ-{YYYY}-{\#\#\#\#\#} Each RITM: RITM-{YYYY}-{\#\#\#\#\#} Approval chain evaluated per RITM: if requires\_approval \= False → auto-approved immediately If approval required: first approver(s) notified (email with Approve/Reject token link) Requester sees 'Submitted' status on portal; email acknowledgement sent |
| :---- |

## **5.4  Approval Flow**

| 7 | Approver | Receives approval notification Email contains: item description, requester name, filled form variables, business justification. Approve and Reject links are signed tokens valid for 7 days — no login required. Approver can also approve in-portal via My Approvals screen. |
| :---: | :---- | :---- |

| ◆  DECISION: Approval type \= Sequential? ✅  YES → Approver A → if approved → Approver B notified → if approved → Authorised ❌  NO  → Parallel: all approvers notified simultaneously → all must approve (or any, per config) |
| :---- |

| ◆  DECISION: Approver action taken within timeout period? ✅  YES → Decision recorded (approved/rejected with comment and timestamp) ❌  NO  → Escalate to secondary approver or auto-approve/reject per catalog item config |
| :---- |

| ⚡  AUTO-TRIGGER: On RITM Fully Approved RITM status → Approved Fulfillment tasks auto-created and assigned to fulfillment team SLA timer starts for RITM (sla\_hours from catalog item) Requester notified: 'Your request is approved and in fulfillment' |
| :---- |

## **5.5  Fulfillment Flow**

| 8 | Fulfillment Team | Work fulfillment tasks Fulfillment team sees assigned Request Tasks in Agent Portal queue. Tasks have phases (pre-delivery, delivery, verification). Each task completion advances RITM fulfillment % indicator. |
| :---: | :---- | :---- |

| 9 | Fulfillment Team | Mark RITM Fulfilled All tasks completed. RITM status → Fulfilled. Completion date recorded. Service Request closes when all RITMs are fulfilled. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On RITM Fulfilled Requester notified via email and portal notification CSAT survey sent for service experience rating Catalog fulfillment SLA compliance recorded Asset record created if item type \= Hardware Asset (laptop, phone, etc.) |
| :---- |

| 🔗  CROSS-MODULE TOUCHPOINTS →  Incident Management: fulfillment issues create incidents; agent can raise incident from failed RITM →  Change Management: Standard change templates are catalog items (e.g., 'Request Server Access') →  CMDB: hardware fulfillment creates/links CI on deployment →  Asset Management: hardware asset provisioned from stock on fulfillment →  Knowledge Base: catalog item pages link to relevant KB articles →  Omnichannel: request status trackable via WhatsApp bot (check\_ticket\_status intent) |
| :---- |

| 📊  MODULE KPIs ▸  Catalog Adoption Rate \= Requests via catalog / Total requests (target ≥ 60%) ▸  Catalog Fulfillment SLA \= RITMs fulfilled within SLA / Total RITMs (target ≥ 90%) ▸  Approval Cycle Time \= Avg time from submission to first approval ▸  Self-Service Submission Rate \= Requests submitted without agent involvement / Total requests ▸  Most Requested Items \= Top 10 items by RITM volume (monthly) |
| :---- |

| MODULE 6 KNOWLEDGE BASE *Article Lifecycle · Self-Service Deflection · KEDB* |
| :---: |

## **6.1  Process Purpose**

| *The Knowledge Base enables self-service resolution — customers and employees find answers without creating tickets. Agents use it to resolve incidents faster. The deflection rate (sessions resolved via KB without a ticket) is the primary KPI. Every article has a defined lifecycle with review gates to prevent stale content.* |
| :---- |

## **6.2  Article Authoring Flow**

| 1 | Agent / KB Author | Create article in Draft Author creates ITSM Knowledge Article. Rich text editor (TipTap/Quill) supports headers, code blocks, tables, images, video embeds. Category and sub-category assigned. Visibility set: Public / Internal (Agents Only) / Team Only. |
| :---: | :---- | :---- |

| 2 | Author | Submit for review Author sets status → Under Review. Reviewer assigned (mandatory). Reviewer notified via email \+ in-app. |
| :---: | :---- | :---- |

| ◆  DECISION: Reviewer approves article? ✅  YES → Status → Published. Published timestamp and version (v1) recorded. Search index updated immediately. ❌  NO  → Reviewer rejects with comments → Status back to Draft. Author notified with review comments. |
| :---- |

| 3 | System | Article visible per visibility setting Public articles: visible on Customer Portal \+ Employee Portal \+ Agent Portal. Internal articles: Agent Portal only. Team Only: restricted to members of specified ITSM Team. |
| :---: | :---- | :---- |

## **6.3  Self-Service Deflection Flow**

| 4 | User | Visits self-service portal and searches User types query in portal search bar. Full-text search scans title, content, and tags. Results show highlighted matches. Session event 'portal\_session\_started' recorded. |
| :---: | :---- | :---- |

| 5 | System | Article opened — view tracked view\_count incremented. Session event 'article\_viewed' recorded. 'Was this helpful?' prompt shown at article end. |
| :---: | :---- | :---- |

| ◆  DECISION: User submits ticket after viewing KB article? ✅  YES → Session \= NOT deflected. Both article\_viewed and ticket\_created events recorded in same session. ❌  NO  → User closes portal without creating ticket \= DEFLECTED session. Deflection count incremented. |
| :---- |

| 6 | User | Provides helpfulness feedback User clicks 'Yes' or 'No' on helpfulness prompt. If 'No': optional free-text comment. Feedback stored in ITSM KB Feedback DocType. Author notified of low-rating feedback. |
| :---: | :---- | :---- |

## **6.4  KB Suggestion During Incident Creation**

| 7 | Agent / User | Types incident subject As subject field is typed (debounced 400ms), API call to KB search endpoint. Top 3 matching articles shown in right-panel collapsible sidebar. Agent can click to open article in new tab. View tracked even when opened from suggestion panel. |
| :---: | :---- | :---- |

| 8 | Agent | Applies workaround from suggestion If article contains the workaround needed, agent copies content to workaround field on incident. Incident can be fast-tracked to Resolved without further investigation. |
| :---: | :---- | :---- |

## **6.5  Article Maintenance Flow**

| ⚡  AUTO-TRIGGER: Daily Background Job Check valid\_until date on all Published articles Articles past valid\_until → auto-retire (status \= Retired); author notified to review Articles with helpful % \< 30% and \> 20 views → flagged on KB Admin Dashboard for revision |
| :---- |

| 9 | Author | Revive or update article Author revives Retired article → new Draft version created (version incremented). Previous version preserved in ITSM KB Version history. Edit, submit for review, re-publish cycle repeats. |
| :---: | :---- | :---- |

| 🔗  CROSS-MODULE TOUCHPOINTS →  Incident Management: KB articles suggested during incident creation; workaround copy to incident →  Problem Management: problem workaround → auto-draft KB article; PIR findings → new article →  Service Catalog: catalog items link to relevant KB articles for self-service guidance →  Omnichannel: Virtual Agent (chatbot) searches KB for answers to user queries →  AI: embedding-based semantic search enhances keyword search for better matches (Phase 2\) →  Reporting: deflection rate, view count, helpfulness %, expiring articles on KB dashboard |
| :---- |

| 📊  MODULE KPIs ▸  KB Deflection Rate \= Deflected sessions / Total portal sessions (target ≥ 20%) ▸  Article Helpfulness Rate \= Helpful votes / (Helpful \+ Not Helpful) votes (target ≥ 75%) ▸  KB Coverage \= Incidents resolved using KB / Total incidents (measures KB utility) ▸  Article Expiry Compliance \= Published articles past valid\_until / Total published (target \= 0%) ▸  Search-to-Resolution Rate \= KB searches that avoid ticket creation / Total searches |
| :---- |

| MODULE 7 OMNICHANNEL COMMUNICATION *Unified Inbox · Email · Chat · WhatsApp · Voice* |
| :---: |

## **7.1  Process Purpose**

| *The Omnichannel module eliminates channel silos. Every customer communication — regardless of whether it arrives via email, live chat, WhatsApp, or phone — is captured as a Conversation record and handled from a single agent inbox. Agents see full cross-channel history. No message falls through the cracks.* |
| :---- |

## **7.2  Message Ingestion Flow (per channel)**

| 1 | Customer | Sends message on any channel Email → Frappe IMAP poller picks up every 2 minutes. Chat → Socket.io message event. WhatsApp → Meta Cloud API webhook POST to /api/method/frappe\_itsm.omnichannel.whatsapp\_webhook. Voice → Twilio/Exotel CTI screen pop via webhook. |
| :---: | :---- | :---- |

| 2 | Omnichannel Engine | Normalise to Conversation record All channels feed a common processing pipeline. Lookup: does this sender (email/phone/WhatsApp number) have an existing OPEN conversation? If yes → append message as ITSM Message. If no → create new ITSM Conversation \+ first ITSM Message. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On New Message Received ITSM Message record created: sender\_type, content, content\_type, sent\_at, channel\_message\_id (for dedup) Sentiment analysis: AI classifies message sentiment (Positive/Neutral/Frustrated/Angry) Frustrated/Angry conversations flagged in inbox with visual indicator for priority pickup If WhatsApp: HMAC-SHA256 webhook signature verified before processing |
| :---- |

## **7.3  Agent Inbox & Assignment Flow**

| 3 | Assignment Engine | Route conversation to team/agent Routing rules (from ITSM Automation Rule) assign conversation to team based on: channel, contact type, time of day, issue keywords. Within team: round-robin or least-loaded agent assignment. Agent presence status checked — Offline agents skipped. |
| :---: | :---- | :---- |

| 4 | Agent | Picks up conversation from Unified Inbox Agent sees all channels in single list sorted by: wait time, SLA risk, unread count. Click conversation → right panel shows full message history across ALL channels for this customer. Agent sees linked incidents, past requests, contact details. |
| :---: | :---- | :---- |

| 5 | Agent | Replies via same channel Reply box renders channel-appropriate editor: rich text for email, plain text for chat/WhatsApp. Quick replies (canned responses) available with Jinja variables. File attachment supported for all channels. Outbound WhatsApp: if within 24h window → free-form text; else → approved template required. |
| :---: | :---- | :---- |

| ◆  DECISION: Does this conversation need to become a formal ITSM record? ✅  YES → Agent clicks 'Create Incident' or 'Create Request'. Form pre-filled from conversation context. ITSM Incident / Service Request linked to conversation. ❌  NO  → Continue as conversation — resolve informally without creating incident |
| :---- |

## **7.4  Live Chat Widget Flow**

| 6 | Customer | Opens chat widget on website/portal Proactive chat trigger may fire based on: time on page (\> 30s), page URL (pricing/support pages), scroll depth (\> 70%). Widget shows greeting message. Pre-chat form captures name and email. |
| :---: | :---- | :---- |

| 7 | Virtual Agent (Bot) | Handles initial conversation Bot greets, identifies intent (check status, raise issue, request service, etc.). Handles top-10 intents autonomously via GPT-4o function calling. Each turn tracked as ITSM Bot Turn record. |
| :---: | :---- | :---- |

| ◆  DECISION: Bot can resolve the request? ✅  YES → Bot resolves (status check, KB answer, form fill). Session ends. CSAT prompt shown. Containment count incremented. ❌  NO  → Bot reaches max\_bot\_turns or detects 'speak to agent' intent → handoff to human agent |
| :---- |

| 8 | System | Bot-to-Human Handoff Bot sends handoff\_message. ITSM Conversation status updated. Assigned to handoff\_team queue. Agent desktop notified via Socket.io. Agent sees full bot transcript in conversation history. |
| :---: | :---- | :---- |

## **7.5  CSAT & Closure**

| 9 | System | Post-resolution CSAT survey sent On conversation status → Resolved: CSAT survey sent via original channel. Email: HTML survey link. WhatsApp: Interactive Message with star rating buttons. Chat: inline rating widget. CSAT score stored on conversation and linked to agent performance. |
| :---: | :---- | :---- |

| 🔗  CROSS-MODULE TOUCHPOINTS →  Incident Management: conversations escalate to incidents; incident replies sent via original channel →  Service Catalog: 'request\_service' bot intent → catalog browse and request submission →  Knowledge Base: bot searches KB for answers; chat widget shows KB suggestions →  AI / Virtual Agent: bot handles top-10 intents; sentiment analysis on every message →  Reporting: queue metrics (wait times, agent utilisation, abandoned rate) on Service Desk Dashboard →  ERPNext Customer: incoming contacts matched to ERPNext Customer record |
| :---- |

| 📊  MODULE KPIs ▸  Bot Containment Rate \= Sessions resolved by bot / Total sessions (target ≥ 30%) ▸  Average Wait Time \= Avg(first\_response\_at − first\_message\_at) per channel ▸  First Contact Resolution \= Conversations resolved in one session / Total conversations ▸  Abandoned Chat Rate \= Chats where customer left before agent pickup / Total chats (target \< 10%) ▸  Avg Concurrent Conversations per Agent \= Active chats / Active agents ▸  Channel Mix \= % of volume per channel (Email / Chat / WhatsApp / Voice) — monthly trend |
| :---- |

| MODULE 8 REPORTING & DASHBOARDS *KPIs · Analytics · Scheduled Reports · Drill-down* |
| :---: |

## **8.1  Data Flow Architecture**

| *All ITSM data lives in MariaDB on the same Frappe site. Dashboards query this data directly via custom REST API endpoints. No separate data warehouse required for v1. Reports are generated server-side; PDF export uses Frappe print engine; Excel export uses openpyxl.* |
| :---- |

## **8.2  Dashboard Rendering Flow**

| 1 | User | Opens dashboard page User navigates to /itsm/dashboard/{name}. Dashboard config (widget layout, filters, refresh rate) loaded from ITSM Dashboard DocType. Role-check: if user lacks Report Viewer role, dashboard inaccessible. |
| :---: | :---- | :---- |

| 2 | Frontend | Renders widget grid Vue component renders CSS grid. Each widget makes independent API call with date range \+ filter params. Widgets render in parallel — dashboard not blocked by slow widget. Loading skeleton shown per widget during data fetch. |
| :---: | :---- | :---- |

| 3 | Backend | API computes KPI data Each widget's API endpoint executes optimised SQL (with MariaDB FULLTEXT indexes). Results returned as JSON: current period value, previous period value, % change, chart data series, raw record count. |
| :---: | :---- | :---- |

| 4 | User | Drills down on chart segment User clicks bar/slice on chart. Click event passes filter parameters to ITSM list view URL (e.g., Incidents where priority=P1 AND sla\_status=Breached AND date\_range=last\_30\_days). Underlying records shown with full context. |
| :---: | :---- | :---- |

## **8.3  Scheduled Report Flow**

| 5 | ITSM Admin | Configure scheduled report Admin creates ITSM Scheduled Report: select report, date range (relative or absolute), format (PDF/Excel), schedule (daily/weekly/monthly), distribution list (email addresses or roles). |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Report Schedule Trigger Background job wakes at configured time Report query executed with configured date range PDF generated via Frappe print engine (wkhtmltopdf) Excel generated via openpyxl for tabular data Email sent to distribution list with file attachment ITSM Report Run Log entry created: timestamp, recipients, record count, file size |
| :---- |

## **8.4  KPI Alert Flow**

| 6 | ITSM Admin | Define KPI threshold alert Admin creates ITSM KPI Alert Rule: select KPI, comparator (\>, \<, \=), threshold value, notification recipients, notification frequency (once / every evaluation / daily digest). |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: Every 15 minutes — KPI Alert Evaluator Current KPI value computed for each active alert rule If condition met (e.g., SLA breach rate \> 10%): in-app notification created \+ email sent Repeat suppression: if same alert fired in last N hours, skip (configurable cooldown) |
| :---- |

| 🔗  CROSS-MODULE TOUCHPOINTS →  All modules contribute data to dashboards and reports →  SLA Engine: breach events, SLA compliance data consumed by SLA Compliance Report →  Incident Management: MTTR, FCR, volume by category/team/agent →  Change Management: success/failure rate, CAB cycle time, freeze violations →  Knowledge Base: deflection rate, helpfulness score, expiring articles →  Omnichannel: queue metrics, channel mix, agent utilisation, CSAT by channel →  Asset Management: inventory report, depreciation, warranty expiry forecast |
| :---- |

| 📊  MODULE KPIs ▸  Dashboard Load Time \= Avg time to render complete dashboard (target \< 3s at P95) ▸  Report Delivery Success Rate \= Reports delivered successfully / Scheduled (target 100%) ▸  KPI Alert Response Time \= Avg time from breach to notification delivery (target \< 20 min) ▸  Active Dashboard Users \= Weekly active report viewers / Total agents (adoption metric) |
| :---- |

| MODULE 9 AI & VIRTUAL AGENT *Classification · Reply Assist · Chatbot · Sentiment* |
| :---: |

## **9.1  AI Processing Architecture**

| *All AI features call external LLM APIs (OpenAI GPT-4o or Sarvam AI for Indian languages) via a provider abstraction layer. Every AI invocation is logged to ITSM AI Log (model used, input hash, output, accepted/rejected by agent). Provider can be switched without code changes. All PII sanitised before transmission.* |
| :---- |

## **9.2  Auto-Classification Flow**

| 1 | User / Agent | Creates new incident Incident saved with title and description filled but category/priority left blank (or agent submits and wants AI suggestion). |
| :---: | :---- | :---- |

| 2 | System | AI classifier invoked POST to LLM API with structured prompt: incident title \+ description → request JSON output: {category, sub\_category, impact, urgency, routing\_team}. Response parsed. If confidence \< threshold: no suggestion made. |
| :---: | :---- | :---- |

| 3 | Agent | Reviews and accepts/overrides suggestion Suggested values highlighted in form fields with 'AI Suggested' badge. Agent clicks Accept All / Accept Individual / Override. Decision recorded in ITSM AI Log for model accuracy tracking. |
| :---: | :---- | :---- |

## **9.3  Reply Assist Flow**

| 4 | Agent | Clicks 'Suggest Reply' on incident Button in reply editor toolbar. Context package built: incident title, description, current status, linked KB article IDs, resolution\_code of top-5 similar resolved incidents. |
| :---: | :---- | :---- |

| 5 | System | LLM generates draft reply GPT-4o called with system prompt (tone guidelines, company name, signature template) \+ context package. Draft reply returned in \< 5 seconds. Inserted into reply editor. |
| :---: | :---- | :---- |

| 6 | Agent | Edits and sends Agent reviews, adjusts draft, sends. Acceptance logged. Over time, accepted vs rejected ratio used for prompt optimisation. |
| :---: | :---- | :---- |

## **9.4  Virtual Agent (Chatbot) Flow**

| 7 | Customer | Sends message to chat/WhatsApp Message arrives at Omnichannel Engine. Active bot config checked for this channel. Bot takes ownership of conversation. |
| :---: | :---- | :---- |

| 8 | Bot | Intent extraction via LLM function calling GPT-4o with function calling: bot prompt includes list of registered functions (check\_ticket\_status, raise\_incident, request\_service, kb\_search, etc.). LLM selects function \+ extracts parameters from user message. |
| :---: | :---- | :---- |

| 9 | Bot | Executes function via Frappe API Python function handler called: queries ITSM Incident API / ITSM KB search / creates ITSM Incident. Result formatted as user-friendly message. Multi-turn: bot keeps context for up to max\_bot\_turns exchanges. |
| :---: | :---- | :---- |

| ◆  DECISION: User intent resolved within bot capabilities? ✅  YES → Bot confirms resolution. CSAT prompt. Conversation closed. Containment count \+1. ❌  NO  → Handoff to human agent: bot sends handoff\_message, assigns conversation to handoff\_team queue |
| :---- |

## **9.5  Duplicate Detection Flow**

| 10 | System | New incident saved Server-side hook: fetch open incidents same category \+ same raised\_by. Compare subjects using Levenshtein distance (or embedding cosine similarity). If similarity \> 70%: ITSM Duplicate Alert record created. |
| :---: | :---- | :---- |

| 11 | Agent | Reviews duplicate alert Alert banner shown on incident form: 'Possible duplicate of INC-2026-00123'. Agent can: Merge (copy activity to original, cancel this) / Link as Related / Dismiss (false positive logged for model improvement). |
| :---: | :---- | :---- |

| 🔗  CROSS-MODULE TOUCHPOINTS →  Incident Management: auto-classification, reply assist, summarisation, duplicate detection →  Omnichannel: bot deployed on chat and WhatsApp; sentiment analysis on every inbound message →  Knowledge Base: KB article suggestions during incident creation; bot searches KB →  Problem Management: anomaly detection triggers problem suggestion (Phase 2\) →  Reporting: AI Performance Dashboard — classification accuracy, containment rate, override rate |
| :---- |

| 📊  MODULE KPIs ▸  Classification Accuracy \= Agent-accepted AI suggestions / Total AI suggestions (target ≥ 80%) ▸  Bot Containment Rate \= Bot-resolved sessions / Total sessions (target ≥ 30%) ▸  Reply Assist Acceptance Rate \= Agent-sent AI drafts / Total suggestions shown ▸  Duplicate Detection Precision \= True duplicates found / Alerts raised (target ≥ 70%) ▸  Sentiment Alert Response \= Frustrated/Angry conversations picked up within 2 min / Total flagged |
| :---- |

| MODULE 10 ASSET MANAGEMENT *Hardware · Software · CMDB-Linked · Lifecycle · Compliance* |
| :---: |

## **10.1  Process Purpose**

| *Asset Management tracks every IT asset from purchase order to disposal. Hardware assets are automatically linked to CMDB CIs when deployed. Software licenses are tracked against deployment counts for compliance. Depreciation, warranty alerts, and disposal workflows create a complete financial and operational asset record.* |
| :---- |

## **10.2  Hardware Asset Lifecycle Flow**

| 1 | Procurement / Asset Manager | Asset Procurement Asset Manager creates ITSM Asset record on purchase. Links to ERPNext Purchase Order (purchase\_order field). Status \= On Order. purchase\_cost, warranty\_expiry, manufacturer, model, serial\_number recorded. |
| :---: | :---- | :---- |

| 2 | Asset Manager | Goods Received → In Stock PO goods receipt confirmed in ERPNext. ITSM Asset status → In Stock. Physical QR code label generated (Python qrcode library). Asset placed in stockroom location. |
| :---: | :---- | :---- |

| 3 | Asset Manager | Assign to User / Deploy Asset assigned to employee (assigned\_to link to ERPNext Employee). assigned\_date recorded. ITSM Asset Assignment History entry created. Status → In Use. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Asset Status → In Use CMDB check: search ITSM CI by serial\_number If CI found: link asset to existing CI (linked\_ci field) If CI not found: prompt to create CI from asset template (one-click CI creation) ERPNext Asset DocType created/linked for depreciation tracking |
| :---- |

| 4 | System | Depreciation calculated current\_nbv (Net Book Value) computed on each save: straight-line or written-down value method using purchase\_cost, useful\_life\_years, salvage\_value. ERPNext Asset Depreciation Schedule created for annual JE posting. |
| :---: | :---- | :---- |

| 5 | Technician | Asset sent for repair Status → In Repair. ITSM Incident raised for repair tracking. Vendor (ERPNext Supplier) linked. Return date tracked. On return: status → In Use. |
| :---: | :---- | :---- |

| 6 | Asset Manager | Asset Disposal Status → Retired first. Disposal request raised: disposal\_method selected (Sold/Donated/Scrapped/Certified Destruction). Approval required (configurable). On approval: disposal\_certificate upload mandatory. Status → Disposed. |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: On Asset Disposed Linked CMDB CI status → Retired ERPNext Asset residual value written off via Journal Entry Assignment history closed Disposal certificate archived to Frappe private files |
| :---- |

## **10.3  Software License Compliance Flow**

| 7 | Asset Manager | Register software license ITSM Software License record: product name, vendor, license\_type, license\_count\_purchased, version, expiry\_date, eol\_date. |
| :---: | :---- | :---- |

| 8 | System | Deployment count tracked license\_count\_deployed \= count of ITSM Asset Deployment records for this software (auto-computed). compliance\_status auto-calculated: Compliant / Over-Licensed (waste) / Under-Licensed (risk). |
| :---: | :---- | :---- |

| ⚡  AUTO-TRIGGER: Daily Background Job — Asset Alerts warranty\_expiry within 90 days → alert to CI owner \+ IT Manager (ITSM CI Alert created) amc\_expiry within 60 days → alert to Asset Manager Software license expiry within 90 days → alert to Asset Manager Software EoL within 180 days → alert with upgrade recommendation Under-Licensed software → immediate alert to ITSM Admin |
| :---- |

| 🔗  CROSS-MODULE TOUCHPOINTS →  CMDB: deployed asset → CI auto-created/linked; asset disposal → CI retired →  ERPNext: PO linked for procurement; ERPNext Asset for depreciation JEs →  Service Catalog: laptop/phone requests fulfilled from ITSM Asset stockroom →  Incident Management: hardware incidents link to affected asset CI →  Change Management: asset upgrade changes linked to affected CIs →  Reporting: Asset Inventory Report, depreciation NBV, license compliance, warranty forecast |
| :---- |

| 📊  MODULE KPIs ▸  Asset Utilisation \= Assets In Use / Total Active Assets (target ≥ 90%) ▸  License Compliance Rate \= Compliant software licenses / Total licenses (target 100%) ▸  Warranty Coverage \= Assets with active warranty / Total In Use (target ≥ 80%) ▸  Avg Asset Age \= Days since purchase\_date averaged across all In Use assets ▸  Disposal Cycle Time \= Avg days from Retired to Disposed status |
| :---- |

| MODULE 11 CROSS-MODULE INTEGRATION MAP *How All 10 Modules Connect* |
| :---: |

## **11.1  Master Integration Matrix**

| *Every cell in this matrix represents a data flow or trigger between two modules. This is the nervous system of the platform — understanding these connections is essential for developers to build each module correctly.* |
| :---- |

| From Module → | Incident Mgmt | Problem Mgmt | Change Mgmt | CMDB | Catalog | KB | Omnichannel | AI | Assets |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Incident Mgmt | — | Create Problem (PRB); linked incidents rollup | Link to causal change; incidents raised by change | Link affected CIs; CI impact fetched | — | KB article suggestions; deflection tracking | Conversation linked; replies via original channel | Auto-classify; duplicate detect; reply assist | — |
| Problem Mgmt | Auto-close linked incidents; workaround notification | — | Create RFC from problem; change notifies problem | Inherit CI links from incidents | — | Workaround → KB auto-draft; PIR → KB article | — | Anomaly detection triggers problem (Ph2) | — |
| Change Mgmt | Link incidents caused by change; failed change → incident | Link to problem being fixed | — | Affected CIs listed; CI change schedule tab | Standard changes as catalog items | — | Downtime notification via WhatsApp/email | — | Asset upgrade changes link CIs |
| CMDB | Link CIs to incidents; CI shows linked incidents | Link CIs to problems | Link CIs to changes; change schedule on CI | — | Hardware fulfillment → CI created | — | 'What systems affected?' answered from CMDB | — | Deployed asset → CI created/linked |
| Service Catalog | Fulfillment issues → incident | — | Standard change templates as catalog items | Hardware fulfillment creates CI | — | Catalog items link to KB articles | Request status via WhatsApp bot | — | Hardware fulfilled from asset stockroom |
| Knowledge Base | KB articles suggested in incident creation | Workaround KB article from problem | — | — | KB articles linked from catalog items | — | Bot searches KB for user answers | Semantic search enhances KB (Ph2) | — |
| Omnichannel | Conversation escalated to incident | — | — | — | Request\_service intent → catalog | Bot answers from KB | — | Sentiment analysis; bot NLU on messages | — |
| AI / VA | Auto-classify; summarise; reply assist | Auto problem from incident cluster (Ph2) | — | — | Request\_service intent fulfillment | KB search and suggestion | Chatbot on chat/WhatsApp; handoff | — | — |
| Assets | Asset incidents link to CI | — | Asset upgrade → RFC | Asset deployed → CI linked | Asset request via catalog | — | — | — | — |

## **11.2  SLA Engine — Cross-Module Service**

The SLA Engine serves all ticketing modules (Incident, Service Catalog RITM, optionally Problem). It is a shared service, not tied to any single module.

| Event | SLA Engine Action | Modules Served |
| :---- | :---- | :---- |
| New Incident created | Create ITSM SLA Instance; calculate response\_due and resolution\_due using working hours \+ holiday list | Incident Management |
| New RITM created (catalog) | Create ITSM SLA Instance with sla\_hours from Catalog Item; track fulfillment deadline | Service Catalog |
| Incident status → Pending | Pause SLA timer; record on\_hold\_since; create ITSM SLA Hold Log | Incident, Catalog |
| Incident status → In Progress (from Pending) | Resume timer; subtract hold duration from elapsed time | Incident, Catalog |
| SLA 50% elapsed | Notify assigned agent | Incident, Catalog |
| SLA 75% elapsed | Notify agent \+ team lead; set sla\_status \= At Risk | Incident, Catalog |
| SLA 100% elapsed (breach) | Set sla\_status \= Breached; L1 escalation: reassign \+ notify IT Manager | Incident, Catalog |
| Incident Resolved or Closed | Finalise SLA compliance status; update KPI data | Incident, Catalog |

## **11.3  Workflow / Automation Engine — Cross-Module Service**

The Workflow Automation Engine serves all modules as a configurable automation layer. No hardcoded business rules — all routing, notification, and escalation logic lives in ITSM Automation Rule records.

| Automation Example | Trigger | Actions | Module |
| :---- | :---- | :---- | :---- |
| P1 Incident → Immediate Alert | Incident Created, Priority=P1 | Send WhatsApp to On-Call Manager, Assign to P1 Team, Post internal comment | Incident |
| Pending \> 24h without reply | Scheduled: every 1h, Incident Pending \> 24h | Send email to requester: 'Are you still waiting?', Post reminder comment | Incident |
| Change CAB approval reminder | Scheduled: 4h before CAB meeting | Send email to CAB members with agenda link | Change |
| New catalog item published | Catalog Item status → Active | Send email to target department announcing new service | Catalog |
| KB article low rating | KB Feedback created, not\_helpful\_count \> 5 | Notify article author, flag on KB dashboard | Knowledge Base |
| Asset warranty expiry | Scheduled: daily, warranty\_expiry within 90 days | Create CI alert, email CI owner and IT Manager | Assets / CMDB |

