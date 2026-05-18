<template>
  <div>
    <div class="text-center py-12">
      <h1 class="text-4xl font-extrabold text-gray-900 mb-4">How can we help you today?</h1>
      <p class="text-lg text-gray-600 mb-8">Search for answers or raise a new request.</p>
      
      <div class="max-w-2xl mx-auto flex gap-4">
        <input type="text" placeholder="Search knowledge base..." class="flex-1 p-4 rounded-lg border shadow-sm focus:ring-2 focus:ring-blue-500 outline-none" />
        <Button variant="solid" color="blue" size="lg" class="px-8">Search</Button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12">
      <div class="bg-white p-8 rounded-xl border shadow-sm hover:shadow-md transition-shadow cursor-pointer">
        <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-6">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        </div>
        <h3 class="text-xl font-bold mb-2">Report an Issue</h3>
        <p class="text-gray-600">Something isn't working? Let us know and we'll fix it.</p>
      </div>

      <div class="bg-white p-8 rounded-xl border shadow-sm hover:shadow-md transition-shadow cursor-pointer">
        <div class="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-6">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
        </div>
        <h3 class="text-xl font-bold mb-2">Request a Service</h3>
        <p class="text-gray-600">Need new software, hardware, or access?</p>
      </div>
    </div>
  </div>
</template>

<script>
import { Button } from 'frappe-ui'

export default {
  name: 'PortalDashboard',
  components: {
    Button
  }
}
</script>
