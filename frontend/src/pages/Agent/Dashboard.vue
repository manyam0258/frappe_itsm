<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Agent Dashboard</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- KPIs -->
      <div class="bg-white p-6 rounded-lg shadow-sm border">
        <h3 class="text-gray-500 text-sm font-medium">Open Incidents</h3>
        <p class="text-3xl font-bold mt-2">12</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-sm border">
        <h3 class="text-gray-500 text-sm font-medium">SLA Breached</h3>
        <p class="text-3xl font-bold mt-2 text-red-600">2</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-sm border">
        <h3 class="text-gray-500 text-sm font-medium">Pending Approvals</h3>
        <p class="text-3xl font-bold mt-2 text-orange-500">5</p>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="mt-8 bg-white rounded-lg shadow-sm border p-6">
      <h2 class="text-lg font-medium mb-4">Recent Activity</h2>
      <p class="text-gray-500 italic">No recent activity to display.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AgentDashboard'
}
</script>
