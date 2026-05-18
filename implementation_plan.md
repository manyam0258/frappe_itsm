# Phase-Wise Implementation Plan: frappe_itsm

Based on the Product Requirements Document (PRD) for the `frappe_itsm` custom app, here is the proposed phased implementation plan. This aligns with the phased delivery roadmap described in the PRD, breaking the project into 4 distinct phases spanning 36 weeks.

## User Review Required
> [!IMPORTANT]
> Please review the phasing and timeline. Ensure that the dependencies on ERPNext data (Company, Employee, Customer, etc.) are available for Phase 1. 

## Open Questions
> [!NOTE]
> 1. Do you have a specific test environment (staging site) already provisioned for Phase 1 deployments?
> 2. Have the WhatsApp Meta Business API approvals been initiated? (This is a known risk mentioned in the PRD taking 6-8 weeks).

---

# Immediate Execution Plan: Phase 1 Sprint 4+
*Focus: Problem Management, Change Management, and Vue 3 Portals.*

## Proposed Changes

### Problem Management
We will create the core DocTypes to handle Problem lifecycles and Root Cause Analysis.
- **[NEW] DocType `ITSM Problem`**: Includes fields for Category, Priority, status, workaround, and RCA details.
- **[NEW] DocType `ITSM Problem Incident`**: Child table mapping problems to multiple incidents.
- **[NEW] DocType `ITSM Problem Task`**: Child table for assigning parallel investigation tasks.
- **[NEW] Python Logic**: Auto-create KB Draft when `workaround_published` is checked.

### Change Management
We will build out the ITIL v4 Change Enablement workflow, CAB management, and Risk calculation.
- **[NEW] DocType `ITSM Change`**: Core RFC tracking with Change Types (Standard, Normal, Emergency), Risk Level, and Rollback Plans.
- **[NEW] DocType `ITSM Change Task`**: Tasks for pre, impl, and post phases.
- **[NEW] DocType `ITSM CAB Meeting`**: For scheduling CABs. Includes child tables for `ITSM CAB Member` and `ITSM CAB Agenda Item`.
- **[NEW] DocType `ITSM Blackout Window`**: To define restricted deployment periods.
- **[NEW] Python Logic**: 
  - *Risk Calculation*: Auto-calculate `risk_score` from the risk assessment questionnaire.
  - *Blackout Validation*: Server script to warn/block if Change `start_datetime` to `end_datetime` overlaps with an active Blackout Window.

### Portals & Reporting
We will configure the `frontend/` Vue 3 SPA using `frappe-ui`.
- **[NEW] Vue Router**: Setup routes for `/agent` (Agent Portal) and `/self-service` (Employee Portal).
- **[NEW] Agent Portal Views**: Incident List, Problem List, Change List, and a central Dashboard component.
- **[NEW] Employee Portal Views**: Landing page, "My Tickets" tracker, and a Ticket Submission form.

## Verification Plan
### Playwright E2E Test Suite (Next Immediate Step)
To fully complete Phase 1, we will implement comprehensive end-to-end testing using Playwright in the `frappe-itsm-tests` directory.

#### Test 1: Incident Lifecycle & SLA (`tests/incident_lifecycle.spec.js`)
- **API/UI Flow:** Agent creates an Incident -> Workflow transition to 'Assigned' -> 'In Progress' -> 'Resolved' -> 'Closed'.
- **Validation:** SLA Response and Resolution timers are started, evaluated, and correctly logged in `ITSM SLA Instance`. Priority auto-calculation is verified.

#### Test 2: Problem Lifecycle & KEDB (`tests/problem_lifecycle.spec.js`)
- **API/UI Flow:** Problem is created -> Incident is linked -> RCA (5-Whys) is filled out -> Workaround is published.
- **Validation:** The Python trigger correctly creates a Draft `ITSM Knowledge Article` when the workaround is published.

#### Test 3: Change Enablement & CAB (`tests/change_lifecycle.spec.js`)
- **API/UI Flow:** Normal Change is submitted -> Risk Assessment is filled -> Workflow transitions to 'Pending Review' -> 'CAB Scheduled'.
- **Validation:** Risk Score is accurately calculated (0-100) and mapped to Risk Level. Blackout window validation throws a warning if dates overlap.

