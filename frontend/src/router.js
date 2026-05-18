import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/agent/dashboard',
  },
  {
    path: '/agent',
    component: () => import('@/layouts/AgentLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'AgentDashboard',
        component: () => import('@/pages/Agent/Dashboard.vue'),
      },
      {
        path: 'incidents',
        name: 'IncidentList',
        component: () => import('@/pages/Agent/IncidentList.vue'),
      }
    ]
  },
  {
    path: '/portal',
    component: () => import('@/layouts/PortalLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'PortalDashboard',
        component: () => import('@/pages/Portal/Dashboard.vue'),
      },
      {
        path: 'tickets',
        name: 'MyTickets',
        component: () => import('@/pages/Portal/MyTickets.vue'),
      }
    ]
  }
]

let router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

// Simple Role-based routing guard
router.beforeEach(async (to, from, next) => {
  // In a real app, you would fetch this from a frappe-ui session store or API
  // For this Phase 1 Sprint 4/5 scaffold, we assume Administrator has access to all.
  const isAgentRoute = to.path.startsWith('/agent')
  const isPortalRoute = to.path.startsWith('/portal')
  
  // Example logic:
  // if (isAgentRoute && !user.roles.includes('ITSM Agent')) return next('/portal/dashboard')
  
  next()
})

export default router
