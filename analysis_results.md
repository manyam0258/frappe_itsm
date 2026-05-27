# Codebase Insights & Status: frappe_itsm

This document provides a comprehensive overview of the current development state of the **frappe_itsm** application. It details the implemented features, active DocTypes, frontend portals, and guides what should be developed next in Phase 2.

---

## 1. Executive Status Summary

The project is currently at the transition point between **Phase 1 (ITSM Core)** and **Phase 2 (Catalog & CMDB)**.
All core ITIL v4 modules for Incident, SLA, Problem, and Change Management are scaffolded, installed, and populated on your local site `aaa`.

```mermaid
graph TD
    subgraph Phase 1: Core ITSM (Completed)
        A[Foundation & Roles] --> B[Incident Management & Priority Matrix]
        B --> C[SLA Engine & Background Job]
        C --> D[Problem & Change Management]
        D --> E[Vue 3 Agent & Self-Service Portals]
    end
    subgraph Phase 2: Catalog & CMDB (Next)
        E --> F[Service Catalog & RITM]
        E --> G[CMDB & CI Relationships]
        E --> H[Asset Management & ERPNext Sync]
        E --> I[Knowledge Base & KEDB integration]
    end
```

---

## 2. Deep Dive: What Has Been Developed

### 2.1 Foundation & Roles (Sprint 1)
- **Roles Configured**: `ITSM Admin`, `ITSM Manager`, `ITSM Agent`, `ITSM Employee`, and others are set up for role-based permissions.
- **Core DocTypes**:
  - `ITSM Category` & `ITSM Sub Category` (Categorisation)
  - `ITSM Team` & `ITSM Location` (Assignment & Location tracking)
  - `ITSM Tag` (Labelling)

### 2.2 Incident Management (Sprint 2)
- **ITSM Priority Matrix**: Configurable grid mapping **Impact** (Enterprise, Department, Group, Individual) and **Urgency** (Critical, High, Medium, Low) to **Priority** (P1-P5).
- **ITSM Incident**: Fully ITIL-compliant main ticket tracking document with:
  - Naming series: `INC-{YYYY}-{#####}`
  - Auto-Priority logic implemented in Python controller (`itsm_incident.py`) that executes `before_save`.
  - State machine/workflow transitions: `New -> Assigned -> In Progress -> Pending -> Resolved -> Closed`.

### 2.3 SLA Engine (Sprint 3)
- **SLA Policy Configuration**: Uses parent `ITSM SLA Policy` with child tables:
  - `ITSM SLA Condition` (criteria for policy eligibility)
  - `ITSM SLA Target` (response and resolution times)
  - `ITSM SLA Escalation` (escalation paths at 50%, 75%, 100% breach)
- **SLA Evaluation**:
  - Background Python runner (`sla_evaluator.py`) evaluated periodically.
  - Pauses SLAs when incident is in `Pending` state and logs pauses in `ITSM SLA Hold Log`.
  - Links active execution to `ITSM SLA Instance` per ticket.

### 2.4 Problem & Change Management (Sprint 5)
- **Problem Management**:
  - `ITSM Problem` captures root cause and RCA methodologies (like 5-Whys).
  - Python controller (`itsm_problem.py`) contains a hook to automatically create a Draft `ITSM Knowledge Article` when `workaround_published` is toggled.
- **Change Enablement**:
  - `ITSM Change` supports Standard, Normal, Emergency types.
  - Python controller (`itsm_change.py`) implements:
    - **Risk Score Calculation**: Computes 0-100 score from the `ITSM Change Risk Question` table and updates `risk_level` (Very Low to Very High).
    - **Blackout Window Validation**: Checks for planned start/end conflicts against `ITSM Blackout Window` and warns the user on save.
  - Scaffolds for CAB meetings (`ITSM CAB Meeting`, `ITSM CAB Member`, `ITSM CAB Agenda Item`).

### 2.5 Frontend Portals (Sprint 4)
- A Vue 3 SPA is established in `/frontend` using Vite and TailwindCSS:
  - **Agent Portal Layout** (`AgentLayout.vue`) with Sidebar navigation.
    - Dashboard View (`Agent/Dashboard.vue`) displaying placeholder KPIs.
    - Incident List View (`Agent/IncidentList.vue`) displaying open tickets.
  - **Employee Self-Service Portal Layout** (`PortalLayout.vue`).
    - Dashboard / Search landing page (`Portal/Dashboard.vue`).
    - Tickets list view (`Portal/MyTickets.vue`).
