<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">My Tickets</h1>
    <div class="bg-white rounded-lg shadow-sm border overflow-hidden">
      <div v-if="tickets.loading" class="p-8 text-center text-gray-500">
        Loading tickets...
      </div>
      <div v-else-if="tickets.data && tickets.data.length === 0" class="p-8 text-center text-gray-500">
        You don't have any open tickets.
      </div>
      <table v-else class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 border-b">
            <th class="p-4 font-medium text-gray-600 text-sm">Ticket ID</th>
            <th class="p-4 font-medium text-gray-600 text-sm">Subject</th>
            <th class="p-4 font-medium text-gray-600 text-sm">Status</th>
            <th class="p-4 font-medium text-gray-600 text-sm">Created On</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ticket in tickets.data" :key="ticket.name" class="border-b hover:bg-gray-50 cursor-pointer">
            <td class="p-4 text-blue-600 font-medium">{{ ticket.name }}</td>
            <td class="p-4">{{ ticket.title }}</td>
            <td class="p-4">
              <span class="px-2 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium">
                {{ ticket.status }}
              </span>
            </td>
            <td class="p-4 text-gray-500">{{ ticket.creation ? ticket.creation.split(' ')[0] : '' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyTickets',
  resources: {
    tickets() {
      return {
        url: 'frappe.client.get_list',
        params: {
          doctype: 'ITSM Incident',
          fields: ['name', 'title', 'status', 'creation'],
          limit_page_length: 20
        },
        auto: true
      }
    }
  }
}
</script>
