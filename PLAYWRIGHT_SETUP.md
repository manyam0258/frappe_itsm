# Playwright E2E Testing — Quick Start

## 1. Install

```bash
cd frappe-itsm-tests
npm install
npx playwright install chromium      # installs the browser binary
```

## 2. Configure your site URL

Create a `.env` file (never commit this):

```bash
FRAPPE_BASE_URL=http://192.168.252.6:8007
FRAPPE_ADMIN_USER=Administrator
FRAPPE_ADMIN_PASS=demo@123
```

> If your bench site responds on a different port (e.g. 8001), change `FRAPPE_BASE_URL`.
> If you have an Nginx proxy and the site is at `http://aaa`, use that.

## 3. One thing to verify before running

The tests call the SLA evaluator via Frappe's whitelisted API:

```
POST /api/method/frappe_itsm.frappe_itsm.sla_evaluator.evaluate_slas
```

Make sure this method is in your `whitelist` decorator:

```python
# frappe_itsm/frappe_itsm/sla_evaluator.py

@frappe.whitelist()
def evaluate_slas():
    # ... your existing code
```

If it isn't whitelisted, test **3.11** will fail. Either whitelist it or skip test 3.11
by adding `.skip` on that test temporarily.

## 4. Run tests

```bash
# Full suite
npm test

# Per sprint
npm run test:sprint1
npm run test:sprint2
npm run test:sprint3

# Watch mode with live browser (great during development)
npm run test:ui

# See HTML report
npm run test:report
```

## 5. Using with Frappe Assistant Core (MCP in IDE)

Your Frappe AC MCP at `https://192.168.252.6:8002` exposes direct Frappe API access.
You can trigger test runs from the IDE using the MCP via:

```
POST /api/method/frappe_assistant_core.api.fac_endpoint.handle_mcp
{
  "tool": "execute_script",
  "args": {
    "script": "import subprocess; subprocess.run(['npx', 'playwright', 'test', '--project', 'sprint2-incident'], cwd='/path/to/frappe-itsm-tests')"
  }
}
```

Alternatively, configure a **Run Configuration** in your IDE that executes:

```
npx playwright test --project sprint2-incident --reporter=list
```

pointing at your `frappe-itsm-tests/` directory.

## 6. What to adjust for your exact Frappe version

Frappe v15 uses these selectors — confirm they match your actual DOM:

| What | Expected selector |
|------|-------------------|
| Login email | `#login_email` |
| Login password | `#login_password` |
| Login button | `.btn-login` |
| Field wrapper | `[data-fieldname="{name}"]` |
| Input inside field | `.input-with-feedback` |
| Save (keyboard) | `Ctrl+S` |
| Workflow button | `.workflow-action-btn:has-text("...")` |
| Status indicator | `.indicator.green` |

If any selector doesn't match, update `tests/helpers/frappe-form.ts`. All selectors
are centralised there — one change fixes all tests.

## 7. Test record cleanup

Every spec file cleans up its own `PW_TEST_*` records in `afterAll()`.
If a test run is interrupted, run this to clean up manually:

```bash
# Using Frappe shell
bench --site aaa console

# Inside console:
import frappe
for dt in ["ITSM Incident", "ITSM Category", "ITSM Team", "ITSM Location", "ITSM Tag",
           "ITSM SLA Policy", "ITSM Working Hours", "ITSM Holiday List"]:
    names = frappe.get_list(dt, filters={"name": ["like", "PW_TEST_%"]}, pluck="name")
    for n in names:
        frappe.delete_doc(dt, n, ignore_permissions=True)
    print(f"Cleaned {len(names)} records from {dt}")
frappe.db.commit()
```
