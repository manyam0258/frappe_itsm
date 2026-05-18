

**PRODUCT REQUIREMENTS DOCUMENT**

frappe\_itsm — Enterprise ITSM & Change Management Platform

*ServiceNow-Parity Custom Frappe App · Built from Scratch*

| Field | Value |
| :---- | :---- |
| Document ID | ITSM-PRD-2026-001 |
| Version | 1.0 — DRAFT |
| Classification | CONFIDENTIAL — Internal |
| App Name | frappe\_itsm |
| Frappe Framework | v15+ |
| ERPNext | v15+ (same site) |
| Target Users | 100–500 (all user types) |
| ITIL Alignment | ITIL v4 |
| ISO Compliance | ISO/IEC 20000-1:2018 |
| Date | May 2026 |
| Prepared By | Product & Engineering |
| Status | Pending Review |

# **1\. Document Control**

## **1.1 Revision History**

| Version | Date | Author | Change Description |
| :---- | :---- | :---- | :---- |
| 1.0 | May 2026 | Product Team | Initial PRD — all modules |

## **1.2 Stakeholders & Reviewers**

| Role | Name / Team | Review Area |
| :---- | :---- | :---- |
| Product Owner | Engineering Lead | All sections |
| Tech Lead | Backend Developer | Architecture, DocTypes, Integrations |
| Frontend Lead | Frontend Developer | UI/UX, Portal design, Vue components |
| QA Lead | QA Engineer | Acceptance criteria, test coverage |
| Business Analyst | BA Team | Business rules, workflows, ITIL compliance |
| ITIL Consultant | External / Internal | ITIL v4 process alignment |

## **1.3 Definitions of Priority**

| Priority | Meaning | Must be in v1? |
| :---- | :---- | :---- |
| Must Have | Core functionality — app is unusable without it | Yes |
| Should Have | High-value feature, strong business case | Yes (if capacity allows) |
| Nice to Have | Enhances UX, low risk to defer | No — Phase 2+ |
| Out of Scope | Explicitly excluded from this PRD | No |

# **2\. Executive Summary**

## **2.1 Problem Statement**

Organisations across real estate, hospitality, manufacturing, and services sectors manage IT operations, internal service requests, and infrastructure changes through disconnected tools — email threads, Excel trackers, WhatsApp groups, and legacy ticketing systems. This creates:

* Zero visibility into SLA compliance — no way to know if tickets are breached

* No structured change management — changes deployed without risk assessment, CAB review, or rollback plans

* Fragmented communication — customer/employee queries arrive via 5+ channels with no unified inbox

* No audit trail — compliance with ITIL v4 and ISO 20000 impossible to demonstrate

* Manual reporting — management dashboards produced manually in Excel weekly

## **2.2 Solution Overview**

| *frappe\_itsm is a custom Frappe application built entirely from scratch that delivers ServiceNow-parity ITSM capabilities — natively integrated on the same Frappe/ERPNext site, without per-seat licensing, vendor lock-in, or multi-system sprawl.* |
| :---- |

The app delivers 10 integrated modules on a single Frappe site:

| \# | Module | Key Capability | ServiceNow Equivalent |
| :---- | :---- | :---- | :---- |
| 1 | Incident Management | Full ticket lifecycle, SLA, escalation chains, major incident | INC / ITSM |
| 2 | Problem Management | RCA, KEDB, workaround publishing, known error lifecycle | PRB |
| 3 | Change Management | Standard/Normal/Emergency RFC, CAB, risk scoring, change calendar, PIR | CHG |
| 4 | CMDB | CI class hierarchy, relationships, impact analysis, discovery | CMDB |
| 5 | Service Catalog | Self-service portal, catalog items, approval workflows, RITM | Service Catalog |
| 6 | Knowledge Base | Article lifecycle, categories, self-service deflection, feedback | KM |
| 7 | Omnichannel | Email, live chat, WhatsApp, voice — unified agent inbox | CSM Omnichannel |
| 8 | Reporting & Dashboards | KPI dashboards, SLA reports, executive analytics, scheduled reports | Performance Analytics |
| 9 | AI / Virtual Agent | Chatbot, intent classification, KB suggestion, reply assist | Now Assist / VA |
| 10 | Asset Management | Hardware/software lifecycle, CMDB-linked, depreciation, compliance | ITAM |

## **2.3 Key Design Principles**

* ITIL v4 aligned — all processes map to ITIL v4 service value chain practices

* ERPNext-native — uses shared Company, Customer, Employee, User, and Item DocTypes; no data duplication

* Single codebase — one custom Frappe app (frappe\_itsm), zero dependency on Frappe Helpdesk

* Role-first design — every screen, field, and action is governed by Frappe's role permission engine

* API-first — every entity exposes REST APIs consumed by portals and integrations

* Configurable, not coded — SLA policies, escalation rules, approval workflows, and routing rules are data, not code

* Audit-complete — every state change, field edit, and approval logged with user, timestamp, and before/after values

# **3\. Scope Definition**

## **3.1 In Scope — v1**

| Module | In Scope Features | Out of Scope (deferred) |
| :---- | :---- | :---- |
| Incident Mgmt | Creation via all channels, priority matrix, SLA timers, multi-level escalation, major incident, parent-child linking, resolution, closure | Predictive MTTR |
| Problem Mgmt | Full RCA workflow, KEDB, workaround KB publishing, problem tasks, PIR | Auto-problem creation from incident clusters (AI) |
| Change Mgmt | Standard/Normal/Emergency RFC, multi-level CAB, risk scoring, change calendar, blackout windows, change tasks, PIR, rollback plan | DevOps CI/CD integration, auto-RFC from pipeline |
| CMDB | CI class hierarchy, relationships, impact analysis, bulk import, CI linking on ITSM records, audit trail | Auto-discovery agent, network scanning |
| Service Catalog | Catalog builder, variable types, multi-stage approval, RITM, shopping cart, fulfillment tasks, SLA per item | External e-commerce integration |
| Knowledge Base | Article lifecycle (draft→published→retired), categories, ratings, version history, portal embedding, keyword search | AI-powered semantic search (Phase 2\) |
| Omnichannel | Email (multi-account), live chat widget, WhatsApp Business API, voice (Twilio/Exotel), unified agent inbox | Facebook/Instagram/Twitter DMs, SMS |
| Reporting | 10 pre-built dashboards, KPI widgets, SLA compliance reports, scheduled email reports, export PDF/Excel | External BI connector (Power BI/Tableau) |
| AI / VA | Intent classification, KB article suggestion, reply assist, chatbot for top-10 intents, sentiment analysis | Full NLU training pipeline, voice bot |
| Asset Mgmt | Asset lifecycle, hardware/software tracking, CMDB linkage, depreciation, warranty alerts, assignment tracking | Software license reconciliation automation |
| Integrations | ERPNext (native), Email IMAP/SMTP, WhatsApp Business API, Twilio voice, Azure AD SSO, Jira (basic sync) | PagerDuty, Grafana, ServiceNow migration |

## **3.2 Assumptions & Dependencies**

* Frappe Framework v15+ and ERPNext v15+ installed on the same bench site

* Python 3.11+, Node.js 18+, MariaDB 10.6+, Redis 7+

* WhatsApp Business API access approved via Meta (allow 6–8 weeks for verification)

* Twilio or Exotel account with active SIP trunk for voice integration

* Azure AD / Okta tenant available for SSO configuration

* ERPNext base data exists: Company, Department, Employee, Customer records

* ITIL v4 process owner named within the organisation before go-live

* ISO 20000 audit trail requirements reviewed with compliance team before UAT

# **4\. User Roles, Personas & Portals**

## **4.1 Role Hierarchy**

| *All roles are Frappe Roles assigned via Role Profile. Roles are additive — a user can have multiple roles. The permission engine enforces DocType-level, document-level, and field-level access.* |
| :---- |

| Role Name | Frappe Role ID | Description | Portal Access |
| :---- | :---- | :---- | :---- |
| Super Admin | ITSM Super Admin | Full system access — configuration, all modules, all records | Admin Portal \+ All Portals |
| ITSM Admin | ITSM Admin | Module configuration, SLA policies, routing rules, catalog management | Admin Portal |
| IT Manager | ITSM Manager | All incidents/problems/changes in assigned teams, reports, dashboards | Agent Portal \+ Reports |
| Change Manager | ITSM Change Manager | Full change management — RFC approval, CAB scheduling, blackout windows | Agent Portal (Change) |
| CAB Member | ITSM CAB Member | Review and vote on Normal/Emergency changes in CAB meetings | Agent Portal (Change Review) |
| Senior Agent | ITSM Senior Agent | All tickets in assigned teams, escalation authority, knowledge authoring | Agent Portal |
| Agent | ITSM Agent | Assigned tickets only, reply, update status, create comments | Agent Portal |
| Knowledge Author | ITSM Knowledge Author | Create and publish KB articles, manage categories | Agent Portal (KB) |
| Field Technician | ITSM Field Tech | Assigned work orders, update status, capture parts, mobile view | Mobile / Agent Portal (limited) |
| Employee (Requester) | ITSM Employee | Raise tickets, service requests, track own records | Employee Self-Service Portal |
| External Customer | ITSM Customer | Raise support tickets, track status, access public KB | Customer Portal |
| Vendor | ITSM Vendor | View assigned vendor tasks, update status, upload delivery notes | Vendor Portal (limited) |
| Report Viewer | ITSM Report Viewer | Read-only dashboards and reports — no ticket operations | Reports Portal |

## **4.2 Portal Architecture — 4 Portals**

| Portal | URL Path | Primary Users | Key Features |
| :---- | :---- | :---- | :---- |
| Agent Portal | /itsm | Agents, Senior Agents, IT Managers, Change Manager | Unified inbox, ticket management, change calendar, CMDB, reports, KB authoring |
| Employee Self-Service | /itsm/portal | Internal employees, HR staff | Raise tickets, service requests, check status, access KB, CSAT feedback |
| Customer Portal | /itsm/support | External customers, partners | Submit support tickets, track status, chat widget, public KB |
| Admin Portal | /itsm/admin | ITSM Admin, Super Admin | SLA config, routing rules, catalog builder, user management, system settings |

## **4.3 User Personas**

### **Persona 1 — Priya (IT Manager)**

| Attribute | Detail |
| :---- | :---- |
| Role | IT Manager — oversees 5-agent helpdesk |
| Goals | SLA compliance \> 90%, zero unauthorized changes, weekly report to CTO |
| Pain Points | No visibility into ticket queue depth; change failures disrupt production; manual Excel reports take 2 hours/week |
| Key Screens | Operations dashboard, SLA breach list, change calendar, team utilization report |

### **Persona 2 — Rajan (Senior IT Agent)**

| Attribute | Detail |
| :---- | :---- |
| Role | Senior Helpdesk Agent — handles P1/P2 incidents, mentors junior agents |
| Goals | Resolve P1s within 1 hour, access full CI impact data, quickly find KB workarounds |
| Pain Points | Switching between 4 tools (email, Jira, WhatsApp, Excel) to handle one incident; no CMDB to see what's affected |
| Key Screens | Unified inbox, incident detail, CMDB relationship map, saved replies |

### **Persona 3 — Ananya (Employee / Requester)**

| Attribute | Detail |
| :---- | :---- |
| Role | Marketing Manager — raises IT requests for team |
| Goals | Submit requests quickly without calling IT; see real-time status; not wait for email replies |
| Pain Points | No self-service — must email IT and wait; no idea when laptop will arrive; can't track request |
| Key Screens | Service catalog, request status tracker, ticket history, KB search |

### **Persona 4 — Thomas (Change Manager)**

| Attribute | Detail |
| :---- | :---- |
| Role | Change Manager — owns RFC lifecycle, chairs CAB meetings |
| Goals | Zero unauthorized changes, \< 2% failed changes, automated risk scoring, change calendar always current |
| Pain Points | CAB approvals done via email replies — no audit trail; change calendar in Excel; no conflict detection between changes |
| Key Screens | Change calendar, CAB dashboard, RFC detail, risk matrix, PIR tracker |

### **Persona 5 — Mehul (External Customer)**

| Attribute | Detail |
| :---- | :---- |
| Role | Operations head at a client company — raises support tickets |
| Goals | Fast resolution, real-time status updates via WhatsApp, self-serve KB for common issues |
| Pain Points | No visibility after submitting ticket; follow-up requires calling support; no knowledge base for common questions |
| Key Screens | Customer portal, ticket status page, WhatsApp chat, CSAT feedback form |

# **5\. System Architecture**

## **5.1 App Structure**

| *frappe\_itsm is a single custom Frappe app installed alongside ERPNext. App directory: frappe-bench/apps/frappe\_itsm/. All DocTypes, Workflows, Server Scripts, Web Templates, and API endpoints live within this app namespace.* |
| :---- |

| App Layer | Component | Technology | Notes |
| :---- | :---- | :---- | :---- |
| App Core | DocTypes, Workflows, Server Scripts | Python / Frappe ORM | \~80 DocTypes across 10 modules |
| Frontend — Agent Portal | Vue 3 SPA | Vue 3 \+ Vite \+ Frappe UI | Served from /itsm, auth via Frappe session |
| Frontend — Self-Service | Frappe Web Pages \+ Vue components | Jinja \+ Vue widgets | /itsm/portal — employee & customer portals |
| Frontend — Admin | Vue 3 SPA | Vue 3 \+ Frappe UI | Configuration screens, served from /itsm/admin |
| Real-time Layer | WebSocket events | Socket.io (Frappe built-in) \+ Redis pub/sub | Live chat, real-time queue updates, typing indicators |
| Background Jobs | Async workers | Frappe RQ (Redis Queue) \+ Celery-compatible | SLA timer evaluation, escalation engine, email fetch, report generation |
| Database | MariaDB 10.6+ | Frappe ORM | Shared with ERPNext — all DocTables in same DB |
| Cache | Redis 7+ | Frappe cache layer | Session cache, permission cache, rate limiting, chat message buffer |
| File Storage | Frappe private/public files or S3 | MinIO or AWS S3 | Attachments, CI images, KB article images |
| API Layer | REST API \+ Webhooks | Frappe REST (auto-generated) \+ custom API endpoints | Every DocType auto-exposes CRUD REST; custom endpoints for AI, chat, voice |
| Search | MariaDB FULLTEXT \+ custom indexing | Frappe search \+ custom SQL | Ticket search, KB search; Phase 2: Meilisearch/Typesense |

## **5.2 ERPNext Integration Points**

| ERPNext DocType | Used In frappe\_itsm | How Integrated | Sync Direction |
| :---- | :---- | :---- | :---- |
| Company | All modules — company context | Shared DocType, read-only in ITSM | ERPNext → ITSM |
| Employee | Agent, Requester, Field Tech profiles | Link field to Employee; fetch department, designation, manager | ERPNext → ITSM |
| Customer | External customer tickets | Link to Customer DocType; inherit contacts | ERPNext → ITSM (read) |
| Department | Team, SLA policy, routing rules | Link field — filter agents by department | ERPNext → ITSM |
| User | All roles use Frappe User | Shared auth; ITSM roles assigned to User | Shared |
| Item | Asset catalog, catalog item cost | Link to Item for asset tracking | ERPNext → ITSM |
| Purchase Order | Hardware asset procurement | PO number linked to asset record | ERPNext → ITSM |
| Journal Entry | Depreciation entries for assets | Auto JE creation on depreciation posting | ITSM → ERPNext |
| HR Leave Application | ITSM working hours respect leave calendar | API call to check agent availability | ERPNext → ITSM (read) |

## **5.3 Data Flow — Ticket Lifecycle**

The following summarises how a ticket flows through the system from submission to closure:

* Submission: Customer/employee submits via portal, email, WhatsApp, chat widget, or voice (CTI pop)

* Channel ingestion: Omnichannel engine normalises all inputs into a Conversation record with a linked Incident/Request record

* Classification: AI classifier suggests Category, Sub-category, Priority, and Routing Team (agent reviews and accepts)

* SLA assignment: SLA Engine evaluates active SLA policies against ticket fields and assigns matching SLA Instance

* Assignment: Assignment Engine applies routing rules → auto-assigns to team or individual agent

* Work: Agent works ticket — updates, sends replies via omnichannel, links CI, adds work notes

* Escalation: SLA timer events trigger escalation notifications and optional auto-reassignment

