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

## Phase 1: ITSM Core
**Duration:** Weeks 1–12 (3 months)
**Focus:** Foundational architecture, Core Ticketing, and SLA Management.

### Key Deliverables:
- **Core Architecture:** Setup `frappe_itsm` app scaffold, DocType scaffolding, Frappe hooks, naming series, and base permission roles.
- **Incident Management:** Full implementation of `ITSM Incident` DocType, Incident state machine (Frappe Workflow), Priority Matrix, Impact x Urgency logic.
- **SLA Engine:** `ITSM SLA Policy`, `ITSM SLA Instance`, working hours, holiday lists, response/resolution due calculation, background evaluator jobs, and escalation engine.
- **Problem Management:** Full implementation of `ITSM Problem`, RCA form (5-Whys, Fishbone), KEDB lookup, workaround publishing, and problem tasks.
- **Change Management:** Full implementation of `ITSM Change`, risk assessment calculation, CAB meeting management, blackout window validation, and rollback workflows.
- **Portals & Reporting:** Basic Agent Portal (Vue SPA), Employee Self-Service Portal v1, Operations Dashboard, SLA Compliance Report, Change Management Dashboard, and Email integration.
- **Automation:** Basic Workflow Engine (Automation rules with basic action types).

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