#### Test 4: Vue 3 Portals UI (`tests/portals_ui.spec.js`)
- **UI Flow:** End-User accesses the Employee Portal -> Raises a Ticket -> Navigates to "My Tickets" -> Agent logs into Agent Portal -> Dashboard loads -> Incident List displays the newly raised ticket.
- **Validation:** The Vue router functions correctly, and data bindings successfully pull from Frappe REST APIs.

---

## Phase 1: ITSM Core
**Duration:** Weeks 1–12 (3 months)
**Focus:** Foundational architecture, Core Ticketing, and SLA Management.

### Key Deliverables & Sprints:
- **Sprint 1 (Core Architecture):** Setup `frappe_itsm` app scaffold, DocType scaffolding, Frappe hooks, naming series, and base permission roles.
- **Sprint 2 (Incident Management):** Full implementation of `ITSM Incident` DocType, Incident state machine (Frappe Workflow), Priority Matrix, Impact x Urgency logic.
- **Sprint 3 (SLA Engine):** `ITSM SLA Policy`, `ITSM SLA Instance`, working hours, holiday lists, response/resolution due calculation, background evaluator jobs, and escalation engine.
- **Sprint 4 (Portals & Vue SPA):** Setup `frappe-ui` frontend, build Agent Portal (Vue SPA), Employee Self-Service Portal v1, Operations Dashboard, and basic API endpoints for Vue integration. *(Problem & Change management deferred to Phase 1.5/Sprint 5 to focus purely on the frontend delivery).*

---

## Phase 2: Catalog + CMDB
**Duration:** Weeks 13–20 (2 months)
**Focus:** Self-Service, Asset Tracking, and ERPNext Integration.

### Key Deliverables:
- **Service Catalog:** Full implementation of `ITSM Catalog Item`, `ITSM Request Item` (RITM), dynamic catalog variables, multi-stage approvals, and shopping cart experience.
- **CMDB:** Full implementation of `ITSM CI`, CI class hierarchy, relationship mapping, visual D3.js impact analysis graph, and CI lifecycle management.
- **Asset Management:** Full implementation of `ITSM Asset`, procurement tracking, hardware/software lifecycle, depreciation calculation, ERPNext Asset integration, and QR code generation.
- **Knowledge Base:** Full article lifecycle, KEDB integration, internal vs public visibility, deflection tracking, and feedback/ratings.
- **Advanced SLA & Reporting:** Advanced SLA (OLAs, complex escalation chains) and completion of all 10 standard dashboards.

---

## Phase 3: Omnichannel
**Duration:** Weeks 21–28 (2 months)
**Focus:** Unified Agent Inbox and Multi-Channel Communication.

### Key Deliverables:
- **Unified Inbox:** Omnichannel core (`ITSM Conversation`, `ITSM Message`), real-time Vue SPA inbox using Socket.io and Redis pub/sub.
- **Live Chat:** Web widget for live chat with typing indicators and file sharing.
- **WhatsApp Integration:** Meta Cloud API integration, WhatsApp message templates, and CSAT via WhatsApp.
- **Voice CTI:** Integration with Twilio/Exotel for voice calls and screen pops.
- **Portals:** Customer Portal (full feature set with ticket tracking and chat widget).
- **CSAT Engine:** Post-resolution CSAT surveys sent via the original channel (Email/WhatsApp/Chat).

---

## Phase 4: AI + Polish
**Duration:** Weeks 29–36 (2 months)
**Focus:** AI Enhancements, External Integrations, and Go-Live.

### Key Deliverables:
- **AI Classification & Suggestions:** Auto-classification of intent/priority, KB article suggestion during ticket creation.
- **Agent Assist:** LLM-powered reply assist, ticket summarisation for handoffs, and sentiment analysis for inbound messages.
- **Virtual Agent:** Chatbot handling top-10 self-service intents, with bot-to-human handoff capabilities.
- **Integrations:** Azure AD SSO, Jira integration (syncing Incidents/Bugs), and generic webhook receivers for monitoring tools (Grafana, PagerDuty, Zabbix).
- **Final Polish:** Performance tuning, security penetration testing, duplicate detection, UAT, and production deployment.

## Verification Plan
### Automated Tests
- End-to-end tests for all core processes (Incident lifecycle, Change CAB approvals, SLA calculations).
- k6 load testing for 300+ concurrent users on the Agent Portal.
- Automated API checks for email-to-incident latency and WebSocket real-time delivery.

### Manual Verification
- UAT sessions with IT Managers, Agents, and End Users.
- Verification of ERPNext data sync and AI Virtual Agent accuracy.
