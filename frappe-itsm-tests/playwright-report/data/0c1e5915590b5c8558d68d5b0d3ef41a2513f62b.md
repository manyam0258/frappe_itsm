# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: portals_ui.spec.js >> Vue 3 Portals UI E2E >> Agent Portal Routing & Incident List
- Location: tests/portals_ui.spec.js:37:3

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: locator('h1').first()
Expected substring: "Incidents"
Received string:    "Frappe ITSM"
Timeout: 5000ms

Call log:
  - Expect "toContainText" with timeout 5000ms
  - waiting for locator('h1').first()
    14 × locator resolved to <h1 class="text-xl font-bold text-gray-800">Frappe ITSM</h1>
       - unexpected value "Frappe ITSM"

```

```yaml
- heading "Frappe ITSM" [level=1]
```

# Test source

```ts
  1  | const { test, expect } = require('@playwright/test');
  2  | 
  3  | test.describe('Vue 3 Portals UI E2E', () => {
  4  | 
  5  |   test('Employee Self-Service Portal Routing & Rendering', async ({ page }) => {
  6  |     // 1. Navigate to root, which redirects to /agent/dashboard
  7  |     await page.goto('http://localhost:8080/');
  8  |     await page.waitForTimeout(1000);
  9  |     
  10 |     // 2. Instead of hard goto, evaluate router push
  11 |     await page.evaluate(() => {
  12 |       // Access the vue router instance (usually exposed or can trigger click)
  13 |       // Since we don't have it explicitly mapped, we can just change window location hash if it was hash mode.
  14 |       // But we are in HTML5 history mode.
  15 |       // Easiest is to click a link if we were on the portal, but we are on Agent Dashboard.
  16 |       // Let's just create a temporary link and click it to use HTML5 history!
  17 |       const a = document.createElement('a');
  18 |       a.href = '/frontend/portal/dashboard';
  19 |       document.body.appendChild(a);
  20 |       a.click();
  21 |     });
  22 |     
  23 |     await page.waitForTimeout(1000);
  24 |     await expect(page.locator('h1').first()).toContainText('IT Helpdesk');
  25 |     
  26 |     // 3. Click the "My Tickets" link in the navbar
  27 |     await page.getByRole('link', { name: 'My Tickets' }).click();
  28 |     await page.waitForTimeout(1000);
  29 |     
  30 |     await expect(page.locator('h1').first()).toContainText('My Tickets');
  31 |     
  32 |     // 4. Verify table headers
  33 |     await expect(page.getByText('Ticket ID')).toBeVisible();
  34 |     await expect(page.getByText('Subject')).toBeVisible();
  35 |   });
  36 | 
  37 |   test('Agent Portal Routing & Incident List', async ({ page }) => {
  38 |     await page.goto('http://localhost:8080/');
  39 |     await page.waitForTimeout(1000);
  40 |     
  41 |     await expect(page.getByText('Agent Dashboard')).toBeVisible();
  42 |     await expect(page.getByText('Open Incidents')).toBeVisible();
  43 |     
  44 |     // Click the "Incidents" link in the sidebar
  45 |     await page.getByRole('link', { name: 'Incidents' }).click();
  46 |     await page.waitForTimeout(1000);
  47 |     
  48 |     // Verify table rendering
> 49 |     await expect(page.locator('h1').first()).toContainText('Incidents');
     |                                              ^ Error: expect(locator).toContainText(expected) failed
  50 |   });
  51 | });
  52 | 
```