- **Client Routing**: Configured in `router.js` with lazy-loaded components and base routes for `/agent` and `/portal`.

---

## 3. Inventory of the 29 DocTypes

Here is the exact state of all 29 `ITSM` prefixed DocTypes currently registered:

| DocType Name | Type | Purpose | Main Fields / Keys |
| :--- | :--- | :--- | :--- |
| **ITSM Category** | Master | Main categorization | `category_name` |
| **ITSM Sub Category** | Master | Sub-level category linked to parent | `sub_category_name`, `parent_category` |
| **ITSM Team** | Master | Support teams | `team_name`, `manager` |
| **ITSM Location** | Master | Organization physical locations | `location_name`, `parent_location` |
| **ITSM Tag** | Master | Tags for incident/change labeling | `tag_name` |
| **ITSM Priority Matrix** | Configuration | Auto-priority mapping | `company`, `impact`, `urgency`, `priority` |
| **ITSM Incident** | Document | Core Incident ticket | `status`, `impact`, `urgency`, `priority`, `assigned_to`, `sla_status` |
| **ITSM Incident CI** | Child Table | Affected CIs linked to Incident | `ci`, `incident` |
| **ITSM Watch List** | Child Table | Subscribers to notifications | `user` |
| **ITSM Resolution Code** | Master | Classification of incident resolution | `code`, `description` |
| **ITSM Working Hours** | Configuration | Work shifts for SLA eligibility | `shift_name`, `start_time`, `end_time` |
| **ITSM Holiday List** | Configuration | Non-working days for SLA calculation | `holiday_list_name` |
| **ITSM Holiday** | Child Table | Indivdual holidays | `holiday_date`, `description` |
| **ITSM SLA Policy** | Configuration | Parent SLA policy definition | `policy_name`, `company`, `working_hours` |
| **ITSM SLA Condition** | Child Table | Filters where SLA policy applies | `field`, `operator`, `value` |
| **ITSM SLA Target** | Child Table | Response/Resolution deadlines | `priority`, `response_time_mins`, `resolution_time_mins` |
| **ITSM SLA Escalation** | Child Table | Notification & action thresholds | `breach_percent`, `action_type`, `recipient_role` |
| **ITSM SLA Instance** | Document | Live SLA tracker per Incident | `incident`, `sla_policy`, `response_due`, `resolution_due`, `status` |
| **ITSM SLA Hold Log** | Document | Records pause durations | `incident`, `sla_instance`, `paused_at`, `resumed_at` |
| **ITSM Problem** | Document | Root Cause Analysis document | `status`, `rca_methodology`, `workaround`, `workaround_published` |
| **ITSM Problem Incident** | Child Table | Incidents linked to a Problem | `incident`, `problem` |
| **ITSM Problem Task** | Child Table | Parallel tasks for investigation | `task_title`, `assigned_to`, `status` |
| **ITSM Change** | Document | Request for Change (RFC) | `change_type`, `risk_level`, `start_datetime`, `end_datetime`, `status` |
| **ITSM Change Task** | Child Table | Tasks for implementation/rollback | `task_title`, `task_type`, `status` |
| **ITSM Change Risk Question** | Child Table | Questionnaire answers for risk scoring | `question`, `answer`, `weight` |
| **ITSM CAB Meeting** | Document | Change Advisory Board scheduling | `meeting_date`, `status` |
| **ITSM CAB Member** | Child Table | Members attending the CAB | `user`, `role` |
| **ITSM CAB Agenda Item** | Child Table | Changes scheduled for review | `change_request`, `status` |
| **ITSM Blackout Window** | Document | Restricted deployment windows | `title`, `start_datetime`, `end_datetime` |

---

## 4. What Needs to Be Developed Next (Phase 2)

As detailed in the roadmap and remaining checklists, we need to transition into **Phase 2: Catalog + CMDB + Asset + KB**. 

### 4.1 Service Catalog
We need to scaffold self-service catalog ordering to transition from generic incidents to structured requests:
* **`ITSM Catalog Item`**: Definition of items available for order (e.g., "Request New Laptop", "Software Install").
* **`ITSM Request Item` (RITM)**: The actual fulfillment ticket containing user variables and multi-stage approvals.
* **Variable Tables**: Child table to capture dynamic inputs (e.g., "RAM Size", "Operating System").
* **Fulfillment Workflows**: Workflows mapping RITM status transitions through approvals and tasks.

