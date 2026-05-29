# Implementation Plan: Phase 1 Gaps & Phase 2 Transitions

This plan details the design, changes, and verification steps for closing the remaining Phase 1 functional gaps and initiating the Phase 2 structural transitions.

## User Review Required
> [!IMPORTANT]
> - **SLA Engine Calculations:** Business hour calculations will step minute-by-minute (or day-by-day) using the specified timezone inside the `ITSM Working Hours` definition.
> - **CAB Email Voting:** HMAC-SHA256 signature tokens will be used to authorize CAB members' votes without authentication. The system key/password will secure these tokens.
> - **CMDB Traversal:** BFS logic will trace upstream dependencies to detect potential change conflicts.

---

## Proposed Changes

### 1. SLA Engine Calculations

#### [MODIFY] [create_sla_doctypes.py](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe_itsm/create_sla_doctypes.py)
- Update `ITSM SLA Instance` schema to include:
  - `triggered_escalations` (Small Text) to store comma-separated escalation thresholds that have already fired.

#### [MODIFY] [sla_evaluator.py](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe_itsm/frappe_itsm/sla_evaluator.py)
- Replace basic placeholder `calculate_sla_due` with a calendar-aware business hour calculator:
  - Fetch working schedule (`monday_start`, `monday_end`, etc.) and the timezone from the linked `ITSM Working Hours`.
  - Handle exceptions for public holidays configured in `ITSM Holiday List` and `ITSM Holiday`.
  - Account for timezone conversions when processing dates in UTC.
- Upgrade background job `evaluate_slas()` to:
  - Monitor elapsed percentage for open SLA instances.
  - Set status to `"At Risk"` if elapsed time exceeds 75% of target.
  - Trigger configured `ITSM SLA Escalation` rules (email notification, priority upgrade, reassignment).
  - Record fired escalations in the `triggered_escalations` field of the SLA Instance to prevent duplicate notifications.

---

### 2. Knowledge Base Integration

#### [NEW] `ITSM Knowledge Article` DocType definition
- Create a setup helper to register the `ITSM Knowledge Article` DocType:
  - Fields: `title` (Data), `article_type` (Select: Info, Workaround, Known Error), `category` (Link to ITSM Category), `content` (HTML/Text Editor), `source_problem` (Link to ITSM Problem), `status` (Select: Draft, Published, Archived), `views` (Int).

#### [MODIFY] [itsm_problem.py](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe_itsm/frappe_itsm/doctype/itsm_problem/itsm_problem.py)
- Remove fallback logic in `publish_to_kedb` and create a real draft article of `ITSM Knowledge Article` when `workaround_published` is checked.

---

### 3. Duplicate Scanning

#### [MODIFY] [itsm_incident.py](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe_itsm/frappe_itsm/doctype/itsm_incident/itsm_incident.py)
- Implement `check_for_duplicates()` inside the `before_save` hook:
  - Query for other open `ITSM Incident` records with the same `caller` and `category`.
  - If a duplicate is found:
    - Automatically link the new ticket's `parent_incident` to the existing open ticket.
    - Raise a user-facing warning using `frappe.msgprint` advising that a duplicate was detected.

---

### 4. CAB Email Voting

#### [MODIFY] [itsm_cab_meeting.py](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe_itsm/frappe_itsm/doctype/itsm_cab_meeting/itsm_cab_meeting.py)
- Implement HMAC-SHA256 URL signature generation and verification methods:
  - `generate_signed_vote_url(meeting_name, member_email, vote)`
  - `verify_vote_token(meeting_name, member_email, vote, token)`
- Implement whitelisted method `record_cab_vote(meeting, user, vote, token)` (allow guest execution):
  - Mark member attendance as `"Attended"` and their vote as `"Approve"` or `"Reject"`.
  - Evaluate total votes against the quorum target (`quorum_required`).
  - Auto-transition linked agenda change requests to `"CAB Approved"` or `"Draft"` (rejected) based on vote majority.
- Implement workflow trigger to automatically email voting links to CAB members when a change is moved to `"CAB Scheduled"`.

---

### 5. CMDB Structure & BFS Traversal

#### [NEW] `ITSM CI` and `ITSM CI Relationship` DocTypes
- Create a script to programmatically register CMDB DocTypes:
  - `ITSM CI`: Fields for `ci_name` (Data), `ci_type` (Select: Hardware, VM, Network, Database), `status` (Select: Active, Inactive, Stale), `ip_address` (Data).
  - `ITSM CI Relationship`: Fields for `parent_ci` (Link to ITSM CI), `child_ci` (Link to ITSM CI), `relationship_type` (Select: Runs On, Depends On, Connects To).

#### [NEW] Dependency Traversal Module
- Implement BFS path search to return upstream dependencies:
  - Trace child-to-parent relations recursively to detect potential scheduling conflicts if multiple changes affect the same dependency path.

---

### 6. Service Catalog

#### [NEW] `ITSM Catalog Item` and `ITSM Request Item` (RITM) DocTypes
- Create catalog DocTypes:
  - `ITSM Catalog Item`: Fields for `item_name` (Data), `description` (Text Editor), `category` (Link to ITSM Category), `cost` (Currency).
  - `ITSM Request Item`: Fields for `catalog_item` (Link to ITSM Catalog Item), `requester` (Link to User), `status` (Select: Pending Approval, Approved, Fulfilling, Closed).

---

### 7. Environment Configurations & Test Refactoring

#### [NEW] [.env](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe-itsm-tests/.env)
- Create a configuration file containing:
  - `FRAPPE_BASE_URL=http://192.168.252.6:8007`
  - `FRAPPE_ADMIN_USER=Administrator`
  - `FRAPPE_ADMIN_PASSWORD=admin`

#### [MODIFY] [playwright.config.js](file:///home/demo/frappe-bench-explore/apps/frappe_itsm/frappe-itsm-tests/playwright.config.js)
- Configure Playwright to load `.env` variables via `dotenv`.

#### [MODIFY] All Spec files
- Update spec files to read URLs and login details dynamically from environment variables.

---

## Verification Plan

### Automated Tests
- Extend the Playwright test suite to add E2E specs verifying:
  - SLA Instance Priority and Business hour deadlines.
  - Incident duplicate warnings and linking.
  - Guest vote recording via signed URLs on CAB Meetings.
- Run all tests to guarantee passing status:
  `npx playwright test`

### Manual Verification
- Verify generated draft articles in KEDB.
- Validate that blackout window warnings and CI relationship mapping function correctly on the desk view.
