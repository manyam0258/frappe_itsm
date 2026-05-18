<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Navbar -->
    <header class="bg-blue-600 text-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4">
            <h1 class="text-xl font-bold">IT Helpdesk</h1>
            <nav class="hidden md:flex space-x-4 ml-6">
              <router-link to="/portal/dashboard" class="px-3 py-2 rounded hover:bg-blue-700 transition-colors" active-class="bg-blue-800 font-medium">Home</router-link>
              <router-link to="/portal/tickets" class="px-3 py-2 rounded hover:bg-blue-700 transition-colors" active-class="bg-blue-800 font-medium">My Tickets</router-link>
            </nav>
          </div>
          <div>
            <!-- Add User Menu -->
            <span class="text-sm font-medium">Self-Service</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t py-6 text-center text-gray-500 text-sm">
      &copy; 2026 Enterprise ITSM. All rights reserved.
    </footer>
  </div>
</template>

<script>
export default {
  name: 'PortalLayout'
}
</script>