* Resolution: Agent marks resolved → resolution triggers CSAT survey via original channel

* Closure: System auto-closes after configurable period (default 72h) unless re-opened by requester

* Audit: Every transition, field change, and communication logged to Audit Log with user \+ timestamp

## **5.4 Technology Stack**

| Category | Technology | Version | Rationale |
| :---- | :---- | :---- | :---- |
| Backend | Python \+ Frappe Framework | Python 3.11 / Frappe v15 | Core platform — DocType ORM, permission engine, REST API, hooks |
| Frontend (Vue) | Vue 3 \+ Vite \+ TypeScript | Vue 3.4+ | Modern reactive UI, consistent with Frappe ecosystem |
| UI Components | Frappe UI \+ custom components | Latest | Pre-built Frappe UI components; custom ITSM-specific components |
| Database | MariaDB | 10.6+ | Frappe-standard; shared with ERPNext |
| Cache / Queue | Redis \+ Frappe RQ | Redis 7 / RQ 1.x | Background jobs, WebSocket pub/sub, rate limiting |
| Real-time | Socket.io (Frappe built-in) | Frappe-provided | Live chat, real-time queue updates |
| Email | Python smtplib / imaplib via Frappe | Frappe email engine | Multi-account email; SendGrid for bulk |
| Voice | Twilio SDK / Exotel REST API | Latest | CTI integration, call pop, call recording |
| WhatsApp | Meta Cloud API / Twilio for WhatsApp | Graph API v18+ | Inbound/outbound WhatsApp messaging |
| AI / NLU | OpenAI GPT-4o API \+ Sarvam AI | Latest | Classification, reply assist, KB suggestion; Sarvam for Indian langs |
| Vector Search | pgvector (MariaDB extension or Postgres sidecar) | Latest | KB semantic search, similar incident lookup |
| Auth | Frappe Auth \+ OAuth2 \+ SAML 2.0 | Frappe v15 built-in | Session auth \+ Azure AD/Okta SSO |
| Monitoring | Frappe's built-in monitoring \+ custom dashboards | — | App-level; ops monitoring via Grafana (separate) |
| Mobile | Progressive Web App (PWA) \+ React Native (Phase 3\) | — | PWA first for field tech; native app Phase 3 |

# **6\. Module 1 — Incident Management**

## **6.1 Process Overview**

| *Incident Management restores normal service operation as quickly as possible with minimum disruption. Every service disruption or degradation — regardless of channel — is captured as an Incident record (INC-YYYY-NNNNN) and tracked through a defined lifecycle with SLA accountability.* |
| :---- |

## **6.2 DocType: ITSM Incident**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | Incident ID | Data | Auto: INC-{YYYY}-{\#\#\#\#\#} | Yes | System-generated naming series |
| title | Subject | Data | — | Yes | One-line description of the issue |
| description | Description | Text Editor | — | Yes | Full rich-text description; supports images, attachments |
| status | Status | Select | New,Assigned,In Progress,Pending,Resolved,Closed,Cancelled | Yes | Current lifecycle state |
| incident\_type | Incident Type | Select | Service Request,Incident,Major Incident | Yes | Type classification |
| category | Category | Link | ITSM Category | Yes | Top-level category (e.g., Network, Hardware, Application) |
| sub\_category | Sub-Category | Link | ITSM Sub Category | Yes | Filtered by category |
| item\_affected | Item Affected | Data | — | No | Specific item/system name |
| impact | Impact | Select | 1-Enterprise Wide,2-Department Wide,3-Group Wide,4-Individual | Yes | Scope of impact |
| urgency | Urgency | Select | 1-Critical,2-High,3-Medium,4-Low | Yes | Speed of resolution needed |
| priority | Priority | Select | P1-Critical,P2-High,P3-Moderate,P4-Low,P5-Planning | Yes | Auto-calculated from Impact × Urgency matrix |
| raised\_by | Raised By | Link | User | Yes | User who submitted the incident |
| caller | Caller | Link | User | No | User on whose behalf the ticket is raised (if different) |
| contact\_email | Contact Email | Data | Email | No | Alternate email for updates |
| contact\_phone | Contact Phone | Data | Phone | No | Alternate phone |
| assigned\_team | Assigned Team | Link | ITSM Team | No | Team responsible for resolution |
| assigned\_to | Assigned To | Link | User | No | Individual agent assigned |
| company | Company | Link | Company | Yes | From ERPNext Company |
| department | Department | Link | Department | No | Requester's department |
| source\_channel | Source Channel | Select | Email,Web Portal,WhatsApp,Chat,Phone,Walk-in,API | Yes | How the incident was received |
| parent\_incident | Parent Incident | Link | ITSM Incident | No | For child incidents under a major incident |
| is\_major\_incident | Is Major Incident | Check | — | No | Flag: enables major incident workflow |
| major\_incident\_manager | Major Incident Manager | Link | User | No | Visible when is\_major\_incident=1 |
| linked\_cis | Linked CIs | Table | ITSM Incident CI (child) | No | Configuration Items affected |
| linked\_problem | Linked Problem | Link | ITSM Problem | No | Root cause problem record |
| linked\_change | Linked Change | Link | ITSM Change | No | Change that caused this incident |
| workaround | Workaround | Text Editor | — | No | Temporary workaround if known |
| resolution\_notes | Resolution Notes | Text Editor | — | No | How the incident was resolved |
| resolution\_code | Resolution Code | Link | ITSM Resolution Code | No | Standard resolution classification |
| reopened\_count | Reopened Count | Int | — | No | Auto-incremented on reopen; affects SLA metric |
| closed\_at | Closed At | Datetime | — | No | Auto-set on closure |
| resolution\_at | Resolved At | Datetime | — | No | Auto-set on resolution |
| first\_response\_at | First Response At | Datetime | — | No | Timestamp of first public reply |
| sla\_policy | SLA Policy | Link | ITSM SLA Policy | No | Auto-assigned by SLA engine |
| response\_due | Response Due | Datetime | — | No | Calculated deadline for first response |
| resolution\_due | Resolution Due | Datetime | — | No | Calculated deadline for resolution |
| sla\_status | SLA Status | Select | Within SLA,At Risk,Breached,Paused,Fulfilled | No | Evaluated by SLA timer job |
| on\_hold\_reason | On Hold Reason | Select | Awaiting User,Awaiting Vendor,Awaiting Change,Scheduled Maintenance,Other | No | Required when status=Pending |
| on\_hold\_since | On Hold Since | Datetime | — | No | SLA timer paused from this timestamp |
| csat\_sent | CSAT Sent | Check | — | No | Whether post-resolution survey was triggered |
| csat\_score | CSAT Score | Select | 1,2,3,4,5 | No | Customer satisfaction rating |
| watch\_list | Watch List | Table | ITSM Watch List (child) | No | Users who receive all updates on this incident |
| tags | Tags | Table MultiSelect | ITSM Tag | No | Labels for filtering and reporting |
| custom\_fields | Custom Fields | Section | — | No | Section for dynamically added org-specific fields |

**6.3 Incident State Machine**

**States**

| State | Field Value | Description | SLA Active? |
| :---- | :---- | :---- | :---- |
| New | New | Ticket created, unassigned, SLA timer starts | Yes |
| Assigned | Assigned | Agent assigned, awaiting first action | Yes |
| In Progress | In Progress | Agent actively working the ticket | Yes |
| Pending | Pending | Waiting on requester/vendor/change — SLA paused | No (Paused) |
| Resolved | Resolved | Resolution provided, awaiting confirmation. CSAT triggered | No (Paused) |
| Closed | Closed | Confirmed resolved or auto-closed after 72h. SLA fulfilment recorded | No |
| Cancelled | Cancelled | Duplicate, test ticket, or withdrawn by requester | No |

**Transitions**

| From | To | Trigger | Actor | Side Effects |
| :---- | :---- | :---- | :---- | :---- |
| New | Assigned | Agent assigned | Agent / Assignment Engine | SLA timer continues; notification to agent |
| Assigned | In Progress | Agent opens ticket | Agent | First response timestamp recorded |
| In Progress | Pending | Agent selects 'Put On Hold' | Agent | On-hold reason required; SLA paused; timer note added |
| Pending | In Progress | Requester replies / agent resumes | System (email reply) / Agent | SLA resumes; hold duration logged |
| In Progress | Resolved | Agent marks resolved | Agent | Resolution notes required; CSAT email/WhatsApp triggered; 72h auto-close timer starts |
| Resolved | Closed | 72h elapses OR requester confirms | System / Requester | SLA fulfillment status finalised; KPIs updated |
| Resolved | In Progress | Requester disputes resolution | Requester / Agent | Reopen count \+1; new SLA instance created; SLA breach count updated |
| Any | Cancelled | Agent/Manager cancels | Agent (Manager required for Resolved) | Cancellation reason required; audit log entry |

## **6.4 Functional Requirements**

