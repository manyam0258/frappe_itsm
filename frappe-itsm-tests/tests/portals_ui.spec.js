const { test, expect } = require('@playwright/test');

test.describe('Vue 3 Portals UI E2E', () => {

  test('Employee Self-Service Portal Routing & Rendering', async ({ page }) => {
    // 1. Navigate to root, which redirects to /agent/dashboard
    await page.goto('http://localhost:8080/');
    await page.waitForTimeout(1000);
    
    // 2. Instead of hard goto, evaluate router push
    await page.evaluate(() => {
      // Access the vue router instance (usually exposed or can trigger click)
      // Since we don't have it explicitly mapped, we can just change window location hash if it was hash mode.
      // But we are in HTML5 history mode.
      // Easiest is to click a link if we were on the portal, but we are on Agent Dashboard.
      // Let's just create a temporary link and click it to use HTML5 history!
      const a = document.createElement('a');
      a.href = '/frontend/portal/dashboard';
      document.body.appendChild(a);
      a.click();
    });
    
    await page.waitForTimeout(1000);
    await expect(page.locator('h1').first()).toContainText('IT Helpdesk');
    
    // 3. Click the "My Tickets" link in the navbar
    await page.getByRole('link', { name: 'My Tickets' }).click();
    await page.waitForTimeout(1000);
    
    await expect(page.locator('h1').first()).toContainText('My Tickets');
    
    // 4. Verify table headers
    await expect(page.getByText('Ticket ID')).toBeVisible();
    await expect(page.getByText('Subject')).toBeVisible();
  });

  test('Agent Portal Routing & Incident List', async ({ page }) => {
    await page.goto('http://localhost:8080/');
    await page.waitForTimeout(1000);
    
    await expect(page.getByText('Agent Dashboard')).toBeVisible();
    await expect(page.getByText('Open Incidents')).toBeVisible();
    
    // Click the "Incidents" link in the sidebar
    await page.getByRole('link', { name: 'Incidents' }).click();
    await page.waitForTimeout(1000);
    
    // Verify table rendering
    await expect(page.locator('h1').first()).toContainText('Incidents');
  });
});
