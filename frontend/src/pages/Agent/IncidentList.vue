<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Incidents</h1>
      <Button variant="solid" color="blue" icon-left="plus">New Incident</Button>
    </div>

    <div class="bg-white rounded-lg shadow-sm border overflow-hidden">
      <div v-if="incidents.loading" class="p-8 text-center text-gray-500">
        Loading incidents...
      </div>
      <div v-else-if="incidents.data && incidents.data.length === 0" class="p-8 text-center text-gray-500">
        No incidents found.
      </div>
      <table v-else class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 border-b">
            <th class="p-4 font-medium text-gray-600 text-sm">ID</th>
            <th class="p-4 font-medium text-gray-600 text-sm">Title</th>
            <th class="p-4 font-medium text-gray-600 text-sm">Status</th>
            <th class="p-4 font-medium text-gray-600 text-sm">Priority</th>
            <th class="p-4 font-medium text-gray-600 text-sm">Assignee</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="incident in incidents.data" :key="incident.name" class="border-b hover:bg-gray-50 cursor-pointer">
            <td class="p-4 text-blue-600 font-medium">{{ incident.name }}</td>
            <td class="p-4">{{ incident.title }}</td>
            <td class="p-4">
              <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                {{ incident.status }}
              </span>
            </td>
            <td class="p-4">{{ incident.priority }}</td>
            <td class="p-4 text-gray-500">{{ incident.assigned_to || 'Unassigned' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { Button } from 'frappe-ui'

export default {
  name: 'IncidentList',
  components: {
    Button
  },
  resources: {
    incidents() {
      return {
        url: 'frappe.client.get_list',
        params: {
          doctype: 'ITSM Incident',
          fields: ['name', 'title', 'status', 'priority', 'assigned_to'],
          limit_page_length: 50
        },
        auto: true
      }
    }
  }
}
</script>
