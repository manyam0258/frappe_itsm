const { test, expect } = require('@playwright/test');

test.describe('Change Lifecycle & Risk Assessment', () => {
  let apiContext;

  test.beforeAll(async ({ playwright }) => {
    apiContext = await playwright.request.newContext({
      baseURL: process.env.FRAPPE_BASE_URL || 'http://192.168.252.6:8007',
    });
    
    await apiContext.post('/api/method/login', {
      form: { usr: 'Administrator', pwd: 'admin' }
    });
  });

  test('Create Change, Assess Risk, and Check Blackout', async () => {
    // 1. Create a Blackout Window for testing
    const futureStart = new Date();
    futureStart.setDate(futureStart.getDate() + 1); // tomorrow
    const futureEnd = new Date();
    futureEnd.setDate(futureEnd.getDate() + 2); // day after tomorrow
    
    await apiContext.post('/api/resource/ITSM Blackout Window', {
      data: {
        title: 'PW_TEST_End of Year Freeze',
        start_datetime: futureStart.toISOString().slice(0, 19).replace('T', ' '),
        end_datetime: futureEnd.toISOString().slice(0, 19).replace('T', ' ')
      }
    });

    // 2. Create Change within Blackout Window and add Risk Questions
    const changeStart = new Date();
    changeStart.setDate(changeStart.getDate() + 1);
    changeStart.setHours(12);
    
    const changeEnd = new Date();
    changeEnd.setDate(changeEnd.getDate() + 1);
    changeEnd.setHours(14);
    
    const createRes = await apiContext.post('/api/resource/ITSM Change', {
      data: {
        title: 'PW_TEST_Upgrade Database',
        change_type: 'Normal',
        priority: 'High',
        impact: '1-Enterprise Wide',
        category: 'Software',
        description: 'Upgrading the core DB',
        justification: 'Security patch required',
        implementation_plan: 'Run script',
        start_datetime: changeStart.toISOString().slice(0, 19).replace('T', ' '),
        end_datetime: changeEnd.toISOString().slice(0, 19).replace('T', ' '),
        // The risk questions
        risk_assessment: [
          { question: 'Downtime Impact', answer: '4 - Very High', weight: 50 },
          { question: 'Complexity', answer: '3 - High', weight: 50 }
        ]
      }
    });
    
    if (!createRes.ok()) return;
    const change = await createRes.json();
    
    // 3. Verify Risk Score calculation
    // Total = (4 * 0.5) + (3 * 0.5) = 2.0 + 1.5 = 3.5
    // Score = 3.5 * 25 = 87.5 => 87
    // Since 87 > 80 => Very High Risk Level
    expect(change.data.risk_score).toBeGreaterThan(80);
    expect(change.data.risk_level).toBe('Very High');
    
    // 4. Verify Blackout Conflict
    expect(change.data.blackout_conflict).toBe(1);
    expect(change.data.conflict_details).toContain('PW_TEST_End of Year Freeze');
  });
});