### 4.2 Configuration Management Database (CMDB)
* **`ITSM CI`**: Base Configuration Item DocType tracking all assets/software configuration records.
* **CI Class/Hierarchy**: Structuring CIs into types (Hardware, VM, Network, Database).
* **CI Relationships**: Capturing upstream/downstream mappings (e.g., "Database server *runs on* VM server 1").
* **Impact Analysis Graph**: Simple visual representation or tree lookup of dependencies.

### 4.3 Asset Management
* **`ITSM Asset`**: Extends ERPNext Asset or creates a customized hardware/software asset lifecycle tracking tool.
* **Asset Depreciation & Procurement Link**: Ties assets directly to purchase orders and calculates financial depreciation.

### 4.4 Knowledge Base (KB)
* **`ITSM Knowledge Article`**: We must implement this DocType (which was mocked in Sprint 5) to allow publishing workarounds into articles, managing categories, tracking customer feedback/ratings, and enabling keyword search.

---

## 5. Verification Plan (Immediate Next Steps)

Before writing new features for Phase 2, we should execute and verify the Phase 1 test suite to ensure stability.

### 1. Run Playwright E2E Tests
Run the test suite in `apps/frappe_itsm/frappe-itsm-tests` to ensure Incident, Problem, Change, and Portal layouts are fully integrated:
```bash
cd apps/frappe_itsm/frappe-itsm-tests
npm install
npx playwright test
```

### 2. Verify Portals
Build and test the Vue 3 development server:
```bash
cd apps/frappe_itsm/frontend
yarn install
yarn dev
```
Verify that:
1. Agent dashboard and incident list display correctly.
2. Self-service portal lists tickets correctly.

#############################

# Alignment & Gap Analysis Report: `frappe_itsm`

This report provides a detailed comparison between the process flows and flowcharts defined in `frappe_itsm_flowcharts.md` / `frappe_itsm_Process_Flows.md` and the actual implemented codebase. It also outlines the root cause and resolution of the Playwright E2E test failures.

---

## 1. Playwright E2E Test Suite Status

### Root Cause of Failures
The test suite in [portals_ui.spec.js](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe-itsm-tests/tests/portals_ui.spec.js) failed due to two main reasons:
1. **Empty Database / Missing Categories**: The local database was missing the initial category master data (`Hardware`, `Software`, etc.), which caused REST API calls to fail. Because of this, when the UI navigated to the portals, it showed the empty/placeholder states instead of the standard lists, resulting in assertion failures (e.g., missing "Ticket ID" and "Subject" table headers).
2. **Vue Resource Binding Issues**: The frontend components ([IncidentList.vue](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frontend/src/pages/Agent/IncidentList.vue) and [MyTickets.vue](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frontend/src/pages/Portal/MyTickets.vue)) were trying to access `incidents.data` and `tickets.data` directly, whereas the Frappe Vue SDK requires accessing them via `$resources.incidents.data` and `$resources.tickets.data`.

### Resolution Applied
* **Seeding Database**: Added the `seed_data` function in [setup.py](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe_itsm/setup.py) to automatically populate standard `ITSM Category` records (`Hardware`, `Software`, `Network`, `Database`, `Cloud`) and the company `"Mindgraph Technologies Pvt Ltd"`.
* **Playwright Session Authentication & Incident Seeding**: Updated the `beforeEach` block in [portals_ui.spec.js](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe-itsm-tests/tests/portals_ui.spec.js) to authenticate as `Administrator` and seed an incident using `page.request.post` prior to routing checks.
* **Component Resource Fix**: Updated both portals' Vue templates to use `$resources.incidents` and `$resources.tickets` bindings.
* **Result**: All 8 E2E Playwright tests are now passing green.

---

## 2. Process Flow & Flowchart Alignment Review

The table below maps the 10 ITSM modules outlined in [frappe_itsm_flowcharts.md](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe_itsm_flowcharts.md) to their actual implementation status in the codebase.

