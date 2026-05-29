const { test, expect } = require('@playwright/test');
const crypto = require('crypto');

test.describe('ITSM Phase 2 Transitions & Phase 1 Gaps', () => {
  let apiContext;

  test.beforeAll(async ({ playwright }) => {
    apiContext = await playwright.request.newContext({
      baseURL: process.env.FRAPPE_BASE_URL || 'http://192.168.252.6:8007',
    });

    // Login as Admin
    const loginRes = await apiContext.post('/api/method/login', {
      form: { usr: 'Administrator', pwd: 'admin' }
    });
    expect(loginRes.ok()).toBeTruthy();

    // Ensure pw_test_user_1@example.com exists
    const userEmail = 'pw_test_user_1@example.com';
    const checkUser = await apiContext.get(`/api/resource/User/${userEmail}`);
    if (!checkUser.ok()) {
      const createUser = await apiContext.post('/api/resource/User', {
        data: {
          email: userEmail,
          first_name: 'PW_TEST_USER_1',
          send_welcome_email: 0,
          roles: [{ role: 'ITSM Agent' }]
        }
      });
      expect(createUser.ok()).toBeTruthy();
    }
  });


  test('Should perform calendar-aware SLA calculations', async () => {
    const whName = 'PW_TEST_Working_Hours';
    // Ensure clean working hours config
    await apiContext.delete(`/api/resource/ITSM Working Hours/${whName}`);
    const whRes = await apiContext.post('/api/resource/ITSM Working Hours', {
      data: {
        schedule_name: whName,
        timezone: 'UTC',
        monday_start: '09:00:00', monday_end: '17:00:00',
        tuesday_start: '09:00:00', tuesday_end: '17:00:00',
        wednesday_start: '09:00:00', wednesday_end: '17:00:00',
        thursday_start: '09:00:00', thursday_end: '17:00:00',
        friday_start: '09:00:00', friday_end: '17:00:00'
      }
    });
    expect(whRes.ok()).toBeTruthy();

    const hlName = 'PW_TEST_Holiday_List';
    // Clean up if it exists
    await apiContext.delete(`/api/resource/ITSM Holiday List/${hlName}`);
    const hlRes = await apiContext.post('/api/resource/ITSM Holiday List', {
      data: {
        list_name: hlName,
        holidays: [
          { holiday_date: '2026-06-01', description: 'Test Holiday' } // Monday, June 1st, 2026
        ]
      }
    });
    expect(hlRes.ok()).toBeTruthy();

    // Call the whitelisted SLA calculation endpoint directly
    // Start date: Friday, May 29, 2026 at 16:00:00 UTC (1 hour remaining in work day).
    // SLA duration: 120 mins (2 hours).
    // Rollover: 1 hour on Friday, skip Sat & Sun, skip Monday (June 1st, holiday).
    // Result should end on Tuesday, June 2, 2026 at 10:00:00 UTC (9:00 + 1 hour).
    const calcRes = await apiContext.get('/api/method/frappe_itsm.frappe_itsm.sla_evaluator.calculate_sla_due', {
      params: {
        start_time: '2026-05-29 16:00:00',
        duration_mins: 120,
        working_hours_name: whName,
        holiday_list_name: hlName
      }
    });
    expect(calcRes.ok()).toBeTruthy();
    const result = await calcRes.json();
    
    // Check returned date (UTC format is usually YYYY-MM-DD HH:MM:SS or ISO format)
    expect(result.message).toContain('2026-06-02 10:00:00');

    // Clean up
    await apiContext.delete(`/api/resource/ITSM Holiday List/${hlName}`);
    await apiContext.delete(`/api/resource/ITSM Working Hours/${whName}`);
  });

  test('Should detect duplicate incidents and automatically link them', async () => {
    const caller = 'Administrator';
    const category = 'Hardware';
    const inc1 = await apiContext.post('/api/resource/ITSM Incident', {
      data: {
        title: 'PW_TEST Duplicate Parent',
        category: category,
        caller: caller,
        raised_by: caller,
        impact: '4-Individual',
        urgency: '4-Low',
        description: 'First ticket',
        company: 'Mindgraph Technologies Pvt Ltd'
      }
    });
    expect(inc1.ok()).toBeTruthy();
    const inc1Data = await inc1.json();
    const parentName = inc1Data.data.name;

    // Create second incident with same caller/category
    const inc2 = await apiContext.post('/api/resource/ITSM Incident', {
      data: {
        title: 'PW_TEST Duplicate Child',
        category: category,
        caller: caller,
        raised_by: caller,
        impact: '4-Individual',
        urgency: '4-Low',
        description: 'Second ticket',
        company: 'Mindgraph Technologies Pvt Ltd'
      }
    });

    expect(inc2.ok()).toBeTruthy();
    const inc2Data = await inc2.json();
    const childName = inc2Data.data.name;
    const parentIncident = inc2Data.data.parent_incident;

    expect(parentIncident).toBe(parentName);

    // Teardown
    await apiContext.delete(`/api/resource/ITSM Incident/${parentName}`);
    await apiContext.delete(`/api/resource/ITSM Incident/${childName}`);
  });

  test('Should verify CAB guest voting using signed URLs', async () => {
    const chg = await apiContext.post('/api/resource/ITSM Change', {
      data: {
        title: 'PW_TEST CAB Change',
        change_type: 'Normal',
        priority: 'Medium',
        risk_level: 'Low',
        impact: '4-Individual',
        category: 'Software',
        change_initiator: 'Administrator',
        change_owner: 'Administrator',
        assigned_team: 'IT Service Desk',
        description: 'Testing CAB voting',
        justification: 'None',
        implementation_plan: 'None',
        start_datetime: '2026-06-01 10:00:00',
        end_datetime: '2026-06-01 12:00:00'
      }
    });
    expect(chg.ok()).toBeTruthy();
    const chgData = await chg.json();
    const chgName = chgData.data.name;

    // Set change status to CAB Scheduled by stepping through workflow
    const statesToCAB = ['Draft', 'Pending Review', 'CAB Scheduled'];
    for (const state of statesToCAB) {
      const res = await apiContext.put(`/api/resource/ITSM Change/${chgName}`, {
        data: { status: state }
      });
      expect(res.ok()).toBeTruthy();
    }


    const meetingName = 'PW_TEST_CAB_Meeting';
    // Clean up if it exists
    await apiContext.delete(`/api/resource/ITSM CAB Meeting/${meetingName}`);
    const meeting = await apiContext.post('/api/resource/ITSM CAB Meeting', {
      data: {
        name: meetingName,
        meeting_type: 'Regular CAB',
        scheduled_datetime: '2026-06-02 14:00:00',
        duration_minutes: 60,
        cab_chair: 'Administrator',
        quorum_required: 100,
        cab_members: [
          { user: 'pw_test_user_1@example.com', role: 'CAB Member', vote: 'Pending' }
        ],
        agenda_changes: [
          { change_request: chgName, presenter: 'Administrator', decision: 'Pending' }
        ]
      }
    });
    expect(meeting.ok()).toBeTruthy();
    const meetingData = await meeting.json();
    const actualMeetingName = meetingData.data.name;

    const userEmail = 'pw_test_user_1@example.com';
    const vote = 'Approve';
    
    // Fetch signed vote token from backend
    const tokenRes = await apiContext.get('/api/method/frappe_itsm.frappe_itsm.doctype.itsm_cab_meeting.itsm_cab_meeting.get_signed_vote_token', {
      params: {
        meeting: actualMeetingName,
        user: userEmail,
        change: chgName,
        vote: vote
      }
    });
    expect(tokenRes.ok()).toBeTruthy();
    const tokenData = await tokenRes.json();
    const token = tokenData.message;


    const voteRes = await apiContext.get('/api/method/frappe_itsm.frappe_itsm.doctype.itsm_cab_meeting.itsm_cab_meeting.record_cab_vote', {
      params: {
        meeting: actualMeetingName,
        user: userEmail,
        change: chgName,
        vote: vote,
        token: token
      }
    });
    if (!voteRes.ok()) {
      console.error("VOTE RES FAIL:", voteRes.status(), await voteRes.text());
    }
    expect(voteRes.ok()).toBeTruthy();


    const updatedMeetingRes = await apiContext.get(`/api/resource/ITSM CAB Meeting/${actualMeetingName}`);
    expect(updatedMeetingRes.ok()).toBeTruthy();
    const updatedMeeting = await updatedMeetingRes.json();
    expect(updatedMeeting.data.cab_members[0].vote).toBe('Approve');
    expect(updatedMeeting.data.agenda_changes[0].decision).toBe('Approved');

    const updatedChgRes = await apiContext.get(`/api/resource/ITSM Change/${chgName}`);
    expect(updatedChgRes.ok()).toBeTruthy();
    const updatedChg = await updatedChgRes.json();
    expect(updatedChg.data.status).toBe('CAB Approved');

    // Teardown
    await apiContext.delete(`/api/resource/ITSM CAB Meeting/${actualMeetingName}`);
    await apiContext.delete(`/api/resource/ITSM Change/${chgName}`);
  });

  test('Should trace CMDB relationships and BFS impact paths', async () => {
    const ciA = 'PW_TEST_CI_A';
    const ciB = 'PW_TEST_CI_B';
    const ciC = 'PW_TEST_CI_C';

    for (const ci of [ciA, ciB, ciC]) {
      await apiContext.delete(`/api/resource/ITSM CI/${ci}`);
      await apiContext.post('/api/resource/ITSM CI', {
        data: { ci_name: ci, ci_type: 'Application', status: 'Active' }
      });
    }

    const rel1 = await apiContext.post('/api/resource/ITSM CI Relationship', {
      data: { parent_ci: ciA, relationship_type: 'Depends On', child_ci: ciB }
    });
    expect(rel1.ok()).toBeTruthy();
    const rel1Data = await rel1.json();

    const rel2 = await apiContext.post('/api/resource/ITSM CI Relationship', {
      data: { parent_ci: ciB, relationship_type: 'Runs On', child_ci: ciC }
    });
    expect(rel2.ok()).toBeTruthy();
    const rel2Data = await rel2.json();

    const impactRes = await apiContext.get('/api/method/frappe_itsm.frappe_itsm.utils.cmdb.get_upstream_impact_api', {
      params: { ci_name: ciC }
    });
    expect(impactRes.ok()).toBeTruthy();
    const impactData = await impactRes.json();
    
    expect(impactData.message).toContain(ciB);
    expect(impactData.message).toContain(ciA);

    // Teardown
    await apiContext.delete(`/api/resource/ITSM CI Relationship/${rel1Data.data.name}`);
    await apiContext.delete(`/api/resource/ITSM CI Relationship/${rel2Data.data.name}`);
    for (const ci of [ciA, ciB, ciC]) {
      await apiContext.delete(`/api/resource/ITSM CI/${ci}`);
    }
  });

  test.afterAll(async () => {
    const userEmail = 'pw_test_user_1@example.com';
    await apiContext.delete(`/api/resource/User/${userEmail}`);
  });
});
