<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <div class="w-64 bg-white border-r flex flex-col">
      <div class="p-4 border-b">
        <h1 class="text-xl font-bold text-gray-800">Frappe ITSM</h1>
        <p class="text-sm text-gray-500">Agent Workspace</p>
      </div>
      <nav class="flex-1 p-4 space-y-2">
        <router-link to="/agent/dashboard" class="block px-4 py-2 rounded text-gray-700 hover:bg-gray-100 transition-colors" active-class="bg-blue-50 text-blue-700 font-medium">
          Dashboard
        </router-link>
        <router-link to="/agent/incidents" class="block px-4 py-2 rounded text-gray-700 hover:bg-gray-100 transition-colors" active-class="bg-blue-50 text-blue-700 font-medium">
          Incidents
        </router-link>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <!-- Topbar -->
      <header class="bg-white border-b h-16 flex items-center px-6 justify-between">
        <h2 class="text-lg font-medium text-gray-800">Agent Portal</h2>
        <div>
          <!-- Add user avatar/menu here -->
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 p-6 overflow-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AgentLayout'
}
</script>