| # | Module | Status in Codebase | Alignment / Implemented Features | Missing Elements / Gaps |
|---|--------|--------------------|----------------------------------|-------------------------|
| **1** | **Incident Management** | **Partially Aligned** | - Priority calculation based on Matrix matches PRD/Flowchart.<br>- Workflow states defined.<br>- Core child tables (`ITSM Incident CI`, `ITSM Watch List`) exist. | - **No Auto-Duplicate Scanning**: Missing code to scan open incidents for same category + caller.<br>- **No Round-Robin Routing**: Auto-assignment engine is missing.<br>- **Major Incident bridge**: Bridge meeting integrations and L2 alerts not implemented. |
| **2** | **Problem Management** | **Partially Aligned** | - DocTypes (`ITSM Problem`, `ITSM Problem Incident`, `ITSM Problem Task`) exist.<br>- Auto-drafts Knowledge Article (if DocType exists) when workaround is published. | - **No Proactive Auto-Suggestion**: System check for 3+ incidents in 2 hours is missing.<br>- **No PIR Blocking**: Python controller does not enforce that problem cannot close while PIR tasks are open. |
| **3** | **Change Management** | **Partially Aligned** | - DocTypes for Change, Blackout Windows, CAB, Tasks, Risk Questions exist.<br>- Blackout window overlap logic is checked in `before_save` SQL query.<br>- Risk score (0-100) auto-calculated in Python controller. | - **CAB Email Voting**: Signed URL token voting without login is missing.<br>- **Change Calendar conflicts**: Checking same CI in same window is not coded.<br>- **ECAB Rules**: No automated 4h approval timeout or enforcement. |
| **4** | **SLA Engine** | **Scaffold Only** | - DocTypes exist for Policies, Targets, Instances, and Hold Logs.<br>- Hold/resume logs pause-time. | - **sla_evaluator.py** is a basic placeholder; doesn't integrate working hours / holidays.<br>- No 50%, 75%, or 125% escalations implemented. |
| **5** | **CMDB** | **Completely Missing** | - None (only a dummy child table on Incident exists). | - No `ITSM CI` or `ITSM CI Relationship` DocTypes exist.<br>- No relationship graph traversal (BFS) or stale alerts. |
| **6** | **Service Catalog** | **Completely Missing** | - None. | - No `ITSM Catalog Item`, `REQ`, `RITM` or dynamic variable forms. |
| **7** | **Knowledge Base** | **Completely Missing** | - Problem controller guards checking if `ITSM Knowledge Article` exists before attempting creation. | - No `ITSM Knowledge Article` DocType exists. |
| **8** | **Reporting & Dashboards** | **Completely Missing** | - Frontend Agent dashboard contains simple mockup charts. | - No automated report schedules, KPI thresholds, or email alerts. |
| **9** | **AI / Virtual Agent** | **Completely Missing** | - None. | - No LLM/GPT classifier integration or deflection bot. |
| **10** | **Asset Management** | **Completely Missing** | - None. | - No hardware/software assets or ERPNext integration. |

---

## 3. Recommended Actions for Phase 2

1. **CMDB Foundations**: Introduce the `ITSM CI` and `ITSM CI Relationship` DocTypes, and write Python hooks to trace dependencies.
2. **Service Catalog & RITM**: Create request fulfillment DocTypes to allow user portal requests.
3. **Knowledge Base Implementation**: Build the `ITSM Knowledge Article` DocType to enable published workarounds.
4. **SLA Evaluator Implementation**: Replace placeholders in `sla_evaluator.py` with actual business-hour math using `ITSM Working Hours` and `ITSM Holiday List`.


25/05/2026
Ran command: `cd apps/frappe_itsm/`
Ran command: `git status`

I will start by checking the files inside `/home/demo/frappe-bench-explore/apps/frappe_itsm` to see the setup, implementation plan, task list, and current Playwright setup. This will help understand the current development status, issues, and next steps.

Listed directory frappe_itsm

I will read `task.md` to check the current task progress.

Viewed task.md:1-81

I will inspect `implementation_plan.md` to get context on the design goals and architectural decisions made so far.

Viewed implementation_plan.md:1-125

I will read `walkthrough.md` to see the details of the latest implementation.

Viewed walkthrough.md:1-68

I will read `PLAYWRIGHT_SETUP.md` to see what tests have been defined, how they are run, and what portals and endpoints they test.

Viewed PLAYWRIGHT_SETUP.md:1-123

I will list the contents of the `frappe-itsm-tests` directory to see what test files are present and how they are structured.

Listed directory frappe-itsm-tests

I will list the files inside the `tests` subdirectory under `frappe-itsm-tests`.

Listed directory tests

