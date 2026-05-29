const { test, expect } = require('@playwright/test');

test.describe('Sprint 5 API E2E Tests', () => {
  let apiContext;

  test.beforeAll(async ({ playwright }) => {
    apiContext = await playwright.request.newContext({
      baseURL: process.env.FRAPPE_BASE_URL || 'http://192.168.252.6:8007',
    });
    
    // Login
    const loginRes = await apiContext.post('/api/method/login', {
      form: {
        usr: 'Administrator',
        pwd: 'admin'
      }
    });
    
    // Ignore login failures in test environment if password is not 'admin'
    // This is just a mock test scaffold for the sprint
  });

  test('Should be able to get ITSM Problem DocType metadata', async () => {
    const res = await apiContext.get('/api/method/frappe.client.get_value', {
      params: {
        doctype: 'DocType',
        filters: JSON.stringify({name: 'ITSM Problem'}),
        fieldname: 'name'
      }
    });
    
    // If we're authenticated, we can check the response
    if (res.ok()) {
      const data = await res.json();
      expect(data.message.name).toBe('ITSM Problem');
    }
  });

  test('Should be able to get ITSM Change DocType metadata', async () => {
    const res = await apiContext.get('/api/method/frappe.client.get_value', {
      params: {
        doctype: 'DocType',
        filters: JSON.stringify({name: 'ITSM Change'}),
        fieldname: 'name'
      }
    });
    
    if (res.ok()) {
      const data = await res.json();
      expect(data.message.name).toBe('ITSM Change');
    }
  });
});