| Req ID | Requirement | Priority | Notes / Acceptance Criteria |
| :---- | :---- | :---- | :---- |
| INC-001 | Impact × Urgency priority matrix: 4×4 configurable matrix auto-calculates Priority (P1–P5) on field change | Must Have | Matrix stored in ITSM Priority Matrix DocType; configurable per company |
| INC-002 | Naming series: INC-{YYYY}-{\#\#\#\#\#}, zero-padded, company-scoped, never reused | Must Have | Use Frappe naming series mechanism |
| INC-003 | Multi-channel creation: Portal form, Email-to-incident (IMAP polling), WhatsApp inbound, Chat, Voice CTI pop, REST API | Must Have | Each channel normalised to Incident via Omnichannel engine |
| INC-004 | Mandatory fields enforced by role: agents can skip some fields that are mandatory for end-users | Must Have | Use Frappe Customize Form \+ role-based mandatory |
| INC-005 | Major Incident workflow: flag activates bridge communication, assigns Major Incident Manager, groups child incidents | Must Have | Major Incident flag reveals dedicated section; sends bridge notification |
| INC-006 | Parent-child incident linking: major incident → N child incidents with progress rollup | Must Have | Child incidents show parent reference; major incident view shows children list with status rollup |
| INC-007 | Related incidents: manually link incidents describing the same symptom | Should Have | Many-to-many via ITSM Incident Relation child table |
| INC-008 | Problem promotion: 'Create Problem' button on incident promotes to PRB with pre-filled fields | Must Have | Creates ITSM Problem record pre-filled from incident; bidirectional link |
| INC-009 | Change linkage: link incident to the change record that caused it | Must Have | Link field to ITSM Change; appears on change record as 'Incidents raised' |
| INC-010 | CI linkage: multi-select CIs from CMDB affected by this incident | Must Have | Child table ITSM Incident CI; each row links to ITSM CI |
| INC-011 | Workaround from KEDB: during incident creation, system suggests known workarounds from linked problem KEDB | Must Have | Query ITSM Problem where status=Known Error and matching category |
| INC-012 | Watch list: agents and managers subscribe to incident; receive all activity notifications | Should Have | Watch list child table; notification on every status/comment change |
| INC-013 | On-hold with reason: status=Pending requires on-hold reason; SLA pauses automatically | Must Have | Validate on\_hold\_reason present when status transitions to Pending |
| INC-014 | Reopen protection: re-opened incident increments reopened\_count; metric tracked in SLA compliance report | Must Have | Server-side hook on status change to Resolved→In Progress |
| INC-015 | Bulk operations on list view: bulk assign, bulk priority change, bulk close (with manager role) | Should Have | List view action buttons; validate role before bulk action |
| INC-016 | Timeline / activity feed: chronological view of all events — comments, emails, status changes, SLA events, CSAT | Must Have | Frappe Activity feed \+ custom ITSM Timeline component |
| INC-017 | Internal notes: private work notes visible only to agents (not shown to requester on portal) | Must Have | Comment type \= Internal Note; permission check before display |
| INC-018 | Resolution code required: agent must select resolution code before marking Resolved | Must Have | Validate resolution\_code and resolution\_notes on status=Resolved transition |
| INC-019 | Auto-close: system auto-closes Resolved incidents after configurable period (default 72h) | Must Have | Background job runs every 30 min; evaluates resolved\_at \+ auto\_close\_hours |
| INC-020 | CSAT trigger: post-resolution survey sent via original channel (email/WhatsApp) with 1–5 star rating | Must Have | Trigger on status=Resolved; channel-specific template; CSAT score links back to incident |
| INC-021 | Duplicate detection: new incident checks for open incidents same category \+ requester (alert, not block) | Should Have | Server-side check on save; alert banner in form if potential duplicate found |
| INC-022 | Incident templates: pre-populated incident forms for common issue types (e.g., 'VPN not working', 'Printer offline') | Should Have | ITSM Incident Template DocType; 'Create from template' button on new incident form |
| INC-023 | Knowledge Base suggestion: during ticket creation, system suggests KB articles matching subject | Must Have | Real-time search on subject field change; right-panel suggestions |
| INC-024 | SLA breach notification: notifications at 50%, 75%, 100% of SLA time to assigned agent \+ manager | Must Have | Background SLA evaluator job every 5 min; notification via email \+ in-app |
| INC-025 | Escalation chains: L1 breach → reassign \+ notify manager; L2 breach → notify director \+ upgrade priority | Must Have | ITSM Escalation Rule DocType; triggered by SLA timer events |
| INC-026 | Print / export: incident PDF with full activity timeline for audit | Should Have | Custom print format; includes all comments, status changes, SLA data |
| INC-027 | Incident metrics on list view: colour-coded SLA status badges, time remaining indicator per row | Must Have | Custom list view renderer; green/amber/red based on sla\_status field |

## **6.5 Impact × Urgency Priority Matrix**

| Impact \\ Urgency | 1-Critical | 2-High | 3-Medium | 4-Low |
| :---- | :---- | :---- | :---- | :---- |
| 1-Enterprise Wide | P1 — Critical | P1 — Critical | P2 — High | P3 — Moderate |
| 2-Department Wide | P1 — Critical | P2 — High | P3 — Moderate | P4 — Low |
| 3-Group Wide | P2 — High | P3 — Moderate | P3 — Moderate | P4 — Low |
| 4-Individual | P3 — Moderate | P4 — Low | P4 — Low | P5 — Planning |

## **6.6 SLA Default Targets (configurable per SLA Policy)**

| Priority | First Response | Acknowledgement | Resolution | Auto-Close After Resolution |
| :---- | :---- | :---- | :---- | :---- |
| P1 — Critical | 15 minutes | 30 minutes | 4 hours | 24 hours |
| P2 — High | 30 minutes | 1 hour | 8 hours | 48 hours |
| P3 — Moderate | 2 hours | 4 hours | 24 hours | 72 hours |
| P4 — Low | 4 hours | 8 hours | 72 hours | 7 days |
| P5 — Planning | 1 business day | — | 5 business days | 14 days |

# **7\. Module 2 — Problem Management**

## **7.1 Process Overview**

| *Problem Management identifies the root cause of one or more incidents and prevents future recurrence. A Problem record (PRB) is raised from incidents or proactively by IT staff. The Known Error Database (KEDB) stores confirmed problems with documented workarounds visible to agents during incident resolution.* |
| :---- |

## **7.2 DocType: ITSM Problem**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | Problem ID | Data | Auto: PRB-{YYYY}-{\#\#\#\#\#} | Yes | Auto-naming |
| title | Problem Summary | Data | — | Yes | One-line problem description |
| description | Problem Description | Text Editor | — | Yes | Full description of the problem |
| status | Status | Select | New,Assess,Root Cause Analysis,Fix in Progress,Known Error,Resolved,Closed | Yes | Lifecycle state |
| category | Category | Link | ITSM Category | Yes | Service/system category |
| sub\_category | Sub-Category | Link | ITSM Sub Category | No | Filtered by category |
| priority | Priority | Select | P1-Critical,P2-High,P3-Moderate,P4-Low | Yes | Problem severity |
| problem\_owner | Problem Owner | Link | User | Yes | Accountable owner for RCA |
| assigned\_team | Assigned Team | Link | ITSM Team | No | Team handling investigation |
| root\_cause | Root Cause | Text Editor | — | No | Documented root cause (required for Known Error/Resolved) |
| root\_cause\_category | Root Cause Category | Select | Hardware Failure,Software Bug,Configuration Error,Process Gap,Human Error,External/Vendor,Unknown | No | Classification of root cause type |
| workaround | Workaround | Text Editor | — | No | Temporary fix available to agents and users |
| workaround\_published | Workaround Published | Check | — | No | If checked, workaround shown in KEDB during incident creation |
| permanent\_fix | Permanent Fix | Text Editor | — | No | Permanent solution implemented or planned |
| linked\_change | Linked RFC | Link | ITSM Change | No | Change raised to implement permanent fix |
| linked\_incidents | Linked Incidents | Table | ITSM Problem Incident (child) | No | All incidents caused by this problem |
| problem\_tasks | Problem Tasks | Table | ITSM Problem Task (child) | No | Work tasks for parallel investigation streams |
| rca\_methodology | RCA Methodology | Select | 5-Whys,Fishbone,Fault Tree,Timeline Analysis,Other | No | RCA technique used |
| rca\_five\_whys | 5-Whys Analysis | Text Editor | — | No | Structured 5-Whys text fields |
| rca\_timeline | Incident Timeline | Text Editor | — | No | Chronology of events leading to the problem |
| contributing\_factors | Contributing Factors | Text Editor | — | No | Non-root contributing conditions |
| pir\_required | PIR Required | Check | — | No | Triggers Post-Implementation Review workflow on closure |
| pir\_completed\_at | PIR Completed At | Datetime | — | No | Auto-set when PIR task closed |
| error\_code | Known Error Code | Data | — | No | Short code for KEDB indexing (e.g., KEDB-NET-001) |
| resolution\_notes | Resolution Notes | Text Editor | — | No | How problem was permanently resolved |
| closed\_at | Closed At | Datetime | — | No | Auto-set on closure |

**7.3 Problem State Machine**

**States**

| State | Field Value | Description | SLA Active? |
| :---- | :---- | :---- | :---- |
| New | New | Problem created, unassigned | N/A (no SLA by default) |
| Assess | Assess | Problem being evaluated for scope and priority | No |
| Root Cause Analysis | Root Cause Analysis | Active RCA underway | No |
| Fix in Progress | Fix in Progress | RFC raised, permanent fix being implemented | No |
| Known Error | Known Error | Root cause known, workaround available, fix planned/deferred | No |
| Resolved | Resolved | Permanent fix implemented, incidents confirmed resolved | No |
| Closed | Closed | PIR completed (if required), problem lifecycle ended | No |

**Transitions**

| From | To | Trigger | Actor | Side Effects |
| :---- | :---- | :---- | :---- | :---- |
| New | Assess | Problem owner assigned | Problem Owner | Notification to owner |
| Assess | Root Cause Analysis | RCA started | Problem Owner | RCA methodology selected |
| Root Cause Analysis | Fix in Progress | RFC created | Problem Owner | Linked RFC appears on problem |
| Root Cause Analysis | Known Error | Root cause identified, fix deferred | Problem Owner | Workaround published to KEDB |
| Known Error | Fix in Progress | RFC raised for permanent fix | Change Manager | RFC linked to problem |
| Fix in Progress | Resolved | Permanent fix deployed | Problem Owner | Resolution notes required |
| Resolved | Closed | PIR completed or PIR waived | Problem Owner | Auto-closes linked incidents if still open |

## **7.4 Functional Requirements**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| PRB-001 | Problem creation from incident: 'Create Problem' button on any incident; incident auto-linked; problem pre-filled with incident category, description | Must Have | Creates bidirectional link; incident shows 'Linked Problem' field |
| PRB-002 | Auto problem suggestion: if N incidents (configurable, default 3\) of same category open in X hours (default 2h), system suggests creating a problem | Should Have | Background job; creates ITSM Problem Suggestion record; notifies IT Manager |
| PRB-003 | Linked incidents view: problem form shows all linked incidents with status rollup (open/resolved count) | Must Have | Child table with live lookup; click-through to incident |
| PRB-004 | Known Error Database (KEDB): during incident creation, system searches PRBs with status=Known Error and matching category; shows workaround in right panel | Must Have | Real-time lookup during incident form entry; workaround can be copied to incident |
| PRB-005 | Workaround publishing: agent marks 'Workaround Published'; workaround appears in KEDB searches and KB article auto-draft is generated | Must Have | KB article draft auto-created in ITSM Knowledge Article in Draft status |
| PRB-006 | RCA templates: structured RCA forms for 5-Whys, Fishbone, Fault Tree methodologies — rendered as guided sections in the problem form | Must Have | Tab-based RCA section; methodology selection determines which sub-form to show |
| PRB-007 | Problem tasks: parallel work tasks on same problem assigned to different agents/teams (e.g., network team \+ application team working in parallel) | Must Have | ITSM Problem Task child DocType; each task has own status, assignee, due date |
| PRB-008 | Problem to Change: 'Create RFC' button from problem form; change pre-filled from problem data; bidirectional link | Must Have | Creates ITSM Change; change shows linked\_problem field |
| PRB-009 | PIR workflow: if pir\_required=1, closure triggers PIR task assigned to problem owner; problem cannot close until PIR task completed | Should Have | PIR task auto-created on status→Resolved when pir\_required=1 |
| PRB-010 | Problem SLA (optional): configurable SLA per problem priority for time-to-root-cause (not mandatory v1) | Nice to Have | Separate SLA policy type for problems; disabled by default |
| PRB-011 | Problem metrics: MTTR, recurrence rate (same root cause), incident count per problem, time in each state | Must Have | Calculated fields \+ report; visible on Problem Management dashboard |
| PRB-012 | Audit trail: full history of every field change, status transition, and comment with user \+ timestamp | Must Have | Frappe Document History \+ custom ITSM Audit Log entry on every transition |

# **8\. Module 3 — Change Management**

## **8.1 Process Overview**

| *Change Management controls the lifecycle of all changes to IT infrastructure, services, and applications — minimising risk while enabling business-aligned delivery speed. The app implements ITIL v4 Change Enablement with three change types (Standard, Normal, Emergency), a full CAB workflow, automated risk scoring, a visual change calendar, blackout windows, and mandatory Post-Implementation Review (PIR) for failed changes.* |
| :---- |

## **8.2 Change Types**

| Change Type | Description | Risk Level | Approval Path | SLA |
| :---- | :---- | :---- | :---- | :---- |
| Standard | Pre-approved, routine, low-risk. Procedure documented. Examples: password reset, RAM upgrade, patch apply | Low | Auto-approved — no CAB; single technical approver optional | 24h total |
| Normal | Requires full assessment and CAB approval. Examples: server migration, firewall rule change, application upgrade | Medium–High | Multi-stage: Technical Review → CAB Approval → Implementation Authorisation | Per schedule |
| Emergency | Urgent change to restore service or prevent imminent failure. Examples: emergency hotfix, security patch | Variable | ECAB (Emergency CAB) — expedited; 2 approver minimum; retrospective CAB review required | 4h approval |

## **8.3 DocType: ITSM Change**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | RFC ID | Data | Auto: RFC-{YYYY}-{\#\#\#\#\#} | Yes | Auto-naming |
| title | Change Title | Data | — | Yes | Brief description of the change |
| change\_type | Change Type | Select | Standard,Normal,Emergency | Yes | Determines approval path and calendar visibility |
| description | Change Description | Text Editor | — | Yes | What is being changed and why |
| justification | Business Justification | Text Editor | — | Yes | Business reason for the change |
| status | Status | Select | New,Draft,Pending Review,CAB Scheduled,CAB Approved,Authorised,Scheduled,In Progress,Completed,Failed,Cancelled,PIR Pending,Closed | Yes | Lifecycle state |
| priority | Priority | Select | Low,Medium,High,Critical | Yes | Change urgency |
| risk\_level | Risk Level | Select | Very Low,Low,Medium,High,Very High | Yes | Auto-calculated from risk matrix; can be overridden with justification |
| risk\_score | Risk Score | Int | — | No | Numeric score 0–100 from risk assessment questionnaire |
| impact | Impact | Select | 1-Enterprise Wide,2-Department Wide,3-Group Wide,4-Individual | Yes | Scope of impact if change fails |
| category | Category | Link | ITSM Category | Yes | Service/system category |
| sub\_category | Sub-Category | Link | ITSM Sub Category | No | — |
| change\_initiator | Change Initiator | Link | User | Yes | Person raising the RFC |
| change\_owner | Change Owner | Link | User | Yes | Accountable for successful delivery |
| assigned\_team | Assigned Team | Link | ITSM Team | Yes | Team implementing the change |
| technical\_reviewer | Technical Reviewer | Link | User | No | Required for Normal/Emergency; performs technical review |
| cab\_required | CAB Review Required | Check | — | No | Auto-set based on change\_type and risk\_level |
| cab\_meeting | CAB Meeting | Link | ITSM CAB Meeting | No | CAB meeting where this change is scheduled for discussion |
| implementation\_plan | Implementation Plan | Text Editor | — | Yes | Step-by-step implementation procedure |
| rollback\_plan | Rollback Plan | Text Editor | — | Yes | Required for Normal/Emergency — how to undo if failed |
| test\_plan | Test Plan | Text Editor | — | No | Post-implementation testing steps |
| start\_datetime | Planned Start | Datetime | — | Yes | Planned implementation start |
| end\_datetime | Planned End | Datetime | — | Yes | Planned implementation end; must not overlap blackout windows |
| actual\_start | Actual Start | Datetime | — | No | Recorded when status=In Progress |
| actual\_end | Actual End | Datetime | — | No | Recorded when status=Completed or Failed |
| linked\_incidents | Linked Incidents | Table | ITSM Change Incident (child) | No | Incidents fixed by this change |
| linked\_problem | Linked Problem | Link | ITSM Problem | No | Problem that triggered this change |
| linked\_cis | Affected CIs | Table | ITSM Change CI (child) | No | CIs impacted by this change |
| affected\_services | Affected Services | Table | ITSM Change Service (child) | No | Business/IT services impacted |
| downtime\_expected | Downtime Expected | Check | — | No | If yes, downtime\_start and downtime\_end required |
| downtime\_start | Downtime Start | Datetime | — | No | — |
| downtime\_end | Downtime End | Datetime | — | No | — |
| change\_tasks | Change Tasks | Table | ITSM Change Task (child) | No | Pre/Implementation/Post tasks |
| approvals | Approvals | Table | ITSM Change Approval (child) | No | All approval records with decision+comment+timestamp |
| close\_code | Close Code | Select | Successful,Successful with Issues,Unsuccessful — Rolled Back,Unsuccessful — Partial,Cancelled | No | Required on completion/failure |
| close\_notes | Close Notes | Text Editor | — | No | Summary of implementation outcome |
| pir\_required | PIR Required | Check | — | No | Auto-set if close\_code=Unsuccessful or risk\_level=High/Very High |
| pir\_notes | PIR Notes | Text Editor | — | No | Post-implementation review findings |
| risk\_assessment | Risk Assessment | Table | ITSM Change Risk Question (child) | No | Responses to risk questionnaire |
| blackout\_conflict | Blackout Conflict | Check | — | No | System flag: planned dates overlap a blackout window |
| conflict\_details | Conflict Details | Small Text | — | No | Details of detected conflicts |

**8.4 Change State Machine**

**States**

| State | Field Value | Description | SLA Active? |
| :---- | :---- | :---- | :---- |
| New | New | RFC created, incomplete — not yet submitted for review | N/A |
| Draft | Draft | RFC being drafted by change initiator | N/A |
| Pending Review | Pending Review | Submitted for technical review | N/A |
| CAB Scheduled | CAB Scheduled | Change added to CAB meeting agenda | N/A |
| CAB Approved | CAB Approved | CAB voted to approve | N/A |
| Authorised | Authorised | Final authorisation by Change Manager | N/A |
| Scheduled | Scheduled | Implementation window confirmed on change calendar | N/A |
| In Progress | In Progress | Implementation underway | N/A |
| Completed | Completed | Implementation complete — success or partial | N/A |
| Failed | Failed | Implementation failed and rolled back | N/A |
| PIR Pending | PIR Pending | Awaiting Post-Implementation Review completion | N/A |
| Cancelled | Cancelled | RFC withdrawn before implementation | N/A |
| Closed | Closed | PIR done, all tasks closed, audit complete | N/A |

**Transitions**

| From | To | Trigger | Actor | Side Effects |
| :---- | :---- | :---- | :---- | :---- |
| Draft | Pending Review | Submit for review | Change Initiator | Technical reviewer notified; risk score calculated |
| Pending Review | CAB Scheduled | Technical review approved | Technical Reviewer | Change added to next CAB meeting agenda |
| Pending Review | Draft | Technical review rejected | Technical Reviewer | Rejection reason recorded; initiator notified |
| CAB Scheduled | CAB Approved | CAB votes approve (quorum met) | CAB Members | CAB approval recorded with all voter details |
| CAB Scheduled | Draft | CAB rejects | CAB Chair | Rejection reason recorded; initiator must revise |
| CAB Approved | Authorised | Change Manager authorises | Change Manager | Final sign-off; implementation window locked |
| Authorised | Scheduled | Dates confirmed on change calendar | Change Owner | Blackout window check runs; conflict alerts if overlap |
| Scheduled | In Progress | Implementation starts | Change Owner | Actual start recorded; notifications sent |
| In Progress | Completed | Implementation done successfully | Change Owner | Close code required; PIR triggered if applicable |
| In Progress | Failed | Implementation failed | Change Owner | Rollback initiated; close code=Unsuccessful; PIR mandatory |
| Completed | PIR Pending | PIR required (failed/high risk) | System | PIR task auto-created |
| Failed | PIR Pending | PIR always required for failures | System | Mandatory PIR; post-mortem scheduled |
| PIR Pending | Closed | PIR completed | Problem Owner / Change Owner | All tasks closed; metrics finalised |

## **8.5 DocType: ITSM CAB Meeting**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | Meeting ID | Data | Auto: CAB-{YYYY}-{\#\#\#} | Yes | Auto-naming |
| meeting\_type | Meeting Type | Select | Regular CAB,Emergency CAB (ECAB),Post-Implementation Review | Yes | Determines quorum rules |
| scheduled\_datetime | Scheduled Date & Time | Datetime | — | Yes | Meeting time |
| duration\_minutes | Duration (mins) | Int | — | Yes | Expected meeting duration |
| location | Location | Data | — | No | Physical location or video call link |
| cab\_chair | CAB Chair | Link | User | Yes | Change Manager or delegate |
| cab\_members | CAB Members | Table | ITSM CAB Member (child) | Yes | Members: role, attendance status, vote |
| agenda\_changes | Agenda Changes | Table | ITSM CAB Agenda Item (child) | No | Changes presented; order, presenter, decision |
| quorum\_required | Quorum Required (%) | Int | Default: 51 | Yes | Minimum % of members needed for valid approval vote |
| meeting\_notes | Meeting Notes | Text Editor | — | No | Minutes, decisions, action items |
| status | Meeting Status | Select | Scheduled,In Progress,Completed,Cancelled | Yes | — |

## **8.6 Risk Assessment Matrix**

| Risk Factor | Weight | Score 1 (Low) | Score 2 (Medium) | Score 3 (High) | Score 4 (Very High) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Number of CIs affected | 25% | 1 CI | 2–5 CIs | 6–20 CIs | \> 20 CIs |
| Business criticality of CIs | 25% | Dev/Test only | Non-critical production | Business-critical | Mission-critical / Customer-facing |
| Previous change failure rate | 20% | 0% history | \< 5% | 5–15% | \> 15% |
| Rollback tested? | 15% | Fully tested | Tested in staging | Partially tested | Not tested |
| Implementation window | 15% | Off-hours, low traffic | Business hours, low usage | Peak hours | Critical business period |
| *Risk Score \= Σ(Factor Score × Weight) × 25\. Score 0–25 \= Very Low; 26–50 \= Low; 51–65 \= Medium; 66–80 \= High; 81–100 \= Very High. Scores are auto-calculated from the risk assessment questionnaire in the change form.* |  |  |  |  |  |

## **8.7 Functional Requirements**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| CHG-001 | Automated risk score calculation: risk questionnaire (5 factors × 4 levels) auto-calculates numeric risk score and risk level on save | Must Have | ITSM Change Risk Question child table; score computed server-side on change |
| CHG-002 | Blackout window enforcement: system warns (not blocks) if planned dates overlap a blackout window; manager override with reason required | Must Have | ITSM Blackout Window DocType; server-side check on date fields; alert banner |
| CHG-003 | Conflict detection: if two changes affect the same CI in overlapping windows, conflict alert raised; both change owners notified | Should Have | Background job on schedule/authorise; creates ITSM Change Conflict record |
| CHG-004 | Change Calendar: Visual month/week/day calendar showing all authorised changes; filterable by team, type, status; colour-coded by risk | Must Have | Vue 3 calendar component with FullCalendar.js; data from ITSM Change API |
| CHG-005 | CAB meeting management: create CAB meetings, add agenda items, record attendance, capture votes per member, compute quorum | Must Have | ITSM CAB Meeting DocType; CAB member attendance \+ vote child table |
| CHG-006 | Email-based CAB voting: CAB members receive email with Approve/Reject links (token-based, no login required) | Must Have | Signed URL tokens; vote recorded server-side; duplicate vote prevention |
| CHG-007 | Approval delegation: any approver can delegate to alternate user with expiry date; delegations logged | Must Have | ITSM Approval Delegation DocType; system checks active delegations before notification |
| CHG-008 | Standard change library: pre-approved standard change templates; change created from template auto-approves | Must Have | ITSM Change Template DocType; change\_type=Standard templates bypass CAB |
| CHG-009 | Emergency change ECAB: Emergency changes follow expedited ECAB path (minimum 2 approvers); mandatory retrospective CAB review scheduled | Must Have | change\_type=Emergency triggers ECAB workflow; retrospective CAB scheduled on closure |
| CHG-010 | Change tasks (pre/impl/post): structured task list with pre-implementation, implementation, and post-implementation phases; tasks assigned to different users/teams | Must Have | ITSM Change Task child DocType with phase, assignee, status, due\_date |
| CHG-011 | Rollback plan: mandatory for Normal/Emergency changes; validated on status transition to Authorised | Must Have | Server-side validation: rollback\_plan required for change\_type in Normal, Emergency |
| CHG-012 | Rollback execution: if implementation fails, 'Execute Rollback' button triggers rollback task assignments and status=Failed workflow | Must Have | Button visible when status=In Progress; creates rollback tasks from rollback\_plan text |
| CHG-013 | PIR (Post-Implementation Review): mandatory PIR for failed changes and high-risk changes; PIR creates a Problem task for lessons-learned documentation | Must Have | ITSM PIR DocType linked to change; PIR task auto-assigned to change owner |
| CHG-014 | Change freeze periods: global date ranges where only Emergency changes allowed; Calendar highlights freeze periods; Standard/Normal changes blocked | Must Have | ITSM Change Freeze DocType; server-side validation on Authorised transition |
| CHG-015 | CI impact analysis: change form shows all services and CIs that will be affected, sourced from CMDB relationship graph | Should Have | Query ITSM CI Relationship to find upstream/downstream CIs from linked CIs |
| CHG-016 | Downtime notification: if downtime\_expected=1, system sends maintenance notification to affected users/customer groups | Must Have | Notification template for planned downtime; send 72h, 24h, and 1h before maintenance |
| CHG-017 | Change metrics dashboard: changes by type, risk, close code; failed change rate trend; CAB approval cycle time; unauthorized change count | Must Have | Pre-built Change Management dashboard with 8 KPI widgets |
| CHG-018 | Unauthorized change detection: incidents resolved with resolution\_code='Unauthorized Change' flagged in change compliance report | Should Have | Report showing incidents with this code; escalated to Change Manager weekly |
| CHG-019 | Change schedule view per CI: from CMDB CI record, see all past and upcoming changes affecting that CI | Should Have | Linked change list on CI record, filtered by status not Cancelled |
| CHG-020 | Full audit trail: every approval decision, vote, status change, date modification recorded with user \+ timestamp \+ before/after values | Must Have | ITSM Audit Log entry on every significant change field transition |

# **9\. Module 4 — CMDB (Configuration Management Database)**

## **9.1 Overview**

| *The CMDB is the authoritative repository of all Configuration Items (CIs) in the IT environment — their attributes, states, and relationships. It is the connective tissue linking incidents, problems, changes, and assets to the business services they support. The CI class hierarchy is configurable; organisations define their own CI types.* |
| :---- |

## **9.2 CI Class Hierarchy**

| Class | Typical Sub-Classes | Key Attributes | Linked To |
| :---- | :---- | :---- | :---- |
| Hardware | Server, Workstation, Laptop, Mobile Device, Printer, Network Device, Storage Array, UPS | Serial \#, Model, Manufacturer, IP, OS, Location, Owner, Warranty End, Rack/Room | Assets, Incidents, Changes |
| Software | Application, Operating System, Database, Middleware, SaaS Application, Open Source Library | Version, Vendor, License Type, License Count, EoL Date, Install Location | Incidents, Problems, Changes |
| Service | Business Service, IT Service, Application Service, API | Service Owner, Business Criticality, SLA Policy, Dependent CIs, DR Category | Incidents (affected service), SLAs |
| Network | Router, Switch, Firewall, Load Balancer, WAP, WAN Link, VLAN | IP Range, VLAN ID, Interface Count, Bandwidth, Location | Incidents, Changes |
| Cloud | Cloud Account, VM Instance, Container, Kubernetes Cluster, S3 Bucket, Cloud Region | Provider (AWS/Azure/GCP), Region, Instance Type, vCPU, RAM, Monthly Cost | Incidents, Changes, Assets |
| Facility | Datacenter, Server Room, Rack, Power Distribution Unit, HVAC | Physical Location, Power Capacity kW, Cooling Capacity, Rack Units | Hardware CIs |
| Database | Database Instance, Database Schema, Stored Procedure | Version, Vendor, Host CI, Size GB, Backup Schedule | Applications, Services |
| Certificate | SSL Certificate, Code Signing Certificate, CA Certificate | Domain, Issuer, Expiry Date, Algorithm, SHA Thumbprint | Services, Applications |

## **9.3 DocType: ITSM CI (Configuration Item)**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | CI ID | Data | Auto: CI-{CLASS\_CODE}-{\#\#\#\#\#} | Yes | Auto-naming per CI class |
| ci\_name | CI Name | Data | — | Yes | Human-readable name (e.g., 'PROD-WEB-01', 'CRM Application') |
| ci\_class | CI Class | Link | ITSM CI Class | Yes | Top-level class (Hardware, Software, Service, etc.) |
| ci\_type | CI Type | Link | ITSM CI Type | Yes | Sub-type within class; filtered by ci\_class |
| status | Status | Select | On Order,In Stock,In Use,In Maintenance,Retired,Stolen,Disposed | Yes | Lifecycle state |
| business\_criticality | Business Criticality | Select | Critical,High,Medium,Low | Yes | Impact if CI fails |
| environment | Environment | Select | Production,Staging,UAT,Development,DR | Yes | Deployment environment |
| location | Location | Link | ITSM Location | No | Physical or logical location |
| ci\_owner | Owner | Link | User | Yes | Person responsible for this CI |
| managed\_by\_team | Managed By Team | Link | ITSM Team | No | Team managing this CI |
| company | Company | Link | Company | Yes | Organisation context |
| department | Department | Link | Department | No | Business department |
| linked\_asset | Linked Asset | Link | ITSM Asset | No | Physical asset record (for hardware CIs) |
| ip\_address | IP Address | Data | — | No | Primary IP address |
| mac\_address | MAC Address | Data | — | No | Network interface MAC |
| serial\_number | Serial Number | Data | — | No | Hardware serial (for hardware CIs) |
| os\_name | OS Name | Data | — | No | Operating system |
| os\_version | OS Version | Data | — | No | OS version string |
| manufacturer | Manufacturer | Data | — | No | Hardware manufacturer |
| model | Model | Data | — | No | Hardware model |
| version | Version | Data | — | No | Software version |
| vendor | Vendor | Link | Supplier | No | Software/service vendor; links to ERPNext Supplier |
| purchase\_date | Purchase Date | Date | — | No | When CI was acquired |
| warranty\_end | Warranty End Date | Date | — | No | Alert generated 90 days before expiry |
| end\_of\_life | End of Life Date | Date | — | No | Vendor EoL; alert generated 180 days before |
| attributes | Custom Attributes | Table | ITSM CI Attribute (child) | No | Class-specific dynamic attributes (key-value) |
| tags | Tags | Table MultiSelect | ITSM Tag | No | Labels for filtering |
| discovery\_source | Discovery Source | Select | Manual,CSV Import,API Import,Agent Discovery,Cloud API | No | How this CI was added |
| last\_discovered | Last Discovered | Datetime | — | No | Timestamp of last successful discovery |
| notes | Notes | Text Editor | — | No | Free-text notes |

## **9.4 DocType: ITSM CI Relationship**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| source\_ci | Source CI | Link | ITSM CI | Yes | The CI the relationship originates from |
| relationship\_type | Relationship Type | Link | ITSM CI Relationship Type | Yes | e.g., 'Runs on', 'Hosted on', 'Depends on', 'Connected to' |
| target\_ci | Target CI | Link | ITSM CI | Yes | The CI the relationship points to |
| is\_bidirectional | Bidirectional | Check | — | No | If checked, relationship shown on both CIs |
| relationship\_strength | Strength | Select | Hard Dependency,Soft Dependency,Related,Associated | No | How tightly coupled the relationship is |
| notes | Notes | Small Text | — | No | Context for this specific relationship |

## **9.5 Functional Requirements**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| CMDB-001 | CI class and type hierarchy: configurable ITSM CI Class \+ ITSM CI Type DocTypes; attributes vary by type; dynamic sections on CI form | Must Have | ITSM CI Type links to ITSM CI Class; type-specific attribute template applied on type selection |
| CMDB-002 | Relationship management: create, edit, delete CI relationships with type; bidirectional relationships shown on both CIs | Must Have | ITSM CI Relationship DocType; visualised in relationship map |
| CMDB-003 | Visual relationship map: interactive D3.js force-directed graph; click node to open CI; expand/collapse relationship levels; filter by relationship type | Must Have | Vue component with D3.js (loaded from CDN); data from API endpoint /api/method/frappe\_itsm.cmdb.get\_relationship\_graph |
| CMDB-004 | Impact analysis: 'What will be affected if this CI fails?' — upstream service chain traced; result shows affected services and business impact | Must Have | Server-side BFS/DFS graph traversal from selected CI; results in impact panel on CI form |
| CMDB-005 | CI linking on ITSM records: multi-select CI lookup on Incident, Problem, Change, and Asset forms; linked CIs shown on CI record (reverse lookup) | Must Have | ITSM Incident CI, ITSM Change CI child tables; CI record shows linked records in tabs |
| CMDB-006 | Bulk import: CSV/Excel upload with column mapping wizard; validates required fields; creates or updates CIs in bulk | Must Have | Custom import page at /itsm/cmdb/import; field mapping saved as template; error report downloadable |
| CMDB-007 | CMDB health dashboard: data completeness % per CI class (missing mandatory attributes), stale CIs (not updated in 90+ days), orphaned CIs (no relationships), expiring warranties | Should Have | Pre-built CMDB Health dashboard; background job calculates scores nightly |
| CMDB-008 | CI audit trail: complete history of every field change — who changed what, from what value, to what value, when | Must Have | Frappe Document History \+ ITSM Audit Log entry on every save |
| CMDB-009 | CI lifecycle state management: state transitions logged; status changes generate notification to CI owner | Must Have | Workflow on status field; notification on transition |
| CMDB-010 | Warranty and EoL alerts: background job sends alert to CI owner 90 days before warranty\_end; 180 days before end\_of\_life | Must Have | Scheduled job; notification template; creates ITSM CI Alert record |
| CMDB-011 | Cloud CI import: API connectors to import CIs from AWS (EC2, RDS, S3), Azure (VMs, databases), and GCP | Should Have | Phase 2 enhancement; basic structure defined in v1 with manual import |
| CMDB-012 | Change schedule on CI: CI record shows tab listing all upcoming and past changes affecting it, with dates and status | Must Have | Linked changes query from ITSM Change CI child table |
| CMDB-013 | CI search: full-text search across CI name, serial number, IP address, and notes; filter by class, type, status, environment | Must Have | Custom search endpoint; list view with filters |
| CMDB-014 | Service dependency map: for a given Business Service CI, show all dependent CIs in a hierarchical tree view | Should Have | Specialised view of relationship graph filtered to service hierarchy |

# **10\. Module 5 — Service Catalog & Request Management**

## **10.1 Overview**

| *The Service Catalog is the single source of truth for all services offered by IT, HR, Facilities, and other departments. Employees and customers browse a branded, searchable self-service portal, select catalog items, fill guided forms, and track requests through approval and fulfillment — all without calling or emailing anyone.* |
| :---- |

## **10.2 Entity Model**

| Entity | DocType Name | Description |
| :---- | :---- | :---- |
| Catalog | ITSM Catalog | Top-level grouping (IT Services, HR Services, Facilities). Multiple catalogs per portal. |
| Category | ITSM Catalog Category | Sub-grouping within catalog. Hierarchical (category → sub-category). |
| Catalog Item | ITSM Catalog Item | Individual requestable service with form, approval rules, SLA, and fulfillment config. |
| Catalog Variable | ITSM Catalog Variable | Form field on a catalog item. Typed, ordered, conditional. |
| Variable Set | ITSM Variable Set | Reusable group of variables (e.g., Shipping Address, Employee Info) importable across items. |
| Service Request | ITSM Service Request | Submitted request parent record. One request may contain multiple items. |
| Request Item (RITM) | ITSM Request Item | Line item for each catalog item in a request. Has own approval chain and fulfillment tasks. |
| Approval | ITSM Catalog Approval | Approval record per approver per RITM. Records decision, comment, timestamp. |
| Request Task | ITSM Request Task | Fulfillment task assigned to fulfillment group/user per RITM. |
| Catalog Approval Rule | ITSM Catalog Approval Rule | Defines the approval chain for a catalog item. Supports sequential, parallel, and conditional logic. |

## **10.3 DocType: ITSM Catalog Item**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | Item Code | Data | Auto: CATITEM-{\#\#\#\#\#} | Yes | — |
| item\_name | Item Name | Data | — | Yes | Display name shown in catalog portal |
| catalog | Catalog | Link | ITSM Catalog | Yes | Parent catalog |
| category | Category | Link | ITSM Catalog Category | Yes | — |
| sub\_category | Sub-Category | Link | ITSM Catalog Category | No | — |
| short\_description | Short Description | Small Text | — | Yes | One-liner shown on catalog card |
| description | Full Description | Text Editor | — | No | Rich description with screenshots, videos |
| icon | Icon | Attach Image | — | No | Catalog item icon/thumbnail |
| status | Status | Select | Draft,Active,Retired | Yes | Only Active items visible in portal |
| fulfillment\_team | Fulfillment Team | Link | ITSM Team | Yes | Team that executes the request |
| fulfillment\_user | Default Assignee | Link | User | No | Specific user (optional override of team) |
| sla\_hours | SLA (Business Hours) | Int | — | No | Fulfillment target in business hours; 0 \= no SLA |
| requires\_approval | Requires Approval | Check | — | Yes | If unchecked, auto-approved immediately |
| approval\_type | Approval Type | Select | Sequential,Parallel,Manager Approval | No | How approvers are sequenced |
| approval\_rules | Approval Rules | Table | ITSM Catalog Approval Rule (child) | No | Ordered list of approvers/roles |
| variables | Form Variables | Table | ITSM Catalog Variable (child) | No | Form fields for this catalog item |
| variable\_sets | Variable Sets | Table | ITSM Catalog Variable Set (child) | No | Imported reusable variable groups |
| tags | Tags | Table MultiSelect | ITSM Tag | No | For search and filtering |
| price | Cost (Display Only) | Currency | — | No | Informational — cost shown to requester |
| is\_popular | Popular Item | Check | — | No | Displayed in 'Popular' section of portal |
| allow\_guest | Allow Guest Request | Check | — | No | If portal set to public, non-authenticated users can request |

## **10.4 Catalog Variable Types**

| Variable Type | Field Type | Config Options | Use Case |
| :---- | :---- | :---- | :---- |
| Single Line Text | Data | Max length, regex validation, placeholder | Name, system name, error message |
| Multi-line Text | Text | Max chars, placeholder | Description, justification, special instructions |
| Yes / No | Check | Default value | Do you need admin rights? / Is this urgent? |
| Integer | Int | Min, Max, default | Quantity, number of users, port number |
| Decimal | Float | Min, Max, precision | Cost estimate, percentage |
| Date | Date | Min date, Max date | Start date, preferred delivery date |
| Date & Time | Datetime | — | Preferred appointment, scheduled time |
| Select (Dropdown) | Select | Options list (pipe-separated) | Software version, location, access level |
| Multi-Select | Table MultiSelect | DocType or static options | Multiple permissions, multiple groups |
| User Lookup | Link to User | Filter expression | Manager, alternate contact, team member |
| CI Lookup | Link to ITSM CI | Filter by class/type/status | Affected system, asset to be repaired |
| File Upload | Attach | Allowed extensions, max size MB | Justification document, approval screenshot |
| Container (Group) | Section Break | Label, collapse default | Group related fields visually |

## **10.5 Functional Requirements**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| CAT-001 | Drag-and-drop catalog item builder: add variables, reorder by drag, set required/optional, add help text — no code | Must Have | Vue drag-and-drop form builder; config stored as JSON in ITSM Catalog Variable |
| CAT-002 | Variable visibility conditions: show/hide a variable based on value of another variable (UI policy equivalent) | Must Have | Condition engine: {field} {operator} {value} → show/hide target field; evaluated client-side |
| CAT-003 | Multi-stage approval workflow: sequential (A → B → C), parallel (A+B+C simultaneously), or manager-of-requester | Must Have | ITSM Catalog Approval Rule child table; parallel approvals tracked via ITSM Catalog Approval records |
| CAT-004 | Email-based approval: approvers receive email with Approve / Reject links (no login needed, signed token) | Must Have | Token-based approval endpoint /api/method/frappe\_itsm.catalog.approve\_token?token=X\&decision=approve |
| CAT-005 | Approval timeout: if approver does not act within N hours, escalate to next approver or auto-approve (configurable per rule) | Must Have | Background job checks pending approvals; escalation action from catalog approval rule config |
| CAT-006 | Approval delegation: approver sets delegate (user \+ date range) via self-service My Profile screen | Should Have | ITSM Approval Delegation DocType; system checks before sending approval notification |
| CAT-007 | RITM (Request Item) per catalog item: each item in a request generates independent RITM with own status, approval chain, and fulfillment tasks | Must Have | ITSM Request Item DocType; one ITSM Service Request → many ITSM Request Items |
| CAT-008 | Shopping cart: requester adds multiple catalog items in one session; submits as single Service Request; each item tracked independently | Should Have | Cart stored in session/localStorage; submitted as one ITSM Service Request with multiple RITMs |
| CAT-009 | Fulfillment tasks: each RITM auto-generates fulfillment tasks assigned to fulfillment team; task completion drives RITM progress | Must Have | ITSM Request Task child table on RITM; RITM status updates based on task completion % |
| CAT-010 | Requester status tracking: self-service portal shows real-time progress through approval and fulfillment stages with visual timeline | Must Have | Status timeline component on portal; polls ITSM Request Item API |
| CAT-011 | SLA per item: if sla\_hours defined, RITM gets SLA timer; breach notification to fulfillment team lead | Must Have | SLA engine creates ITSM SLA Instance for each RITM with SLA defined |
| CAT-012 | Catalog item versioning: Draft / Active / Retired states; retiring an item closes pending requests; new requests blocked | Must Have | Status check on catalog browse API; admin can retire with redirect to replacement item |
| CAT-013 | Catalog access control: items visible only to specific roles, departments, or user groups | Should Have | ITSM Catalog Item Visibility child table (role/department filter) |
| CAT-014 | Popular and featured items: admin can mark items as popular or featured; displayed in dedicated sections on portal home | Should Have | is\_popular flag; featured items configurable in ITSM Catalog (portal config) |
| CAT-015 | Catalog admin roles: non-IT users (HR, Facilities) can manage their own catalog section via Admin Portal without touching IT catalog | Must Have | Role-based catalog ownership; ITSM Admin delegates catalog section to non-IT team lead |

# **11\. Module 6 — Knowledge Base**

## **11.1 Overview**

| *The Knowledge Base (KB) enables self-service resolution and supports agent efficiency. Articles are authored by agents, reviewed, and published to appropriate audiences (public, internal agents, or specific teams). Deflection rate — the percentage of portal sessions resolved via KB without creating a ticket — is a primary KPI.* |
| :---- |

## **11.2 DocType: ITSM Knowledge Article**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | Article ID | Data | Auto: KB-{YYYY}-{\#\#\#\#\#} | Yes | Auto-naming |
| title | Title | Data | — | Yes | Article title — optimised for search |
| content | Content | Text Editor | — | Yes | Rich-text article body; supports images, code blocks, tables, videos |
| category | Category | Link | ITSM KB Category | Yes | Top-level KB category |
| sub\_category | Sub-Category | Link | ITSM KB Category | No | — |
| status | Status | Select | Draft,Under Review,Published,Retired | Yes | Publication lifecycle |
| visibility | Visibility | Select | Public (All Users),Internal (Agents Only),Team Only | Yes | Who can read this article |
| visible\_to\_team | Visible to Team | Link | ITSM Team | No | Required when visibility=Team Only |
| author | Author | Link | User | Yes | Original author |
| reviewer | Reviewer | Link | User | No | Agent who approved publication |
| reviewed\_at | Reviewed At | Datetime | — | No | When reviewer approved |
| published\_at | Published At | Datetime | — | No | When status changed to Published |
| version | Version | Int | Default:1 | No | Increments on every publish |
| valid\_until | Valid Until | Date | — | No | Article expiry date; auto-retires on this date |
| linked\_incidents | Linked Incidents | Table | ITSM KB Incident (child) | No | Incidents resolved using this article |
| linked\_problem | Linked Problem | Link | ITSM Problem | No | Problem whose workaround is in this article |
| view\_count | View Count | Int | — | No | Total portal/agent views |
| helpful\_count | Helpful Votes | Int | — | No | Users who rated helpful |
| not\_helpful\_count | Not Helpful Votes | Int | — | No | Users who rated not helpful |
| tags | Tags | Table MultiSelect | ITSM Tag | No | Search tags |
| attachments | Attachments | Attach | — | No | Supporting files, screenshots, PDFs |
| related\_articles | Related Articles | Table | ITSM KB Related (child) | No | Manually curated related articles |

**11.3 KB Article State Machine**

**States**

| State | Field Value | Description | SLA Active? |
| :---- | :---- | :---- | :---- |
| Draft | Draft | Article being authored | N/A |
| Under Review | Under Review | Submitted for peer review | N/A |
| Published | Published | Live — visible per visibility setting | N/A |
| Retired | Retired | No longer accurate; hidden from search | N/A |

**Transitions**

| From | To | Trigger | Actor | Side Effects |
| :---- | :---- | :---- | :---- | :---- |
| Draft | Under Review | Author submits for review | Author | Reviewer assigned; notification sent to reviewer |
| Under Review | Published | Reviewer approves | Reviewer | Published timestamp set; versioned; search index updated |
| Under Review | Draft | Reviewer rejects with comments | Reviewer | Review comments added; author notified |
| Published | Retired | Admin/author retires | Admin / Author | Retirement reason required; hidden from search; related articles updated |
| Retired | Draft | Author revives article | Author | New draft version created; previous version preserved |

## **11.4 Functional Requirements**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| KB-001 | Article editor: rich-text WYSIWYG editor (TipTap or Quill); supports H1–H4, bold/italic, ordered/unordered lists, code blocks, inline images, tables, callout boxes, video embed | Must Have | TipTap editor in Vue component; content stored as HTML |
| KB-002 | Keyword search: full-text search across title, content, and tags; highlighted matches in results; filtered by category and visibility | Must Have | MariaDB FULLTEXT index on title \+ content; custom search endpoint |
| KB-003 | KB suggestion during incident/request creation: as user types subject, matching KB articles appear in right panel with link to open; view tracked | Must Have | Real-time API call on subject keyup (debounced 400ms); articles shown in side panel |
| KB-004 | Deflection tracking: if user views KB article and does NOT create a ticket, session counted as deflected; deflection rate \= deflected sessions / total portal sessions | Must Have | Session event tracking: article\_opened, ticket\_created; deflection rate calculated in reporting |
| KB-005 | Feedback: at article end, users rate 'Was this helpful? Yes/No'; if No, optional free-text comment; feedback visible to author | Must Have | ITSM KB Feedback DocType; feedback count shown on article; low-rating articles flagged |
| KB-006 | Version history: every published version saved; author can view diff between versions; rollback to previous version | Should Have | ITSM KB Version DocType; version\_number increments on publish; diff computed server-side |
| KB-007 | Article expiry: valid\_until date; background job auto-retires expired articles and notifies author for review | Must Have | Scheduler job runs daily; retires articles past valid\_until; notification to author \+ KB admin |
| KB-008 | Workaround auto-draft: when a Problem workaround is published, system auto-creates a KB article draft pre-filled with problem title and workaround content | Must Have | Server-side hook on ITSM Problem workaround\_published field change |
| KB-009 | KB categories management: hierarchical categories (2 levels); icons, descriptions, parent/child relationships; drag-and-drop reorder in Admin Portal | Must Have | ITSM KB Category DocType; category tree UI in admin portal |
| KB-010 | Internal vs public visibility: agents see internal-only articles; customers and employees see only Public articles; team-restricted articles visible only to that team | Must Have | Permission check in KB search API; article list API filters by requesting user's role and team membership |
| KB-011 | Article analytics: per-article stats — view count, helpful %, search hit count, top 10 articles by helpfulness | Should Have | ITSM KB Analytics report; data from view\_count and feedback records |
| KB-012 | KB metrics on dashboard: deflection rate trend, articles published this month, articles expiring in 30 days, low-rating articles needing review | Must Have | KB section on ITSM Operations Dashboard |

# **12\. Module 7 — Omnichannel Communication**

## **12.1 Overview**

| *The Omnichannel module creates a unified agent inbox where all customer communications — regardless of channel — are handled from one screen. Every incoming message from any channel creates or updates a Conversation record, which is linked to the relevant Incident or Service Request. Agents see full cross-channel history for each customer in one view.* |
| :---- |

## **12.2 Channel Coverage Matrix**

| Channel | Inbound | Outbound | Real-time? | Implementation | v1? |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Email | Yes | Yes | No | IMAP/SMTP via Frappe email engine; multi-account | Yes |
| Live Chat (Web Widget) | Yes | Yes | Yes | Socket.io \+ Redis pub/sub; JS embed snippet | Yes |
| WhatsApp Business | Yes | Yes | Yes | Meta Cloud API v18+ / Twilio for WhatsApp | Yes |
| Voice (Inbound) | Yes | Yes | Yes (CTI pop) | Twilio Voice SDK / Exotel REST \+ Frappe WebSocket | Yes |
| Customer Portal Form | Yes | N/A | No | Frappe web form; direct ITSM Incident/Request creation | Yes |
| Employee Portal Form | Yes | N/A | No | Frappe web form; ITSM Service Request creation | Yes |
| SMS | Yes | Yes | No | Twilio SMS / MSG91 (Phase 2\) | No — Phase 2 |
| Microsoft Teams | Yes | Yes | Yes | MS Teams Bot Framework (Phase 2\) | No — Phase 2 |
| Slack | Yes | Yes | Yes | Slack Bolt SDK (Phase 2\) | No — Phase 2 |
| Facebook Messenger | Yes | Yes | No | Meta Messenger API (Phase 3\) | No — Phase 3 |

## **12.3 DocType: ITSM Conversation**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | Conversation ID | Data | Auto: CONV-{\#\#\#\#\#} | Yes | Auto-naming |
| channel | Channel | Select | Email,Chat,WhatsApp,Voice,Portal,API | Yes | Source channel |
| status | Status | Select | Open,Assigned,In Progress,Pending,Resolved,Closed | Yes | Conversation state |
| linked\_incident | Linked Incident | Link | ITSM Incident | No | Escalated to an incident |
| linked\_request | Linked Request | Link | ITSM Service Request | No | Escalated to a service request |
| contact\_name | Contact Name | Data | — | No | Display name of external party |
| contact\_email | Contact Email | Data | Email | No | Email of external party |
| contact\_phone | Contact Phone | Data | Phone | No | Phone number |
| whatsapp\_number | WhatsApp Number | Data | Phone | No | International format e.g. \+91XXXXXXXXXX |
| customer | Customer | Link | Customer | No | Link to ERPNext Customer |
| assigned\_agent | Assigned Agent | Link | User | No | Agent handling this conversation |
| assigned\_team | Assigned Team | Link | ITSM Team | No | Queue/team |
| first\_message\_at | First Message At | Datetime | — | No | When conversation started |
| last\_message\_at | Last Message At | Datetime | — | No | Most recent activity timestamp |
| first\_response\_at | First Response At | Datetime | — | No | First agent reply timestamp |
| wait\_time\_seconds | Wait Time (seconds) | Int | — | No | Time from first message to agent pickup |
| csat\_score | CSAT Score | Select | 1,2,3,4,5 | No | Post-resolution rating |
| session\_tags | Tags | Table MultiSelect | ITSM Tag | No | Conversation labels |

## **12.4 DocType: ITSM Message**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | Message ID | Data | Auto: MSG-{\#\#\#\#\#} | Yes | Auto-naming |
| conversation | Conversation | Link | ITSM Conversation | Yes | Parent conversation |
| sender\_type | Sender Type | Select | Customer,Agent,Bot,System | Yes | Who sent this message |
| sender | Sender | Link | User | No | Frappe User (agents and internal bots) |
| sender\_name | Sender Name | Data | — | No | Display name (for external senders) |
| content | Content | Text | — | Yes | Message text; HTML for email; plain text for chat |
| content\_type | Content Type | Select | Text,HTML,Image,File,Audio,Video,System Note | Yes | How content should be rendered |
| attachment | Attachment | Attach | — | No | File attachment if content\_type=File |
| is\_internal | Is Internal Note | Check | — | No | Internal notes not shown to customer |
| channel\_message\_id | Channel Message ID | Data | — | No | External ID from WhatsApp/Twilio for dedup |
| sent\_at | Sent At | Datetime | — | Yes | Message timestamp |
| read\_at | Read At | Datetime | — | No | When recipient read the message |
| error | Delivery Error | Small Text | — | No | Channel delivery error message |

## **12.5 Unified Agent Inbox Requirements**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| OC-001 | Unified inbox: all open conversations across all channels in a single list; sortable by wait time, SLA due, priority, unread; filterable by channel, team, status | Must Have | Vue SPA at /itsm; left sidebar \= conversation list; right panel \= conversation detail \+ history |
| OC-002 | Real-time conversation updates: new messages appear in inbox without page refresh; active conversation auto-scrolls to new messages | Must Have | Socket.io events from Frappe; Redis pub/sub for cross-process message delivery |
| OC-003 | Agent presence status: Online, Away, Busy, Offline — set by agent or auto-set by inactivity timeout (configurable) | Must Have | ITSM Agent Status DocType updated by Socket.io; routing engine checks availability |
| OC-004 | Concurrent conversation limit: agent can be assigned maximum N simultaneous chat conversations (configurable per team) | Must Have | Assignment engine checks assigned active chat count before auto-assigning new chat |
| OC-005 | Conversation transfer: agent transfers conversation to another agent or queue; full context (all messages \+ linked records) transferred | Must Have | Transfer button; ITSM Message created 'Transferred from {agent} to {target}'; assigned\_agent updated |
| OC-006 | Full customer history: in conversation panel, show all past conversations and linked incidents for this customer/contact across all channels | Must Have | API query: ITSM Conversation where contact\_email/whatsapp\_number \= current contact; chronological |
| OC-007 | Quick replies: canned response selector in chat/WhatsApp reply box; supports Jinja variables (customer name, incident ID, SLA due) | Must Have | Saved Replies lookup with search; Jinja render server-side before send |
| OC-008 | File sending: agents can send files in chat and WhatsApp; customers can attach files; previewed inline in conversation | Must Have | File upload to Frappe private files; WhatsApp Media API for image/PDF/doc types |
| OC-009 | Typing indicator: agent sees '...' when customer is typing in live chat | Should Have | Socket.io typing\_start/typing\_stop events from chat widget; displayed in conversation header |
| OC-010 | Escalate conversation to ticket: one-click 'Create Incident' or 'Create Request' from conversation; ticket pre-filled from conversation context | Must Have | Button in conversation toolbar; opens incident/request form pre-filled with channel, contact, conversation summary |
| OC-011 | CSAT after resolution: post-resolution rating sent via original channel (chat, WhatsApp, email); 1–5 star; result linked to conversation and agent | Must Have | Triggered when conversation status→Resolved; channel-specific template; result stored on conversation |
| OC-012 | Queue dashboard: supervisor view showing all queues (by team/channel), conversations in queue, wait times, agent utilisation — real-time | Must Have | Separate queue dashboard screen; data from ITSM Conversation API; auto-refreshes every 30s |
| OC-013 | Conversation tags: agents tag conversations; tags used for reporting (top issue categories, escalation reasons) | Should Have | Tag multi-select on conversation; tag frequency in omnichannel analytics report |
| OC-014 | Bot-to-human handoff: Virtual Agent hands off to human agent with full bot conversation context preserved; agent sees bot transcript | Must Have | Handoff event from bot engine; ITSM Message records include bot messages; assigned\_agent set on handoff |

## **12.6 Email Integration**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| EMAIL-001 | Multiple email accounts: configure separate inbound email accounts per team (support@, billing@, hr@); each maps to routing rules | Must Have | ITSM Email Account DocType extends Frappe Email Account; routing config per account |
| EMAIL-002 | Email-to-conversation: inbound email creates ITSM Conversation; subject becomes title; if subject contains \[INC-YYYY-NNNNN\], message threaded to existing incident | Must Have | Email listener job; pattern matching on subject; ITSM Conversation created or updated |
| EMAIL-003 | Email threading: all replies in same email thread (matching In-Reply-To / References headers) appended to same conversation | Must Have | Message-ID and In-Reply-To header matching; same thread \= same conversation |
| EMAIL-004 | HTML and plain text: system renders outbound emails with HTML template branded per portal; fallback plain text for legacy clients | Must Have | ITSM Email Template DocType; sendgrid-compatible HTML templates |
| EMAIL-005 | Attachment handling: email attachments stored in Frappe private files; shown inline in conversation timeline | Must Have | MIME multipart parsing; attachments linked to ITSM Message record |
| EMAIL-006 | Spam and loop prevention: auto-reply loop detection (no ticket from auto-responders); email header X-ITSM-Loop prevents recursive replies | Must Have | Check Precedence: bulk/list headers; X-ITSM-Loop: yes header on all outbound system emails |

## **12.7 WhatsApp Integration**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| WA-001 | Meta Cloud API integration: register WhatsApp Business number; receive inbound messages via webhook; send outbound messages via API | Must Have | Webhook endpoint /api/method/frappe\_itsm.omnichannel.whatsapp\_webhook; HMAC verification |
| WA-002 | Message types: receive and send text, image, document, audio; location messages shown as link; sticker/reaction — acknowledge but no response required | Must Have | Message type routing in webhook handler; image/doc downloaded and stored as Frappe attachment |
| WA-003 | WhatsApp templates: use pre-approved Meta message templates for first outbound contact and CSAT surveys; free-form messages in active conversation window (24h) | Must Have | ITSM WhatsApp Template DocType; template selection enforced for first outbound message |
| WA-004 | Opt-out management: if user sends 'STOP' or 'Unsubscribe', contact flagged as opted-out; no further WhatsApp messages sent | Must Have | Keyword detection in webhook handler; ITSM Conversation Contact opt-out flag set |
| WA-005 | WhatsApp CSAT: post-resolution survey sent as WhatsApp Interactive Message with button choices (1–5 star) | Should Have | Meta Interactive Message with reply\_button type; response mapped to csat\_score |

# **13\. Module 8 — Reporting & Dashboards**

## **13.1 Pre-Built Dashboards**

| Dashboard Name | Audience | Key Widgets | Refresh |
| :---- | :---- | :---- | :---- |
| Executive Overview | CTO, VP IT | MTTR trend, SLA compliance %, incident volume by category, top 5 recurring problems, change success rate, CSAT trend | Daily |
| Operations Dashboard | IT Manager, Team Lead | Live queue depth by team, SLA breach forecast (next 4h), agent utilisation heatmap, incidents by priority, unresolved \> 24h | Real-time (30s) |
| Agent Dashboard | Individual Agent | My open tickets by priority, my SLA timers (countdown), my CSAT score (rolling 30 days), my pending approvals | Real-time (30s) |
| Service Desk | Service Desk Manager | All-channel queue status (Email/Chat/WA/Voice), agent presence status board, first call resolution rate, abandoned chat rate, avg wait time | Real-time (30s) |
| Change Management | Change Manager | Upcoming changes (calendar extract), RFC by status, change success/failure rate, CAB approval cycle time, unauthorized changes count | Hourly |
| CMDB Health | Asset Manager | CI count by class, data completeness score per class, stale CIs (not updated 90d), warranty expiry forecast (30/60/90 day), orphaned CIs | Daily |
| SLA Compliance | IT Manager | SLA compliance % by priority/team/agent, breach count trend, top 10 most breached categories, OLA compliance if configured | Daily |
| Knowledge Base | KB Manager | Articles published this month, deflection rate trend, top 10 articles by views, low-rated articles, articles expiring in 30 days | Daily |
| AI Performance | ITSM Admin | Bot containment rate, classification accuracy, KB suggestion click-through rate, auto-classification override rate | Weekly |
| Asset Inventory | Asset Manager | Assets by status/type, assets expiring warranty, software license compliance (used vs purchased), asset depreciation NBV | Daily |

## **13.2 KPI Library — Core Metrics**

| KPI | Formula | Default Target | Category |
| :---- | :---- | :---- | :---- |
| SLA Compliance Rate | Incidents within SLA / Total Incidents × 100 | ≥ 92% | SLA |
| First Call Resolution (FCR) | Incidents closed without reassignment / Total Incidents × 100 | ≥ 70% | Quality |
| Mean Time to Respond (MTTR) | Avg(first\_response\_at − created\_at) for closed incidents | P3 \< 2h | SLA |
| Mean Time to Resolve | Avg(resolution\_at − created\_at) for closed incidents | P3 \< 24h | SLA |
| Customer Satisfaction (CSAT) | Avg(csat\_score) from post-resolution surveys | ≥ 4.2 / 5.0 | Customer |
| Reopen Rate | Reopened incidents / Resolved incidents × 100 | \< 3% | Quality |
| Backlog Growth | New tickets − Closed tickets (weekly trend) | ≤ 0 (shrinking) | Volume |
| Agent Utilisation | Assigned ticket hours / Available hours × 100 | 65–80% | Productivity |
| Change Success Rate | Successful changes / Total changes × 100 | ≥ 96% | Change |
| Failed Change Rate | Failed/Rolled Back changes / Total changes × 100 | \< 3% | Change |
| KB Deflection Rate | Portal sessions resolved via KB / Total portal sessions × 100 | ≥ 20% | Self-Service |
| Catalog Fulfillment SLA | RITMs resolved within SLA / Total RITMs × 100 | ≥ 90% | Catalog |
| P1 Incident Response | P1 incidents with first response within 15 min / Total P1 × 100 | ≥ 95% | SLA |
| Unauthorized Change Rate | RFCs raised retrospectively / Total changes × 100 | \< 1% | Compliance |
| Problem Recurrence Rate | Problems with same root cause re-opened / Total problems × 100 | \< 5% | Quality |

## **13.3 Functional Requirements**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| RPT-001 | Report builder: admin can create custom reports on any ITSM DocType — select fields, filter conditions, group-by, sort, aggregate (count/sum/avg/min/max) | Must Have | Custom report builder UI in Admin Portal; reports saved as ITSM Custom Report |
| RPT-002 | Visualisation types: number card, bar chart (horizontal/vertical), line chart, area chart, pie chart, donut chart, data table, gauge, heat map | Must Have | Chart.js or Recharts library; Vue wrapper components; configured per widget |
| RPT-003 | Dashboard builder: drag-and-drop widget placement on custom dashboard; resize widgets; share with role or user | Should Have | Grid layout component; dashboard config stored as JSON; sharing via role or user list |
| RPT-004 | Scheduled reports: configure report to run on schedule (daily/weekly/monthly); email PDF and/or Excel export to distribution list | Must Have | ITSM Scheduled Report DocType; background job generates PDF via Frappe print \+ wkhtmltopdf; emails via Frappe emailer |
| RPT-005 | Drill-down: click chart segment → open filtered list of underlying records; e.g., click 'P1 Breached SLA' → list of P1 incidents that breached | Must Have | Chart click event passes filter params to ITSM list view URL |
| RPT-006 | Date range picker: relative ranges (today, last 7 days, last 30 days, this month, YTD) and absolute custom ranges | Must Have | Frappe DateRange component integrated in all dashboard filters |
| RPT-007 | Period comparison: KPI cards show % change vs previous period with up/down trend indicator | Must Have | Computed comparison in API; percentage delta rendered with colour-coded arrow |
| RPT-008 | Export: every report and dashboard exportable as PDF, Excel (.xlsx), and CSV | Must Have | Server-side PDF generation; Excel via openpyxl; CSV via Python csv module |
| RPT-009 | Real-time queue metrics: live conversation queue depths, agent presence counts — polled every 30s from WebSocket or REST | Must Have | Agent presence and queue metrics from Redis cache; API endpoint /api/method/frappe\_itsm.reports.queue\_metrics |
| RPT-010 | Threshold alerts: admin defines KPI threshold; if breached, system sends alert notification (in-app \+ email) to configured recipients | Should Have | ITSM KPI Alert Rule DocType; background evaluator job every 15 min |

# **14\. Module 9 — AI & Virtual Agent**

## **14.1 AI Feature Matrix**

| Feature | Description | API / Model | v1? |
| :---- | :---- | :---- | :---- |
| Intent Classification | Classify incoming ticket/message into Category \+ Sub-Category from text | Fine-tuned classifier on historical tickets OR GPT-4o with structured output | Yes |
| Auto-routing suggestion | Suggest Assignment Team from ticket text \+ category | Same classifier pipeline; team as additional output field | Yes |
| Priority suggestion | Suggest Impact \+ Urgency from ticket text | Classifier; agent confirms or overrides | Yes |
| KB Article Suggestion | During ticket creation, find top-3 relevant KB articles | Keyword search \+ optional embedding similarity (pgvector) | Yes |
| Reply Assist | Suggest draft reply to agent based on ticket context \+ past resolutions | GPT-4o with system prompt including incident context \+ KB snippets | Yes |
| Ticket Summarisation | Summarise long incident/conversation for handoff notes | GPT-4o; triggered by 'Summarise' button on incident form | Yes |
| Sentiment Analysis | Classify customer message sentiment: Positive/Neutral/Frustrated/Angry | GPT-4o or lightweight BERT model; shown as emoji indicator on conversation | Yes |
| Duplicate Detection | Flag new incidents likely duplicate of open incident (same category \+ requester \+ similar subject) | Text similarity; threshold configurable; alert banner (not block) | Yes |
| Virtual Agent (Chatbot) | NLU chatbot handling top-10 self-service intents in chat/WhatsApp | GPT-4o with function calling \+ Frappe ITSM API; intent flows defined in config | Yes |
| Anomaly Detection | Alert when incident volume spikes beyond normal baseline | Statistical model (rolling average \+ std dev); alert to IT Manager | Phase 2 |
| Resolution Time Prediction | Predict resolution time at ticket creation for SLA planning | ML regression model trained on historical data | Phase 2 |

## **14.2 DocType: ITSM Virtual Agent Config**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | Config Name | Data | — | Yes | e.g., 'Chat Widget Bot' or 'WhatsApp Bot' |
| channel | Channel | Select | Chat,WhatsApp,Email Auto-Reply | Yes | Deployment channel |
| status | Status | Select | Active,Inactive,Test Mode | Yes | Active bots process real messages |
| greeting\_message | Greeting Message | Small Text | — | Yes | First message bot sends to new conversation |
| fallback\_message | Fallback Message | Small Text | — | Yes | When bot cannot handle intent |
| handoff\_message | Handoff Message | Small Text | — | Yes | Message shown when transferring to human |
| max\_bot\_turns | Max Bot Turns | Int | Default:10 | No | After N turns without resolution, auto-handoff |
| handoff\_team | Handoff Team | Link | ITSM Team | Yes | Team to assign conversation after handoff |
| supported\_intents | Supported Intents | Table | ITSM Bot Intent (child) | No | List of intents this bot handles |
| working\_hours\_only | Active During Working Hours Only | Check | — | No | If checked, bot deactivates outside working hours; fallback message shown |
| ai\_provider | AI Provider | Select | OpenAI GPT-4o,Azure OpenAI,Sarvam AI,Anthropic Claude | Yes | LLM backend for NLU and response generation |
| api\_key\_secret | API Key (Secret) | Password | — | Yes | Stored encrypted; never exposed to frontend |
| system\_prompt | System Prompt | Text Editor | — | Yes | Instructions given to LLM; includes org context, tone, constraints |

## **14.3 Top-10 Default Bot Intents**

| Intent Name | Trigger Phrases (examples) | Bot Action | Creates ITSM Record? |
| :---- | :---- | :---- | :---- |
| check\_ticket\_status | status of my ticket, where is my request, update on INC-2026-00123 | Lookup ITSM Incident by name or latest incident for user; return status \+ SLA due | No (read-only) |
| raise\_incident | not working, can't access, error, system down, issue with | Collect subject \+ category via conversational form; create ITSM Incident via API | Yes — ITSM Incident |
| request\_service | I need, requesting, can I get, please provide | Guide user to relevant catalog items; initiate service request | Yes — ITSM Service Request |
| password\_reset | forgot password, can't login, account locked, reset my password | Trigger password reset via ERPNext/AD API or raise Request | Maybe — depends on integration |
| kb\_search | how do I, what is, help with, documentation for, guide for | Search ITSM Knowledge Article; return top 3 results with links | No |
| schedule\_callback | call me, speak to agent, talk to someone, human please | Capture preferred callback time; create ITSM Incident with source=Phone; schedule callback | Yes — ITSM Incident |
| report\_major\_outage | everything is down, complete outage, all users affected, nobody can access | Escalate directly to human; flag as potential Major Incident; notify on-call manager | Yes — Major Incident flag |
| update\_ticket | adding info, update on my ticket, I found the issue | Attach message as comment to existing incident (identified by ticket ID or latest open) | No — updates existing |
| CSAT\_feedback | feedback, rating, service was, experience was | Capture CSAT score for recently resolved ticket | No — updates existing |
| general\_faq | office hours, support hours, contact number, who to contact for | Answer from pre-configured FAQ list in system prompt; no API call needed | No |

## **14.4 Functional Requirements**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| AI-001 | Auto-classification on ticket save: when ticket saved without category/priority, AI classifier suggests values; agent can accept or override with one click | Must Have | Server-side Python call to LLM API on new incident save; suggestions shown as highlighted fields |
| AI-002 | KB suggestion panel: during incident/request creation, as subject is typed, matching KB articles appear in collapsible side panel; click to view article | Must Have | Debounced keyup → API call → sidebar results; tracks whether article viewed before ticket submitted |
| AI-003 | Reply assist: 'Suggest Reply' button in agent reply editor; generates contextually relevant draft reply using incident description, category, KB articles, and resolution\_code of similar past incidents | Must Have | Button triggers API call to LLM with structured context; draft inserted into editor; agent edits before sending |
| AI-004 | Ticket summarisation: 'Summarise' button on incident form generates a 3–5 sentence summary of the full activity timeline for handoff | Must Have | LLM call with full activity log as input; output inserted as internal note |
| AI-005 | Sentiment indicator: incoming messages (chat, WhatsApp, email) analysed for sentiment; frustrated/angry conversations visually flagged in agent inbox for priority pickup | Must Have | Lightweight sentiment classifier called on new message save; sentiment stored on ITSM Message; inbox renders emoji |
| AI-006 | Virtual Agent chatbot: bot handles top-10 intents in chat widget and WhatsApp; conversational multi-turn flows; function calling to ITSM APIs (check ticket, create incident) | Must Have | GPT-4o with function calling; bot engine in frappe\_itsm/bot/; intent routes to Python functions that call Frappe APIs |
| AI-007 | Bot handoff to human: after max\_bot\_turns or on 'speak to agent' intent, bot sends handoff\_message, creates/updates Conversation, assigns to handoff\_team, agent sees full bot transcript | Must Have | ITSM Bot Turn records preserved; conversation assigned; agent desktop notified via Socket.io |
| AI-008 | Duplicate detection alert: on new incident save, system checks for open incidents same category \+ requester \+ similar subject (Levenshtein or embedding similarity); shows alert banner if \> 70% match | Should Have | Server-side check; ITSM Duplicate Alert record created; agent can merge or dismiss |
| AI-009 | AI usage audit: every AI suggestion logged (model, input hash, output, accepted/rejected by agent) | Must Have | ITSM AI Log DocType; enables accuracy tracking and model fine-tuning |
| AI-010 | Configurable AI provider: admin selects AI provider per feature (classification vs reply assist vs bot); API key stored encrypted in ITSM Virtual Agent Config or ITSM AI Config DocType | Must Have | Provider abstraction layer in Python; switching provider requires no code change |

# **15\. Module 10 — Asset Management**

## **15.1 Overview**

| *Asset Management tracks the complete lifecycle of IT assets — from procurement through deployment, maintenance, and disposal — integrated with the CMDB and ERPNext for financial tracking. Hardware assets become CIs in CMDB once deployed. Software assets are tracked by license entitlements.* |
| :---- |

## **15.2 DocType: ITSM Asset**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| name | Asset ID | Data | Auto: AST-{\#\#\#\#\#} | Yes | Auto-naming |
| asset\_name | Asset Name | Data | — | Yes | Human-readable name (e.g., 'Dell Latitude 5540 \- SN12345') |
| asset\_type | Asset Type | Select | Hardware,Software License,SaaS Subscription | Yes | Top-level asset type |
| asset\_category | Asset Category | Link | ITSM Asset Category | Yes | e.g., Laptop, Server, Antivirus License |
| status | Status | Select | On Order,In Stock,In Use,In Repair,Retired,Disposed,Stolen | Yes | Lifecycle state |
| serial\_number | Serial Number | Data | — | No | Manufacturer serial (hardware only) |
| model | Model | Data | — | No | Hardware model name |
| manufacturer | Manufacturer | Data | — | No | Hardware manufacturer name |
| vendor | Vendor | Link | Supplier | No | Purchase supplier (ERPNext Supplier) |
| purchase\_order | Purchase Order | Link | Purchase Order | No | ERPNext PO that procured this asset |
| purchase\_date | Purchase Date | Date | — | No | When asset was purchased |
| purchase\_cost | Purchase Cost | Currency | — | No | Original purchase price |
| company | Company | Link | Company | Yes | Owner company |
| location | Location | Link | ITSM Location | No | Physical location (building, room, rack) |
| department | Department | Link | Department | No | Assigned department |
| assigned\_to | Assigned To | Link | User | No | User the asset is deployed with |
| assigned\_date | Assigned Date | Date | — | No | When assigned to current user |
| warranty\_expiry | Warranty Expiry Date | Date | — | No | Alert 90 days before |
| amc\_expiry | AMC Expiry Date | Date | — | No | Annual Maintenance Contract expiry; alert 60 days before |
| depreciation\_method | Depreciation Method | Select | Straight Line,Written Down Value,None | No | How asset depreciates |
| useful\_life\_years | Useful Life (Years) | Float | — | No | For depreciation calculation |
| salvage\_value | Salvage Value | Currency | Default:0 | No | Value at end of useful life |
| current\_nbv | Current NBV | Currency | — | No | Net Book Value — auto-calculated |
| linked\_ci | Linked CI | Link | ITSM CI | No | CMDB record for deployed hardware asset |
| linked\_erp\_asset | ERPNext Asset | Link | Asset | No | Link to ERPNext Asset DocType for financial integration |
| qr\_code | QR Code | Attach Image | — | No | Auto-generated QR label image |
| disposal\_date | Disposal Date | Date | — | No | Set when status=Disposed |
| disposal\_method | Disposal Method | Select | Sold,Donated,Scrapped,Returned to Vendor,Certified Destruction | No | How asset was disposed |
| disposal\_certificate | Disposal Certificate | Attach | — | No | Evidence of secure disposal |
| notes | Notes | Text Editor | — | No | Free-text notes |

## **15.3 Software License Tracking**

| Field Name | Label | Type | Options / Link | Req? | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| software\_name | Software Name | Data | — | Yes | Product name |
| vendor | Vendor | Link | Supplier | No | Software vendor |
| license\_type | License Type | Select | Per User Named,Per User Concurrent,Per Device,Site License,Enterprise,Open Source | Yes | Licensing model |
| license\_count\_purchased | Licenses Purchased | Int | — | Yes | Total licenses bought |
| license\_count\_deployed | Licenses Deployed | Int | — | No | Auto-count from assignments; read-only |
| compliance\_status | Compliance Status | Select | Compliant,Over-Licensed (Waste),Under-Licensed (Risk) | No | Auto-calculated from purchased vs deployed |
| license\_key | License Key | Password | — | No | Stored encrypted |
| expiry\_date | License Expiry | Date | — | No | Alert 90 days before |
| version | Version | Data | — | No | Current licensed version |
| eol\_date | End of Life Date | Date | — | No | Vendor EoL date; alert 180 days before |

## **15.4 Functional Requirements**

| Req ID | Requirement | Priority | Notes |
| :---- | :---- | :---- | :---- |
| AST-001 | Asset lifecycle management: full lifecycle from On Order → In Stock → In Use → In Repair → Retired → Disposed; each transition logged with user, date, and reason | Must Have | Workflow on ITSM Asset status field; each transition creates ITSM Asset History record |
| AST-002 | CMDB auto-link: when asset status → In Use, system checks for existing CI with same serial number; if found, links asset to CI; if not found, prompts to create CI | Must Have | Server-side hook on status transition; creates ITSM CI from asset template if user confirms |
| AST-003 | ERPNext Asset integration: when ITSM Asset created with purchase\_order link, auto-create or link ERPNext Asset DocType; depreciation entries flow from ERPNext | Should Have | Server-side call to ERPNext Asset API on save; depreciation via ERPNext Asset Depreciation Schedule |
| AST-004 | Depreciation calculation: NBV auto-calculated from purchase\_cost, useful\_life\_years, depreciation\_method; displayed on asset record | Must Have | Python method calculates NBV on save; stored in current\_nbv |
| AST-005 | Warranty and AMC alerts: background job daily — alert to asset owner and IT Manager 90 days before warranty\_expiry; 60 days before amc\_expiry | Must Have | Scheduler job; ITSM Asset Alert record created; notification via email \+ in-app |
| AST-006 | Asset assignment tracking: full history of who had the asset, when assigned, when returned; current assignment visible on asset record | Must Have | ITSM Asset Assignment History child table; every assignment/return logged |
| AST-007 | QR code label generation: one-click generate QR code encoding asset ID; downloadable PNG for physical labelling | Should Have | Python qrcode library; QR image stored as Frappe attachment on asset; printable label format |
| AST-008 | Asset disposal workflow: disposal request → approval → certificate upload → status=Disposed; links to CMDB CI retirement | Must Have | Disposal form with approval; disposal\_certificate required before Disposed status allowed |
| AST-009 | Software license compliance: ITSM Software License record tracks purchased vs deployed; compliance\_status auto-computed; compliance dashboard shows all licenses | Must Have | license\_count\_deployed \= count of ITSM Asset Deployment records for this software; compliance badge |
| AST-010 | Asset inventory report: filterable by status, type, location, department, warranty expiry; exportable Excel/PDF for audit | Must Have | Pre-built Asset Inventory Report with advanced filters; export buttons |
| AST-011 | Bulk import: CSV import for initial asset population; field mapping wizard; creates ITSM Asset records and optionally ITSM CI records | Must Have | Custom import page; column mapping saved as template; validation errors shown per row |
| AST-012 | Asset request via catalog: employees request hardware/software via Service Catalog; fulfillment team deploys from stock; ITSM Asset updated on deployment | Must Have | Catalog item type=Asset; fulfillment task includes 'Update ITSM Asset assignment' step |

# **16\. SLA Engine Design**

## **16.1 SLA Architecture**

| *The SLA Engine is a standalone Python module (frappe\_itsm/sla/) that evaluates SLA policies against ITSM records, creates and updates SLA instances, and triggers escalation events. It runs as a background scheduler job every 5 minutes and is also triggered on every status change of an ITSM record.* |
| :---- |

## **16.2 DocType: ITSM SLA Policy**

| Field Name | Label | Type | Description |
| :---- | :---- | :---- | :---- |
| name | Policy Name | Data | e.g., Standard IT SLA, VIP Customer SLA |
| document\_type | Applies To | Select | ITSM Incident, ITSM Service Request, ITSM Change |
| is\_default | Is Default | Check | Fallback policy if no conditions match |
| conditions | Conditions | Table — ITSM SLA Condition | Field-operator-value conditions; all must match |
| working\_hours | Working Hours | Link — ITSM Working Hours | Business hours schedule |
| holiday\_list | Holiday List | Link — ITSM Holiday List | Dates excluded from SLA calculation |
| response\_targets | Response Targets | Table — ITSM SLA Target | First Response time by priority |
| resolution\_targets | Resolution Targets | Table — ITSM SLA Target | Resolution time by priority |
| escalation\_rules | Escalation Rules | Table — ITSM SLA Escalation | Multi-level escalation at defined SLA % threshold |
| pause\_statuses | Pause on Status | Table MultiSelect | Statuses that pause SLA timer |
| fulfilled\_statuses | Fulfilled on Status | Table MultiSelect | Statuses that mark SLA complete |

## **16.3 SLA Calculation Logic**

* SLA Engine evaluates all active SLA policies against new/updated record using condition matching

* Matching policy (highest specificity first) is selected; default policy used if no conditions match

* ITSM SLA Instance created linking record \+ policy; response\_due and resolution\_due calculated

* Calculation uses only working hours defined in associated working hours schedule

* Holiday list dates excluded from calculation (timer jumps to next working day start)

* On-hold statuses (e.g., Pending): timer paused from on\_hold\_since; hold duration logged to ITSM SLA Hold Log

* Hold duration subtracted from elapsed time when calculating SLA compliance

* SLA timer evaluated every 5 minutes by background job; sla\_status updated on ITSM record

* Escalation events triggered when elapsed\_time / resolution\_due crosses configured thresholds (e.g., 50%, 75%, 100%)

## **16.4 DocType: ITSM SLA Escalation Rule**

| Field Name | Label | Type | Description |
| :---- | :---- | :---- | :---- |
| sla\_policy | SLA Policy | Link | Parent policy |
| trigger\_at\_percent | Trigger At (% of SLA) | Int | e.g., 75 triggers at 75% of resolution time |
| action | Action | Select | Notify Only, Reassign \+ Notify, Escalate Priority, Escalate Priority \+ Reassign |
| notify\_roles | Notify Roles | Table MultiSelect | Roles to notify (e.g., ITSM Manager) |
| notify\_users | Notify Users | Table — User | Specific users to notify |
| reassign\_to\_team | Reassign To Team | Link | ITSM Team — for Reassign actions |
| priority\_upgrade | Upgrade Priority To | Select | P1-Critical, P2-High, P3-Moderate — for escalate priority actions |
| notification\_template | Notification Template | Link | ITSM Notification Template |

# **17\. Workflow & Automation Engine**

## **17.1 Overview**

| *The Workflow Engine allows ITSM Admins to build automated multi-step workflows without writing code. It combines Frappe's native Workflow DocType (for state machine approvals) with a custom ITSM Automation Rule engine (for event-triggered actions) and a custom Approval Portal for email-based approvals.* |
| :---- |

## **17.2 ITSM Automation Rule**

| Component | Description | Example |
| :---- | :---- | :---- |
| Trigger | What causes the automation to run | Document Created, Field Changed (status → Resolved), Scheduled (every day at 9am), Webhook Received |
| Conditions | Filter criteria — automation only runs if all conditions match | Priority \= P1 AND Category \= Network AND Assigned Team is not set |
| Actions | What the automation does when triggered | Send Email, Send WhatsApp, Create Record, Update Record, Assign Record, Run Server Script, Create Incident, Post Comment |
| Action Sequence | Actions execute in order; can be parallel or sequential | 1\. Assign to Network Team → 2\. Send WhatsApp to team lead → 3\. Post internal note |
| Error Handling | If action fails, log to ITSM Automation Log; optionally retry N times | Retry 3 times on WhatsApp API failure; notify admin if all retries fail |

## **17.3 Built-in Action Library**

| Action | Parameters | Notes |
| :---- | :---- | :---- |
| Send Email | Template, To (user/role/field), CC, subject | Uses ITSM Notification Template; Jinja variable substitution |
| Send WhatsApp | Template/free-text, To (phone field or contact) | Requires WhatsApp integration configured; enforces 24h window rule |
| Assign Record | User (specific/round-robin/least-loaded), Team | Resolves round-robin from team member list in Redis; updates assigned\_to field |
| Update Field | Field name, New value (static/Jinja expression) | Server-side field update; triggers document hooks; full audit trail |
| Create Incident | Title template, Category, Priority, Assigned Team | Creates ITSM Incident from rule context; useful for escalation scenarios |
| Create Catalog Request | Catalog Item, Requester | Auto-submits a service request for a configured catalog item |
| Post Internal Comment | Comment text (Jinja template) | Posts comment with is\_internal=1; visible to agents only |
| Run Server Script | Named ITSM Script | Executes a sandboxed Python script with access to doc context; powerful escape hatch |
| Trigger Webhook | URL, Method, Payload template | Calls external REST API; response logged to ITSM Automation Log |
| Create Problem | Title, Category | Auto-creates ITSM Problem; useful for auto-problem-creation from incident threshold rule |
| Send In-App Notification | Message, User/Role | Creates ITSM Notification record for user; appears in notification bell |

## **17.4 Approval Portal**

* Approvers receive email notification with direct Approve / Reject buttons (signed URL, 7-day token expiry)

* Clicking Approve/Reject without login required — token carries approver identity

* Rejection requires comment (enforced on approval endpoint)

* Approval decisions logged to ITSM Change Approval / ITSM Catalog Approval with user, timestamp, and comment

* My Approvals screen in Agent Portal shows all pending approvals for logged-in user

* Approver can add comment and decide inline in portal — no email required

* Approval timeout: if no decision within configured hours, escalate to secondary approver or auto-decision (configurable)

# **18\. Integration Architecture**

## **18.1 ERPNext Integration**

| Integration Point | Direction | Method | Data Shared |
| :---- | :---- | :---- | :---- |
| User / Employee Sync | ERPNext → frappe\_itsm | Shared Frappe site — same DB | User, Employee, Department DocTypes directly accessible |
| Customer Sync | ERPNext → frappe\_itsm | Shared DB | Customer, Contact DocTypes used in omnichannel and incident forms |
| Supplier (Vendor) | ERPNext → frappe\_itsm | Shared DB | Supplier DocType linked in ITSM Asset and ITSM CI for vendor tracking |
| Purchase Order link | ERPNext → frappe\_itsm | Link field on ITSM Asset | Asset procurement PO linked; no data duplication |
| ERPNext Asset link | frappe\_itsm → ERPNext | frappe.get\_doc() call | ITSM Asset creates/links ERPNext Asset; depreciation via ERPNext |
| Journal Entry (depreciation) | frappe\_itsm → ERPNext | Server Script / Hook | Annual depreciation JE posted from ITSM Asset depreciation schedule |
| HR Leave (agent availability) | ERPNext → frappe\_itsm | API call on assignment | Check employee leave before auto-assigning incident to agent |

## **18.2 Azure AD / LDAP SSO**

* OAuth2 \+ SAML 2.0 supported via Frappe's built-in social login framework

* Azure AD app registration: redirect URI \= https://{site}/api/method/frappe.integrations.oauth2\_logins.login\_via\_azure

* User provisioning: first login auto-creates Frappe User; department \+ designation synced from Azure AD claims

* Role mapping: Azure AD group membership mapped to ITSM roles via ITSM SSO Role Mapping DocType

* LDAP fallback: LDAP integration for on-premise Active Directory via Frappe LDAP configuration

## **18.3 Jira Integration**

| Integration | Direction | Trigger | Data Synced |
| :---- | :---- | :---- | :---- |
| Create Jira Issue from Incident | frappe\_itsm → Jira | Manual button on Incident | INC title, description, priority → Jira issue; Jira issue key stored on Incident |
| Jira Status → Incident Update | Jira → frappe\_itsm | Jira webhook on issue transition | Jira Done/In Progress → updates Incident status via webhook endpoint |
| Jira Comment → Incident Comment | Jira → frappe\_itsm | Jira webhook on comment | Jira comment added as internal note on ITSM Incident |
| Incident → Jira Bug (Change-triggered) | frappe\_itsm → Jira | Change close\_code=Failed | Creates Jira bug for follow-up development work |

## **18.4 Monitoring Tool Integration**

| Tool | Integration Type | Method | Use Case |
| :---- | :---- | :---- | :---- |
| Grafana | Alert → Incident | Grafana Alerting webhook → /api/method/frappe\_itsm.integrations.monitoring.create\_incident | Auto-create P1/P2 Incident when Grafana alert fires |
| PagerDuty | Bi-directional | PagerDuty Events API v2 \+ PagerDuty webhook | ITSM P1 incidents create PD incident; PD ack/resolve syncs back |
| Zabbix | Alert → Incident | Zabbix Action webhook → frappe\_itsm endpoint | Auto-create Incident from Zabbix trigger; close on Zabbix recovery |
| Generic Webhook | Any tool → Incident | POST /api/method/frappe\_itsm.integrations.webhook.create\_incident | Standard webhook payload mapped to ITSM Incident fields |

# **19\. Non-Functional Requirements**

## **19.1 Performance**

| Metric | Target | Measurement |
| :---- | :---- | :---- |
| Page Load Time (Agent Portal) | \< 2 seconds (P95) on standard 10Mbps connection | Lighthouse performance audit; k6 load test |
| API Response Time | \< 500ms (P95) for standard CRUD operations | k6 load test with 100 concurrent users |
| SLA Timer Accuracy | SLA due time accurate to ± 1 minute | Automated test: create incident, advance clock, check timer value |
| Email-to-Incident Latency | Inbound email creates incident within 2 minutes of receipt | End-to-end test with timestamp comparison |
| Background Job Throughput | SLA evaluator processes 1,000 open tickets in \< 2 minutes | Benchmark test with synthetic data |
| Chat Message Delivery | \< 200ms end-to-end in live chat (agent → customer) | Socket.io round-trip latency test |
| Concurrent Users | System stable with 300 concurrent active users (500 total sessions) | k6 test simulating 300 concurrent users browsing \+ editing |
| Database Query Performance | No query \> 1s on P95 for list views with standard filters | Query profiler in MariaDB; optimise with indexes |

## **19.2 Security**

| Requirement | Description | Implementation |
| :---- | :---- | :---- |
| Role-based access control | Every DocType, field, and action governed by Frappe's permission engine; no bypass | Frappe role permissions \+ field-level permissions; tested per role in UAT |
| API authentication | All REST API calls require session cookie or API key \+ secret pair | Frappe built-in; API keys managed per user; no anonymous API endpoints except webhook receivers |
| Webhook signature verification | Inbound webhooks (WhatsApp, Jira, monitoring tools) verified using HMAC-SHA256 | Signature check in webhook handler; reject unverified requests with 403 |
| Secret encryption | API keys, WhatsApp tokens, AI API keys stored AES-256 encrypted in database | Frappe Password field type for secrets; never returned in API responses |
| SQL injection prevention | All queries via Frappe ORM (parameterised); no raw SQL with user input | Code review gate; no string-concatenated SQL; ORM-only policy |
| XSS prevention | Rich-text content (ticket descriptions, KB articles) sanitised with DOMPurify on render | Frontend DOMPurify; backend content sanitised before storage |
| Audit trail | Every document change, login, and API call logged to ITSM Audit Log and Frappe Access Log | Frappe access\_log enabled; custom audit log for ITSM state changes |
| HTTPS enforcement | All traffic encrypted in transit; HTTPS redirect enforced; HSTS header set | Nginx config; Let's Encrypt / org certificate |
| Data at rest | Sensitive fields (API keys, license keys) encrypted at field level | Frappe Password field; DB-level encryption optional per hosting policy |
| Confidential field masking | HR case fields visible only to HR role; customer contact data restricted by role | Frappe field-level permission with Read role restriction |

## **19.3 ITIL v4 Compliance Checklist**

| ITIL v4 Practice | Module | Implementation Status | Evidence |
| :---- | :---- | :---- | :---- |
| Incident Management | Module 1 | Full | Incident lifecycle, SLA, major incident, escalation, problem promotion |
| Problem Management | Module 2 | Full | RCA, KEDB, workaround, problem tasks, PIR |
| Change Enablement | Module 3 | Full | Standard/Normal/Emergency RFC, CAB, risk assessment, change calendar, PIR |
| Service Configuration Mgmt | Module 4 | Full | CMDB CI hierarchy, relationships, impact analysis, change schedule |
| Service Catalog Management | Module 5 | Full | Catalog items, approval, RITM, fulfillment, SLA per item |
| Knowledge Management | Module 6 | Full | Article lifecycle, KEDB integration, version control, visibility control |
| Service Desk | Modules 1,7 | Full | Multi-channel, unified inbox, CSAT, escalation |
| Service Level Management | SLA Engine | Full | SLA policies, OLA config, escalation chains, compliance reporting |
| Monitoring & Event Mgmt | Integration | Partial — webhook receivers implemented; active monitoring in Phase 2 | Webhook endpoints for Grafana, Zabbix, PagerDuty |
| Release Management | Phase 2 | Out of Scope v1 | Planned for Phase 2 as extension to Change Management module |

## **19.4 Availability & Data Residency**

* Target availability: 99.5% uptime (\< 44h downtime/year) — achievable on self-hosted Frappe with standard server redundancy

* Backup policy: daily automated MariaDB dump \+ Frappe private files backup; 30-day retention

* Data residency: all data stored in organisation's own infrastructure (self-hosted) or chosen Frappe Cloud region; no data leaves the site to third-party services except AI API calls (opt-in)

* AI API privacy: ticket data sent to OpenAI/Sarvam for AI features should be sanitised to remove PII before transmission; configurable data masking level

* Disaster recovery: documented runbook for restore from backup; target RTO \< 4h, RPO \< 24h

# **20\. Permission & Role Matrix**

## **20.1 Module-Level Permissions**

| DocType | ITSM Agent | Senior Agent | IT Manager | Change Mgr | ITSM Admin | Employee | Customer |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| ITSM Incident | R/W (assigned) | R/W (team) | Full | Read | Full | Create \+ Read Own | Create \+ Read Own |
| ITSM Problem | Read | R/W | Full | Full | Full | None | None |
| ITSM Change | Read | Read | Full | Full | Full | None | None |
| ITSM CI | Read | R/W | Full | Read | Full | None | None |
| ITSM Asset | Read | R/W | Full | None | Full | Read (own assigned) | None |
| ITSM Catalog Item | Read | Read | Full | None | Full | None | None |
| ITSM Service Request | Read (assigned) | R/W (team) | Full | None | Full | Create \+ Read Own | None |
| ITSM Knowledge Article | Read | R/W/Create | Full | None | Full | Read (public) | Read (public) |
| ITSM Conversation | R/W (assigned) | R/W (team) | Full | None | Full | Read Own | Read Own |
| ITSM SLA Policy | None | None | Read | None | Full | None | None |
| ITSM Automation Rule | None | None | Read | None | Full | None | None |
| ITSM Report / Dashboard | Read | Read | R/W | Read | Full | None | None |
| *R \= Read, W \= Write, Full \= Read/Write/Delete/Submit. 'Assigned' \= only records assigned to this user. 'Team' \= all records assigned to their team. 'Own' \= records created by this user. Admin Portal (configuration screens) accessible only to ITSM Admin and Super Admin roles.* |  |  |  |  |  |  |  |

# **21\. Implementation Roadmap**

## **21.1 Phased Delivery Plan**

| Phase | Duration | Modules Delivered | Team |
| :---- | :---- | :---- | :---- |
| Phase 1 — ITSM Core | Weeks 1–12 (3 months) | Core platform setup, DocType scaffolding, Incident Management (full), Problem Management (full), Change Management (full), SLA Engine, Basic Workflow Engine, Basic Reporting (5 dashboards), Employee Portal (basic), Admin Portal (config) | 3 Backend \+ 2 Frontend \+ 1 QA |
| Phase 2 — Catalog \+ CMDB | Weeks 13–20 (2 months) | Service Catalog (full), CMDB (full), Asset Management (full), Knowledge Base (full), ERPNext integration complete, Advanced SLA (OLA, escalation chains), Reporting (all 10 dashboards) | 3 Backend \+ 2 Frontend \+ 1 QA |
| Phase 3 — Omnichannel | Weeks 21–28 (2 months) | Omnichannel (Email \+ Chat \+ WhatsApp \+ Voice), Unified Agent Inbox, Customer Portal (full), CSAT engine, WhatsApp integration, Voice CTI | 3 Backend \+ 2 Frontend \+ 1 QA \+ 0.5 Integration |
| Phase 4 — AI \+ Polish | Weeks 29–36 (2 months) | AI classification, KB suggestion, Reply assist, Chatbot (top-10 intents), Sentiment analysis, Duplicate detection, Azure AD SSO, Jira integration, Monitoring webhooks, Performance tuning, UAT, Go-live | 2 Backend \+ 1 Frontend \+ 1 AI \+ 1 QA |

## **21.2 Phase 1 — Sprint Detail**

| Sprint | Weeks | Key Deliverables |
| :---- | :---- | :---- |
| S1 | 1–2 | App scaffold (frappe\_itsm), core DocTypes (Category, Team, Agent, Location, Tag), Frappe app hooks, naming series config, base permission roles |
| S2 | 3–4 | ITSM Incident DocType (all fields), Incident state machine (Frappe Workflow), Priority Matrix config, Impact × Urgency auto-calc, naming series INC-YYYY-\#\#\#\#\# |
| S3 | 5–6 | SLA Engine v1: ITSM SLA Policy, ITSM SLA Instance, working hours, holiday list, response/resolution due calculation, background evaluator job |
| S4 | 7–8 | Incident SLA timers on list view, escalation engine v1 (2-level), CSAT trigger on resolution, auto-close background job, major incident flag, parent-child linking |
| S5 | 9–10 | ITSM Problem DocType, state machine, RCA form (5-Whys, Fishbone tabs), KEDB lookup during incident creation, workaround publishing, problem tasks |
| S6 | 11–12 | ITSM Change DocType (all fields), change types, risk assessment questionnaire, risk score calculation, CAB Meeting DocType, blackout window DocType and validation |
| S7 | 13–14 | Change approval workflow (sequential \+ parallel), email-based CAB voting (signed URL tokens), change calendar API, change freeze period validation |
| S8 | 15–16 | Change tasks (pre/impl/post), PIR workflow, rollback execution flow, change metrics, Admin Portal v1 (SLA config, routing config, team management) |
| S9 | 17–18 | Basic Agent Portal (Vue SPA) — incident list, incident detail, activity feed, reply editor, saved replies, KB suggestion panel |
| S10 | 19–20 | Operations Dashboard, SLA Compliance Report, Change Management Dashboard, scheduled report engine (email PDF), employee self-service portal v1 |
| S11 | 21–22 | Email integration (IMAP/SMTP multi-account, email-to-incident, threading, loop prevention), Automation Rule engine v1 (5 action types) |
| S12 | 23–24 | Integration testing, bug fixing, performance tuning, UAT preparation, documentation, Phase 1 deployment to staging |

## **21.3 Risk Register**

| Risk | Probability | Impact | Mitigation |
| :---- | :---- | :---- | :---- |
| WhatsApp Meta Business API approval delayed (6–8 weeks) | Medium | Medium | Start Meta Business Verification at project start; build Email \+ Chat first; WhatsApp added when approved |
| ERPNext data model mismatch (Employee, Customer fields differ from expected) | Medium | Low | Audit ERPNext DocType fields before Phase 1 starts; adapt ITSM link fields accordingly |
| AI API cost overrun (OpenAI GPT-4o per-token pricing) | Low | Medium | Implement token budget per request; cache common classification results in Redis; use smaller model for classification |
| ITIL process resistance from IT team | High | High | ITIL training workshop before go-live; champion user identified in IT team; change management plan for adoption |
| Performance degradation at scale (300+ concurrent users) | Low | High | Load test at end of each phase; MariaDB index optimisation after Phase 1; Redis caching for expensive queries |
| Frappe Workflow limitations for complex CAB approval chains | Medium | Medium | Evaluate early in Phase 1; supplement Frappe Workflow with custom approval engine if needed |
| Data migration from legacy tools (Excel, email) complex and incomplete | High | Medium | Define migration scope in Week 1; build CSV import for Incidents, CIs, Assets; accept data gap as acceptable |

# **22\. Acceptance Criteria — Phase 1**

| Module | Criterion | Test Method |
| :---- | :---- | :---- |
| Incident Management | Agent creates P1 incident; system calculates P1 SLA due; escalation emails received at 75% and 100% of SLA; incident auto-closed 24h after resolution | End-to-end UAT test case IC-01 to IC-10 |
| Problem Management | Problem created from incident; 5-Whys RCA form completed; workaround published to KEDB; workaround shown in incident creation sidebar; problem-to-change RFC link works | UAT test case PRB-01 to PRB-06 |
| Change Management | Normal change goes through: Draft → Technical Review → CAB Scheduled → CAB Approved (email voting) → Authorised → Scheduled (calendar visible) → In Progress → Completed → PIR → Closed | UAT test case CHG-01 to CHG-12 |
| SLA Engine | Create incident at end of working day; SLA due calculated correctly skipping non-working hours and holiday; on-hold pause subtracts correctly | Automated SLA calculation test suite (20 scenarios) |
| Workflow Engine | Admin builds 5-step automation rule without code; rule triggers on incident creation; email sent to manager; record assigned to team | UAT by non-technical ITSM Admin user |
| Reporting | Operations Dashboard loads in \< 3 seconds with 500 test incidents; SLA compliance report accurate within 1% of manual Excel calculation | Load test \+ data accuracy validation |
| Performance | 300 concurrent users browsing portal; average response time \< 2s; zero 500 errors | k6 load test script |
| Security | Penetration test: agent cannot access other team's incidents; customer cannot view internal notes; API returns 403 for unauthorised access | Role-based access test matrix (50 test cases) |

# **23\. Glossary**

| Term | Definition |
| :---- | :---- |
| CAB | Change Advisory Board — group that reviews and approves Normal changes |
| CI | Configuration Item — any IT component tracked in CMDB |
| CMDB | Configuration Management Database — repository of all CIs and their relationships |
| ECAB | Emergency Change Advisory Board — expedited approval group for Emergency changes |
| FCR | First Call Resolution — incident resolved on first contact without escalation or transfer |
| ITIL | Information Technology Infrastructure Library — global ITSM best-practice framework |
| ITIL v4 | Latest ITIL version; introduces Service Value System and 34 management practices |
| KEDB | Known Error Database — catalogue of known problems with documented workarounds |
| MTTR | Mean Time to Resolve — average elapsed time from incident creation to closure |
| NLU | Natural Language Understanding — AI capability to extract intent from natural language |
| OLA | Operational Level Agreement — internal SLA between IT teams (e.g., L1 to L2 handoff) |
| PIR | Post-Implementation Review — structured review after a change or major incident resolution |
| RFC | Request for Change — formal record initiating the change management process |
| RITM | Requested Item — individual line item within a Service Request, linked to one catalog item |
| RCA | Root Cause Analysis — structured investigation into the underlying cause of a problem |
| SLA | Service Level Agreement — contractual targets for response and resolution times |
| ITSM | IT Service Management — set of practices for designing, delivering, and managing IT services |
| CTI | Computer Telephony Integration — screen pop of customer record when phone call arrives |
| Jinja | Templating language used in Frappe Server Scripts and notification templates |
| Socket.io | WebSocket library used for real-time bi-directional communication in live chat |

