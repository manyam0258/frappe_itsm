const { test, expect } = require('@playwright/test');

test.describe('ITSM Workflow-Assignment Engine Integration', () => {
  let apiContext;
  const user1Email = 'pw_test_user_1@example.com';
  const user2Email = 'pw_test_user_2@example.com';
  const teamName = 'PW_TEST_Assignment_Team';
  const ruleName = 'PW_TEST_Assignment_Rule';
  let createdIncidentName;
  let secondIncidentName;
  let ruleDocName;
  let problemRuleDocName;
  let firstAssignee;
  const createdIncidents = [];
  const createdProblems = [];

  test.beforeAll(async ({ playwright }) => {
    apiContext = await playwright.request.newContext({
      baseURL: process.env.FRAPPE_BASE_URL || 'http://192.168.252.6:8007',
    });

    // 1. Login as Admin
    const loginRes = await apiContext.post('/api/method/login', {
      form: { usr: 'Administrator', pwd: 'admin' }
    });
    expect(loginRes.ok()).toBeTruthy();

    // 2. Ensure test users exist with ITSM Agent role
    for (const email of [user1Email, user2Email]) {
      const checkUser = await apiContext.get(`/api/resource/User/${email}`);
      if (!checkUser.ok()) {
        const createUser = await apiContext.post('/api/resource/User', {
          data: {
            email: email,
            first_name: email.split('@')[0].toUpperCase(),
            send_welcome_email: 0,
            roles: [{ role: 'ITSM Agent' }]
          }
        });
        expect(createUser.ok()).toBeTruthy();
      }
    }

    // 3. Ensure ITSM Team exists
    const checkTeam = await apiContext.get(`/api/resource/ITSM Team/${teamName}`);
    if (!checkTeam.ok()) {
      const createTeam = await apiContext.post('/api/resource/ITSM Team', {
        data: {
          team_name: teamName,
          description: 'Team for Playwright workflow assignment tests'
        }
      });
      expect(createTeam.ok()).toBeTruthy();
    }

    // 4. Create an Assignment Rule for Incident
    // Clean up any existing rule first to avoid conflicts
    const getRule = await apiContext.get('/api/resource/Assignment Rule', {
      params: {
        filters: JSON.stringify([
          ["document_type", "=", "ITSM Incident"],
          ["assign_condition", "like", `%${teamName}%`]
        ])
      }
    });
    if (getRule.ok()) {
      const ruleJson = await getRule.json();
      if (ruleJson.data && ruleJson.data.length > 0) {
        await apiContext.delete(`/api/resource/Assignment Rule/${ruleJson.data[0].name}`);
      }
    }

    const createRule = await apiContext.post('/api/resource/Assignment Rule', {
      data: {
        name: ruleName,
        document_type: 'ITSM Incident',
        rule: 'Round Robin',
        disabled: 0,
        assign_condition: `assigned_team == "${teamName}" and workflow_state == "Assigned"`,
        description: 'Auto route incident to team members in Assigned state',
        users: [
          { user: user1Email },
          { user: user2Email }
        ],
        assignment_days: [
          { day: 'Monday' },
          { day: 'Tuesday' },
          { day: 'Wednesday' },
          { day: 'Thursday' },
          { day: 'Friday' },
          { day: 'Saturday' },
          { day: 'Sunday' }
        ]
      }
    });
    if (!createRule.ok()) {
      console.error("Failed to create Assignment Rule:", await createRule.text());
    }
    expect(createRule.ok()).toBeTruthy();
    const ruleResult = await createRule.json();
    ruleDocName = ruleResult.data.name;

    // 5. Create an Assignment Rule for Problem
    // Clean up any existing Problem rule first to avoid conflicts
    const getProbRule = await apiContext.get('/api/resource/Assignment Rule', {
      params: {
        filters: JSON.stringify([
          ["document_type", "=", "ITSM Problem"],
          ["assign_condition", "like", `%${teamName}%`]
        ])
      }
    });
    if (getProbRule.ok()) {
      const ruleJson = await getProbRule.json();
      if (ruleJson.data && ruleJson.data.length > 0) {
        await apiContext.delete(`/api/resource/Assignment Rule/${ruleJson.data[0].name}`);
      }
    }

    const createProblemRule = await apiContext.post('/api/resource/Assignment Rule', {
      data: {
        name: 'PW_TEST_Problem_Assignment_Rule',
        document_type: 'ITSM Problem',
        rule: 'Round Robin',
        disabled: 0,
        assign_condition: `assigned_team == "${teamName}" and status == "Assess"`,
        description: 'Auto route problem to team members in Assess state',
        users: [
          { user: user1Email },
          { user: user2Email }
        ],
        assignment_days: [
          { day: 'Monday' },
          { day: 'Tuesday' },
          { day: 'Wednesday' },
          { day: 'Thursday' },
          { day: 'Friday' },
          { day: 'Saturday' },
          { day: 'Sunday' }
        ]
      }
    });
    if (!createProblemRule.ok()) {
      console.error("Failed to create Problem Assignment Rule:", await createProblemRule.text());
    }
    expect(createProblemRule.ok()).toBeTruthy();
    const problemRuleResult = await createProblemRule.json();
    problemRuleDocName = problemRuleResult.data.name;
  });

  test('Should dynamically assign incident on state transition and preserve audit trail', async () => {
    // 1. Create a new ITSM Incident in New state
    const incidentRes = await apiContext.post('/api/resource/ITSM Incident', {
      data: {
        title: 'PW_TEST_Workflow Assignment Test ticket 1',
        category: 'Software',
        impact: '4-Individual',
        urgency: '4-Low',
        description: 'Testing automatic round robin assignment on workflow transition',
        company: 'Mindgraph Technologies Pvt Ltd',
        assigned_team: teamName,
        workflow_state: 'New',
        raised_by: 'Administrator',
        caller: 'Administrator'
      }
    });
    if (!incidentRes.ok()) {
      console.error("Failed to create Incident:", await incidentRes.text());
    }
    expect(incidentRes.ok()).toBeTruthy();
    const incident = await incidentRes.json();
    createdIncidentName = incident.data.name;
    createdIncidents.push(createdIncidentName);

    // Verify no ToDos exist yet for this incident
    const initialTodosRes = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Incident"],
          ["reference_name", "=", createdIncidentName]
        ])
      }
    });
    expect(initialTodosRes.ok()).toBeTruthy();
    const initialTodos = await initialTodosRes.json();
    expect(initialTodos.data.length).toBe(0);

    // 2. Transition Incident workflow state to 'Assigned'
    // This should trigger handle_workflow_assignments and apply the assignment rule
    const transitionRes = await apiContext.put(`/api/resource/ITSM Incident/${createdIncidentName}`, {
      data: {
        workflow_state: 'Assigned'
      }
    });
    expect(transitionRes.ok()).toBeTruthy();

    // 3. Verify a ToDo assignment was created
    const assignedTodosRes = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Incident"],
          ["reference_name", "=", createdIncidentName],
          ["status", "=", "Open"]
        ]),
        fields: JSON.stringify(["name", "allocated_to", "status"])
      }
    });
    expect(assignedTodosRes.ok()).toBeTruthy();
    const assignedTodos = await assignedTodosRes.json();
    expect(assignedTodos.data.length).toBe(1);

    firstAssignee = assignedTodos.data[0].allocated_to;
    expect([user1Email, user2Email]).toContain(firstAssignee);

    // 4. Transition Incident to 'In Progress'
    // This should change the workflow state and cause the previous assignment to be Cancelled
    const nextTransitionRes = await apiContext.put(`/api/resource/ITSM Incident/${createdIncidentName}`, {
      data: {
        workflow_state: 'In Progress'
      }
    });
    expect(nextTransitionRes.ok()).toBeTruthy();

    // 5. Verify the old ToDo status is Cancelled (preserving audit trail)
    const closedTodosRes = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Incident"],
          ["reference_name", "=", createdIncidentName],
          ["status", "=", "Cancelled"]
        ]),
        fields: JSON.stringify(["name", "allocated_to", "status"])
      }
    });
    expect(closedTodosRes.ok()).toBeTruthy();
    const closedTodos = await closedTodosRes.json();
    expect(closedTodos.data.length).toBe(1);
    expect(closedTodos.data[0].allocated_to).toBe(firstAssignee);

    // 6. Transition Incident to 'Resolved'
    const resolveTransitionRes = await apiContext.put(`/api/resource/ITSM Incident/${createdIncidentName}`, {
      data: {
        workflow_state: 'Resolved'
      }
    });
    expect(resolveTransitionRes.ok()).toBeTruthy();

    // Verify no open ToDos exist
    const openTodosAfterResolve = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Incident"],
          ["reference_name", "=", createdIncidentName],
          ["status", "=", "Open"]
        ])
      }
    });
    expect(openTodosAfterResolve.ok()).toBeTruthy();
    const openTodosResolve = await openTodosAfterResolve.json();
    expect(openTodosResolve.data.length).toBe(0);

    // Check that our audit trail Cancelled ToDo still exists
    const auditTodosAfterResolve = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Incident"],
          ["reference_name", "=", createdIncidentName],
          ["status", "=", "Cancelled"]
        ])
      }
    });
    expect(auditTodosAfterResolve.ok()).toBeTruthy();
    const auditTodosResolve = await auditTodosAfterResolve.json();
    expect(auditTodosResolve.data.length).toBe(1);

    // 7. Transition Incident to 'Closed'
    const closeTransitionRes = await apiContext.put(`/api/resource/ITSM Incident/${createdIncidentName}`, {
      data: {
        workflow_state: 'Closed'
      }
    });
    expect(closeTransitionRes.ok()).toBeTruthy();

    // Verify no open ToDos exist
    const openTodosAfterClose = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Incident"],
          ["reference_name", "=", createdIncidentName],
          ["status", "=", "Open"]
        ])
      }
    });
    expect(openTodosAfterClose.ok()).toBeTruthy();
    const openTodosClose = await openTodosAfterClose.json();
    expect(openTodosClose.data.length).toBe(0);

    // Check that our audit trail Cancelled ToDo still exists
    const auditTodosAfterClose = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Incident"],
          ["reference_name", "=", createdIncidentName],
          ["status", "=", "Cancelled"]
        ])
      }
    });
    expect(auditTodosAfterClose.ok()).toBeTruthy();
    const auditTodosClose = await auditTodosAfterClose.json();
    expect(auditTodosClose.data.length).toBe(1);
  });

  test('Should alternate assignees in Round Robin order for successive assignments', async () => {
    expect(firstAssignee).toBeDefined();

    // 1. Create a second ITSM Incident in New state
    const incidentRes2 = await apiContext.post('/api/resource/ITSM Incident', {
      data: {
        title: 'PW_TEST_Workflow Assignment Test ticket 2',
        category: 'Software',
        impact: '4-Individual',
        urgency: '4-Low',
        description: 'Testing second incident assignment for round robin alternation',
        company: 'Mindgraph Technologies Pvt Ltd',
        assigned_team: teamName,
        workflow_state: 'New',
        raised_by: 'Administrator',
        caller: 'Administrator'
      }
    });
    expect(incidentRes2.ok()).toBeTruthy();
    const incident2 = await incidentRes2.json();
    secondIncidentName = incident2.data.name;
    createdIncidents.push(secondIncidentName);

    // 2. Transition second incident workflow state to 'Assigned'
    const transitionRes2 = await apiContext.put(`/api/resource/ITSM Incident/${secondIncidentName}`, {
      data: {
        workflow_state: 'Assigned'
      }
    });
    expect(transitionRes2.ok()).toBeTruthy();

    // 3. Verify a ToDo assignment was created
    const assignedTodosRes2 = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Incident"],
          ["reference_name", "=", secondIncidentName],
          ["status", "=", "Open"]
        ]),
        fields: JSON.stringify(["name", "allocated_to", "status"])
      }
    });
    expect(assignedTodosRes2.ok()).toBeTruthy();
    const assignedTodos2 = await assignedTodosRes2.json();
    expect(assignedTodos2.data.length).toBe(1);

    const secondAssignee = assignedTodos2.data[0].allocated_to;
    expect([user1Email, user2Email]).toContain(secondAssignee);

    // 4. Assert that round robin assignment alternated the assignee
    expect(secondAssignee).not.toBe(firstAssignee);

    // 5. Transition second incident to 'In Progress' to clean up / cancel the ToDo
    const nextTransitionRes2 = await apiContext.put(`/api/resource/ITSM Incident/${secondIncidentName}`, {
      data: {
        workflow_state: 'In Progress'
      }
    });
    expect(nextTransitionRes2.ok()).toBeTruthy();
  });

  test('Should prevent illegal workflow state transitions (exception flow)', async () => {
    // 1. Create a third ITSM Incident in New state
    const incidentRes3 = await apiContext.post('/api/resource/ITSM Incident', {
      data: {
        title: 'PW_TEST_Workflow Assignment Test ticket 3',
        category: 'Software',
        impact: '4-Individual',
        urgency: '4-Low',
        description: 'Testing illegal transition constraints',
        company: 'Mindgraph Technologies Pvt Ltd',
        assigned_team: teamName,
        workflow_state: 'New',
        raised_by: 'Administrator',
        caller: 'Administrator'
      }
    });
    expect(incidentRes3.ok()).toBeTruthy();
    const incident3 = await incidentRes3.json();
    const thirdIncidentName = incident3.data.name;
    createdIncidents.push(thirdIncidentName);

    // 2. Attempt illegal transition directly from 'New' to 'Resolved'
    // Under Incident Workflow, New can only transition to 'Assigned' or 'Cancelled'.
    // Transitioning from New to Resolved is invalid and should be rejected.
    const invalidTransitionRes = await apiContext.put(`/api/resource/ITSM Incident/${thirdIncidentName}`, {
      data: {
        workflow_state: 'Resolved'
      }
    });
    
    // We expect this to fail (non-2xx response or forbidden)
    expect(invalidTransitionRes.ok()).toBeFalsy();

    // 3. Verify that the incident state did not change
    const checkIncidentRes = await apiContext.get(`/api/resource/ITSM Incident/${thirdIncidentName}`);
    expect(checkIncidentRes.ok()).toBeTruthy();
    const checkIncident = await checkIncidentRes.json();
    expect(checkIncident.data.workflow_state).toBe('New');

    // 4. Verify no ToDos were created for this incident
    const checkTodosRes = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Incident"],
          ["reference_name", "=", thirdIncidentName]
        ])
      }
    });
    expect(checkTodosRes.ok()).toBeTruthy();
    const checkTodos = await checkTodosRes.json();
    expect(checkTodos.data.length).toBe(0);
  });

  test('Should copy incident creator to problem_owner and round-robin assign problem to a user when team is selected', async () => {
    // 1. Create a test ITSM Incident (which will act as the source incident)
    const incidentRes = await apiContext.post('/api/resource/ITSM Incident', {
      data: {
        title: 'PW_TEST_Incident Source for Problem',
        category: 'Software',
        impact: '4-Individual',
        urgency: '4-Low',
        description: 'Source incident for copying creator/owner information',
        company: 'Mindgraph Technologies Pvt Ltd',
        assigned_team: teamName,
        workflow_state: 'New',
        raised_by: 'Administrator',
        caller: 'Administrator'
      }
    });
    expect(incidentRes.ok()).toBeTruthy();
    const incident = await incidentRes.json();
    const sourceIncidentName = incident.data.name;
    createdIncidents.push(sourceIncidentName);

    // Get the owner of the source incident (should be Administrator)
    const getIncRes = await apiContext.get(`/api/resource/ITSM Incident/${sourceIncidentName}`);
    expect(getIncRes.ok()).toBeTruthy();
    const incData = await getIncRes.json();
    const incidentOwner = incData.data.owner;
    expect(incidentOwner).toBeDefined();

    // 2. Create a new ITSM Problem in New state, linking it to the incident
    const problemRes = await apiContext.post('/api/resource/ITSM Problem', {
      data: {
        title: 'PW_TEST_Problem created from incident',
        category: 'Software',
        description: 'RCA required for incident source',
        assigned_team: teamName,
        status: 'New',
        linked_incidents: [
          {
            incident: sourceIncidentName
          }
        ]
      }
    });
    expect(problemRes.ok()).toBeTruthy();
    const problem = await problemRes.json();
    const problemName = problem.data.name;
    createdProblems.push(problemName);

    // 3. Verify that the problem_owner is automatically copied from the incident's owner
    const getProblemRes1 = await apiContext.get(`/api/resource/ITSM Problem/${problemName}`);
    expect(getProblemRes1.ok()).toBeTruthy();
    const problemData1 = await getProblemRes1.json();
    expect(problemData1.data.problem_owner).toBe(incidentOwner);

    // 4. Transition the Problem workflow state to 'Assess'
    // This should trigger handle_workflow_assignments for problem and apply the Problem assignment rule
    const transitionRes = await apiContext.put(`/api/resource/ITSM Problem/${problemName}`, {
      data: {
        status: 'Assess'
      }
    });
    expect(transitionRes.ok()).toBeTruthy();

    // 5. Verify a ToDo assignment was created for the Problem
    const assignedTodosRes = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Problem"],
          ["reference_name", "=", problemName],
          ["status", "=", "Open"]
        ]),
        fields: JSON.stringify(["name", "allocated_to", "status"])
      }
    });
    expect(assignedTodosRes.ok()).toBeTruthy();
    const assignedTodos = await assignedTodosRes.json();
    expect(assignedTodos.data.length).toBe(1);

    const problemAssignee = assignedTodos.data[0].allocated_to;
    expect([user1Email, user2Email]).toContain(problemAssignee);

    // 6. Verify that the assigned_to field on the problem was set to the assignee
    const getProblemRes2 = await apiContext.get(`/api/resource/ITSM Problem/${problemName}`);
    expect(getProblemRes2.ok()).toBeTruthy();
    const problemData2 = await getProblemRes2.json();
    expect(problemData2.data.assigned_to).toBe(problemAssignee);

    // 7. Transition the Problem to 'Root Cause Analysis'
    // This should cancel the ToDo to preserve the audit trail
    const transitionRes2 = await apiContext.put(`/api/resource/ITSM Problem/${problemName}`, {
      data: {
        status: 'Root Cause Analysis'
      }
    });
    expect(transitionRes2.ok()).toBeTruthy();

    // Verify the old ToDo status is Cancelled (audit trail check)
    const cancelledTodosRes = await apiContext.get('/api/resource/ToDo', {
      params: {
        filters: JSON.stringify([
          ["reference_type", "=", "ITSM Problem"],
          ["reference_name", "=", problemName],
          ["status", "=", "Cancelled"]
        ]),
        fields: JSON.stringify(["name", "allocated_to", "status"])
      }
    });
    expect(cancelledTodosRes.ok()).toBeTruthy();
    const cancelledTodos = await cancelledTodosRes.json();
    expect(cancelledTodos.data.length).toBe(1);
    expect(cancelledTodos.data[0].allocated_to).toBe(problemAssignee);
  });

  test.afterAll(async () => {
    // Teardown testing rules and team
    if (ruleDocName) {
      await apiContext.delete(`/api/resource/Assignment Rule/${ruleDocName}`);
    }
    if (problemRuleDocName) {
      await apiContext.delete(`/api/resource/Assignment Rule/${problemRuleDocName}`);
    }
    await apiContext.delete(`/api/resource/ITSM Team/${teamName}`);
    
    // Clean up created incidents and their associated ToDos
    for (const inc of createdIncidents) {
      const getTodos = await apiContext.get('/api/resource/ToDo', {
        params: {
          filters: JSON.stringify([
            ["reference_type", "=", "ITSM Incident"],
            ["reference_name", "=", inc]
          ])
        }
      });
      if (getTodos.ok()) {
        const todos = await getTodos.json();
        if (todos.data) {
          for (const todo of todos.data) {
            await apiContext.delete(`/api/resource/ToDo/${todo.name}`);
          }
        }
      }
      await apiContext.delete(`/api/resource/ITSM Incident/${inc}`);
    }

    // Clean up created problems and their associated ToDos
    for (const prob of createdProblems) {
      const getTodos = await apiContext.get('/api/resource/ToDo', {
        params: {
          filters: JSON.stringify([
            ["reference_type", "=", "ITSM Problem"],
            ["reference_name", "=", prob]
          ])
        }
      });
      if (getTodos.ok()) {
        const todos = await getTodos.json();
        if (todos.data) {
          for (const todo of todos.data) {
            await apiContext.delete(`/api/resource/ToDo/${todo.name}`);
          }
        }
      }
      await apiContext.delete(`/api/resource/ITSM Problem/${prob}`);
    }

    // Clean up test users
    for (const email of [user1Email, user2Email]) {
      await apiContext.delete(`/api/resource/User/${email}`);
    }
  });
});
