const { test, expect } = require('@playwright/test');

test.describe('Incident to Problem to Change E2E Lifecycle', () => {
  let apiContext;

  test.beforeAll(async ({ playwright }) => {
    apiContext = await playwright.request.newContext({
      baseURL: 'http://192.168.252.6:8007',
    });
    
    // Login as Admin
    const loginRes = await apiContext.post('/api/method/login', {
      form: { usr: 'Administrator', pwd: 'admin' }
    });
    expect(loginRes.ok()).toBeTruthy();
  });

  test('Should handle complete Incident -> Problem -> Change lifecycle flow', async () => {
    // 1. Create a new ITSM Incident
    const incidentRes = await apiContext.post('/api/resource/ITSM Incident', {
      data: {
        title: 'PW_TEST_Integration Incident',
        category: 'Software',
        impact: '3-Group Wide',
        urgency: '2-High',
        description: 'Core application performance is degrading.',
        company: 'Mindgraph Technologies Pvt Ltd',
        caller: 'Administrator',
        raised_by: 'Administrator'
      }
    });
    
    expect(incidentRes.ok()).toBeTruthy();
    const incident = await incidentRes.json();
    const incidentName = incident.data.name;
    expect(incidentName).toBeDefined();

    // 2. Create ITSM Problem linked to this Incident
    const problemRes = await apiContext.post('/api/resource/ITSM Problem', {
      data: {
        title: `Problem caused by: PW_TEST_Integration Incident`,
        category: 'Software',
        description: 'Investigation into core application performance degrading.',
        status: 'New',
        priority: 'P2-High',
        linked_incidents: [
          { incident: incidentName }
        ]
      }
    });

    expect(problemRes.ok()).toBeTruthy();
    const problem = await problemRes.json();
    const problemName = problem.data.name;
    expect(problemName).toBeDefined();

    // Step through Problem workflow: New -> Assess -> Root Cause Analysis
    const problemAssessRes = await apiContext.put(`/api/resource/ITSM Problem/${problemName}`, {
      data: { status: 'Assess' }
    });
    expect(problemAssessRes.ok()).toBeTruthy();

    const problemRcaRes = await apiContext.put(`/api/resource/ITSM Problem/${problemName}`, {
      data: { status: 'Root Cause Analysis' }
    });
    expect(problemRcaRes.ok()).toBeTruthy();

    // 3. Create ITSM Change linked to this Problem
    const changeRes = await apiContext.post('/api/resource/ITSM Change', {
      data: {
        title: `Change Request for Problem: ${problemName}`,
        category: 'Software',
        description: 'Apply performance index patch to database.',
        change_type: 'Normal',
        priority: 'High',
        impact: '3-Group Wide',
        risk_level: 'Medium',
        justification: `Fixing root cause for problem ${problemName}`,
        implementation_plan: 'Deploy permanent fix.',
        change_initiator: 'Administrator',
        change_owner: 'Administrator',
        assigned_team: 'Software Team',
        linked_problem: problemName,
        start_datetime: '2026-06-01 12:00:00',
        end_datetime: '2026-06-01 14:00:00'
      }
    });

    expect(changeRes.ok()).toBeTruthy();
    const change = await changeRes.json();
    const changeName = change.data.name;
    expect(changeName).toBeDefined();

    // Step through Change workflow: New -> Draft -> Pending Review -> CAB Scheduled -> CAB Approved -> Authorised -> Scheduled -> In Progress
    const changeStates = ['Draft', 'Pending Review', 'CAB Scheduled', 'CAB Approved', 'Authorised', 'Scheduled', 'In Progress'];
    for (const state of changeStates) {
      const res = await apiContext.put(`/api/resource/ITSM Change/${changeName}`, {
        data: { status: state }
      });
      expect(res.ok()).toBeTruthy();
    }

    // 4. Update the Problem to link back to the Change and transition to 'Fix in Progress'
    const updateProblemRes = await apiContext.put(`/api/resource/ITSM Problem/${problemName}`, {
      data: {
        linked_change: changeName,
        status: 'Fix in Progress'
      }
    });
    expect(updateProblemRes.ok()).toBeTruthy();

    // 5. Publish workaround on the Problem to check KB Article draft creation
    const updateProblemWorkaroundRes = await apiContext.put(`/api/resource/ITSM Problem/${problemName}`, {
      data: {
        workaround: 'Apply DB index patch.',
        workaround_published: 1
      }
    });
    expect(updateProblemWorkaroundRes.ok()).toBeTruthy();

    // 6. Complete the Change
    const closeChangeRes = await apiContext.put(`/api/resource/ITSM Change/${changeName}`, {
      data: {
        status: 'Completed',
        close_code: 'Successful',
        close_notes: 'DB index patch successfully applied.'
      }
    });
    expect(closeChangeRes.ok()).toBeTruthy();

    // 7. Verify that resolving/completing the Change automatically set the Problem status to 'Resolved'
    const checkProblemRes = await apiContext.get(`/api/resource/ITSM Problem/${problemName}`);
    expect(checkProblemRes.ok()).toBeTruthy();
    const checkProblem = await checkProblemRes.json();
    expect(checkProblem.data.status).toBe('Resolved');
    expect(checkProblem.data.permanent_fix).toContain(changeName);

    // 8. Verify that the linked Incident was automatically resolved
    const checkIncidentRes = await apiContext.get(`/api/resource/ITSM Incident/${incidentName}`);
    expect(checkIncidentRes.ok()).toBeTruthy();
    const checkIncident = await checkIncidentRes.json();
    expect(checkIncident.data.status).toBe('Resolved');
    expect(checkIncident.data.resolution_notes).toContain(problemName);
  });
});