I will view the `package.json` file in `frappe-itsm-tests` to see the scripts and packages configured.

Viewed package.json:1-17

I will view the `playwright.config.js` file in the tests directory.

Viewed playwright.config.js:1-19

I will inspect one of the test files, `incident_lifecycle.spec.js`, to see the test implementation.

Viewed incident_lifecycle.spec.js:1-73

I will view `change_lifecycle.spec.js` to see how the Change Management E2E/API tests are structured.

Viewed change_lifecycle.spec.js:1-75

I will view the `portals_ui.spec.js` test file.

Viewed portals_ui.spec.js:1-84

I will view the `problem_lifecycle.spec.js` test file to see how problem lifecycle test logic is implemented.

Viewed problem_lifecycle.spec.js:1-54

I will view `sprint5.spec.js` to see what tests it runs.

Viewed sprint5.spec.js:1-54

I will view the `output.txt` file in `frappe-itsm-tests` to see the results of the previous test execution.

Viewed output.txt:1-49

I will search for occurrences of `8000` in the test files to see if a wrong port or hostname is hardcoded.

Searched for "8000"

I will inspect the `frontend` directory of the app to see how the frontend dev server is configured and what backend URL it tries to proxy to.

Listed directory frontend

I will check `vite.config.js` to see the Vite dev server proxy configuration.

Viewed vite.config.js:1-28

I will read `common_site_config.json` to see the port number used by the web server.

Viewed common_site_config.json:1-19

I will check the git diff in `apps/frappe_itsm` to see what changes have been made to `PLAYWRIGHT_SETUP.md`, `task.md`, and the playwright reports.

Ran command: `git diff`

I will run `git diff PLAYWRIGHT_SETUP.md` to see what changes were made in the Playwright setup instructions.

Ran command: `git diff PLAYWRIGHT_SETUP.md`

I will check all files (including hidden ones like `.env`) inside the `frappe-itsm-tests` directory to see if there are environment configurations.

Ran command: `ls -la`

I will check if the Frappe/bench development server is currently running, and on what ports it is listening.

Ran command: `ps aux | grep -i python`

I will run the Playwright test suite to see the current test failures and output.

Ran command: `npx playwright test`

I will read the `analysis_results.md` file to see the results of any code analysis or checks performed on the project.

Viewed analysis_results.md:1-214

I will check the status of the Playwright E2E tests background job.

Used tool: manage_task

I will inspect the main application directory of `frappe_itsm` to check what modules and code files are present.

Listed directory frappe_itsm

I will check the status of the Playwright E2E tests task to see if they completed.

Used tool: manage_task

I will schedule a brief 10-second wait to allow the tests to finish execution.

Used tool: schedule

I will search the Product Requirements Document (PRD) for any specific testing requirements or guidelines.

Searched for "playwright"

I will search the PRD for mentions of testing or E2E.

Searched for "testing"

Based on a thorough review of the codebase, documentation (`PLAYWRIGHT_SETUP.md`, `task.md`, `implementation_plan.md`, `walkthrough.md`, `analysis_results.md`), and running the Playwright test suite, here is the comprehensive status of development, issues identified, next steps, and a detailed strategy for Playwright E2E testing.

---

### 1. Current Development Status

The project has completed **Phase 1 (ITSM Core)** modules and is transitioning into **Phase 2 (Catalog & CMDB)**. 

*   **DocTypes Scaffolded**: 29 `ITSM`-prefixed DocTypes have been registered and scaffolded.
*   **Backend Logic Implemented**:
    *   **Priority Matrix**: Impact and Urgency auto-calculate the incident's `Priority` (`P1–P5`) on save.
    *   **Workflow / State Machine**: Incidents transition through `New ➔ Assigned ➔ In Progress ➔ Pending ➔ Resolved ➔ Closed`.
    *   **Problem & Change**: Includes dynamic **Risk Score Calculation** (0-100), **Blackout Window Validation** (dates overlap checks), and auto-generation of Knowledge Database drafts.
*   **Vue 3 SPA Frontend**:
    *   Set up using `frappe-ui-starter` and Vite.
    *   **Agent Portal**: Sidebar layout, list view of incidents, and basic KPI dashboard.
    *   **Employee Self-Service Portal**: Ticket submission form, "My Tickets" list view, and landing page.

---

### 2. Issues & Gaps Found

#### A. Playwright Test Suite Port & URL Configuration
*   **Hardcoded Base URLs and Credentials**: While the test suite runs and passes (8/8 tests passed successfully in 24 seconds), multiple test spec files (e.g., `incident_lifecycle.spec.js`, `change_lifecycle.spec.js`, `problem_lifecycle.spec.js`) hardcode the `baseURL` to `http://192.168.252.6:8007` and credentials to `pwd: 'admin'`. In contrast, `PLAYWRIGHT_SETUP.md` refers to `pwd: 'demo@123'` and `port 8002`/`8007`.
*   **Resolution Strategy**: These should be dynamically loaded via a `.env` file using a library like `dotenv` so that local development, CI/CD, and staging run seamlessly without manual file editing.

#### B. Core Module Functional Gaps
*   **SLA Engine**: The background job `sla_evaluator.py` is currently a placeholder. It needs to calculate business-hours math (using `ITSM Working Hours` and `ITSM Holiday List`) and trigger breach escalations (e.g., at 50%, 75%, 100% of the target).
*   **Incident Management**: Lacks auto-duplicate ticket scanning (checking same caller + category) and round-robin auto-assignment to support teams.
*   **Problem Management**: Lacks proactive alert suggestions (e.g., prompting problem creation when 3+ similar incidents happen within 2 hours).
*   **Change Management**: Lacks CAB email-based voting with signed tokens and conflict checking for changes scheduled on the *same Configuration Item (CI)*.

#### C. Missing Phase 2 DocTypes
*   **CMDB & CI Relationships**: Currently, there are no `ITSM CI` or `ITSM CI Relationship` DocTypes.
*   **Service Catalog**: No `ITSM Catalog Item` or Request Item (`RITM`) DocTypes exist yet.
*   **Knowledge Base**: No actual `ITSM Knowledge Article` DocType exists yet (mocked inside Problem workflow).

---

### 3. Playwright E2E Testing Strategy

The E2E testing framework is set up in the `frappe-itsm-tests` folder, running Playwright on chromium. It tests the Vue SPA on port `8080`, which proxies requests to the Frappe backend on port `8007`.

To ensure testing remains robust during Phase 2 development, we should adopt the following patterns:

#### A. Centralized Environment Config
Create a robust configuration in `playwright.config.js` to read from a local `.env` file:
```javascript
// playwright.config.js
require('dotenv').config();

module.exports = defineConfig({
  use: {
    baseURL: process.env.FRAPPE_BASE_URL || 'http://localhost:8007',
  }
});
```

#### B. API Seeding & Cleanup (Hybrid Testing)
Avoid setting up complex test prerequisites using the UI.
*   **Seeding**: Use the `playwright.request` context (API) to authenticate and seed necessary DocTypes (e.g. creating categories, SLA policies, and active incidents) before running UI tests.
*   **Cleanup**: Maintain robust teardown in `afterAll()` hooks using API calls to delete seeded data (matching the `PW_TEST_` naming series prefix) to keep the test database clean.

#### C. Page Object Model (POM) for Vue Portals
As we develop more UI components in Phase 2, separate page selectors from tests.
*   Define page structures (e.g., `EmployeePortalPage`, `AgentDashboardPage`) to keep tests cleaner.
    ```javascript
    // Example Page Object: EmployeePortalPage.js
    class EmployeePortalPage {
      constructor(page) {
        this.page = page;
        this.ticketForm = page.locator('#ticket-form');
        this.subjectInput = page.locator('[data-fieldname="title"] input');
      }
      async goto() {
        await this.page.goto('/frontend/portal/dashboard');
      }
      async submitTicket(subject) {
        await this.subjectInput.fill(subject);
        await this.page.click('button:has-text("Submit")');
      }
    }
    ```

---

### 4. Next Steps in Development

1.  **SLA Engine Business Logic**: Upgrade `sla_evaluator.py` to support true calendar duration calculations, pausing on pending states, and triggers for escalations.
2.  **Scaffold CMDB**: Create `ITSM CI` and `ITSM CI Relationship` DocTypes and write Python utility functions for dependency path traversal.
3.  **Knowledge Base**: Build the actual `ITSM Knowledge Article` DocType and integrate it with the Problem workaround publishing flow.
4.  **Service Catalog**: Create `ITSM Catalog Item`, `ITSM Request Item` (RITM), and custom variable child tables.
5.  **Refactor Test Configurations**: Transition test files from hardcoded URLs/credentials to dotenv environment variables.