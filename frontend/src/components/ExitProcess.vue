<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200">
    <div class="p-6 border-b border-gray-200">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-900">Exit Process</h3>
        <div class="flex items-center space-x-2">
          <select v-model="selectedStatus" @change="loadExitProcesses" class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm">
            <option value="">All Status</option>
            <option value="Initiated">Initiated</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </div>
      </div>
    </div>

    <div class="p-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Exit Processes List -->
      <div v-else-if="exitProcesses.length > 0" class="space-y-4">
        <div v-for="process in exitProcesses" :key="process.name" class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h4 class="font-medium text-gray-900">{{ process.employee_name }}</h4>
                <span :class="getStatusClass(process.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ process.status }}
                </span>
                <span :class="getExitTypeClass(process.exit_type)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ process.exit_type }}
                </span>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Exit Date:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(process.exit_date) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Last Working Day:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(process.last_working_day) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Reason:</span>
                  <p class="font-medium text-gray-900">{{ process.reason }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Status:</span>
                  <p class="font-medium text-gray-900">{{ process.status }}</p>
                </div>
              </div>
              
              <div v-if="process.notes" class="mt-3">
                <span class="text-gray-600 text-sm">Notes:</span>
                <p class="text-gray-900 text-sm mt-1 line-clamp-2">{{ process.notes }}</p>
              </div>
            </div>
            
            <div class="ml-4 flex-shrink-0">
              <button 
                @click="viewExitDetails(process)"
                class="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-8 text-gray-500">
        <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4 4m4-4v4m0-4h-4M6 4l-4 4m0 0l4-4m-4 4v4m0-4h4"/>
        </svg>
        <p class="text-lg font-medium text-gray-900 mb-2">No Exit Processes Found</p>
        <p class="text-sm text-gray-500">Exit processes will appear here when initiated</p>
      </div>
    </div>

    <!-- Exit Details Modal -->
    <div v-if="selectedProcess" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-semibold text-gray-900">Exit Process Details</h3>
          <button @click="selectedProcess = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <div class="space-y-6">
          <!-- Basic Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Employee Information</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Name:</span>
                  <span class="font-medium text-gray-900">{{ selectedProcess.employee_name }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Employee ID:</span>
                  <span class="font-medium text-gray-900">{{ selectedProcess.employee }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Department:</span>
                  <span class="font-medium text-gray-900">{{ selectedProcess.department || 'N/A' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Designation:</span>
                  <span class="font-medium text-gray-900">{{ selectedProcess.designation || 'N/A' }}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Exit Information</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Exit Type:</span>
                  <span :class="getExitTypeClass(selectedProcess.exit_type)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ selectedProcess.exit_type }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Status:</span>
                  <span :class="getStatusClass(selectedProcess.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ selectedProcess.status }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Exit Date:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(selectedProcess.exit_date) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Last Working Day:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(selectedProcess.last_working_day) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Exit Details -->
          <div>
            <h4 class="text-sm font-medium text-gray-700 mb-3">Exit Details</h4>
            <div class="space-y-3">
              <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
                <h5 class="font-medium text-gray-900 mb-1">Reason for Exit</h5>
                <p class="text-sm text-gray-700">{{ selectedProcess.reason }}</p>
              </div>
              
              <div v-if="selectedProcess.notes" class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <h5 class="font-medium text-blue-900 mb-1">Additional Notes</h5>
                <p class="text-sm text-blue-700">{{ selectedProcess.notes }}</p>
              </div>
            </div>
          </div>

          <!-- Checklist Items -->
          <div v-if="selectedProcess.checklist_items && selectedProcess.checklist_items.length > 0">
            <h4 class="text-sm font-medium text-gray-700 mb-3">Exit Checklist</h4>
            <div class="space-y-2">
              <div v-for="item in selectedProcess.checklist_items" :key="item.name" class="border border-gray-200 rounded-lg p-3">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <input 
                      type="checkbox" 
                      :checked="item.is_completed" 
                      disabled
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <span class="font-medium text-gray-900">{{ item.checklist_item }}</span>
                  </div>
                  <span :class="getItemStatusClass(item.is_completed)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ item.is_completed ? 'Completed' : 'Pending' }}
                  </span>
                </div>
                <p v-if="item.notes" class="text-sm text-gray-600 mt-2">{{ item.notes }}</p>
              </div>
            </div>
          </div>

          <!-- Handover Details -->
          <div v-if="selectedProcess.handover_details">
            <h4 class="text-sm font-medium text-gray-700 mb-3">Handover Details</h4>
            <div class="bg-green-50 border border-green-200 rounded-lg p-3">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Handover To:</span>
                  <p class="font-medium text-gray-900">{{ selectedProcess.handover_details.handover_to || 'N/A' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Handover Date:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(selectedProcess.handover_details.handover_date) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Assets Returned:</span>
                  <p class="font-medium text-gray-900">{{ selectedProcess.handover_details.assets_returned || 'Pending' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Clearance Status:</span>
                  <p class="font-medium text-gray-900">{{ selectedProcess.handover_details.clearance_status || 'Pending' }}</p>
                </div>
              </div>
              <div v-if="selectedProcess.handover_details.notes" class="mt-3">
                <span class="text-gray-600 text-sm">Notes:</span>
                <p class="text-sm text-gray-700 mt-1">{{ selectedProcess.handover_details.notes }}</p>
              </div>
            </div>
          </div>

          <!-- Exit Interview -->
          <div v-if="selectedProcess.exit_interview">
            <h4 class="text-sm font-medium text-gray-700 mb-3">Exit Interview</h4>
            <div class="bg-purple-50 border border-purple-200 rounded-lg p-3">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Interview Date:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(selectedProcess.exit_interview.interview_date) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Interviewer:</span>
                  <p class="font-medium text-gray-900">{{ selectedProcess.exit_interview.interviewer || 'N/A' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Feedback:</span>
                  <p class="font-medium text-gray-900">{{ selectedProcess.exit_interview.feedback || 'N/A' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Recommendations:</span>
                  <p class="font-medium text-gray-900">{{ selectedProcess.exit_interview.recommendations || 'N/A' }}</p>
                </div>
              </div>
              <div v-if="selectedProcess.exit_interview.notes" class="mt-3">
                <span class="text-gray-600 text-sm">Notes:</span>
                <p class="text-sm text-gray-700 mt-1">{{ selectedProcess.exit_interview.notes }}</p>
              </div>
            </div>
          </div>

          <!-- Final Settlement -->
          <div v-if="selectedProcess.final_settlement">
            <h4 class="text-sm font-medium text-gray-700 mb-3">Final Settlement</h4>
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Settlement Date:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(selectedProcess.final_settlement.settlement_date) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Total Amount:</span>
                  <p class="font-medium text-gray-900">₹{{ selectedProcess.final_settlement.total_amount || 'N/A' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Status:</span>
                  <p class="font-medium text-gray-900">{{ selectedProcess.final_settlement.status || 'Pending' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Payment Method:</span>
                  <p class="font-medium text-gray-900">{{ selectedProcess.final_settlement.payment_method || 'N/A' }}</p>
                </div>
              </div>
              <div v-if="selectedProcess.final_settlement.notes" class="mt-3">
                <span class="text-gray-600 text-sm">Notes:</span>
                <p class="text-sm text-gray-700 mt-1">{{ selectedProcess.final_settlement.notes }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 pt-4 border-t border-gray-200">
          <button 
            @click="selectedProcess = null"
            class="w-full px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
  employeeId: {
    type: String,
    required: true
  }
})

// Reactive data
const loading = ref(false)
const exitProcesses = ref([])
const selectedStatus = ref('')
const selectedProcess = ref(null)

// Methods
const getStatusClass = (status) => {
  const classes = {
    'Initiated': 'bg-yellow-100 text-yellow-800',
    'In Progress': 'bg-blue-100 text-blue-800',
    'Completed': 'bg-green-100 text-green-800',
    'Cancelled': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getExitTypeClass = (exitType) => {
  const classes = {
    'Resignation': 'bg-blue-100 text-blue-800',
    'Termination': 'bg-red-100 text-red-800',
    'Retirement': 'bg-green-100 text-green-800',
    'End of Contract': 'bg-purple-100 text-purple-800'
  }
  return classes[exitType] || 'bg-gray-100 text-gray-800'
}

const getItemStatusClass = (isCompleted) => {
  return isCompleted ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const loadExitProcesses = async () => {
  loading.value = true
  
  try {
    const filters = {
      employee: props.employeeId
    }
    
    if (selectedStatus.value) {
      filters.status = selectedStatus.value
    }
    
    const response = await call('frappe.client.get_list', {
      doctype: 'Employee Separation',
      fields: [
        'name', 'employee', 'employee_name', 'department', 'designation',
        'exit_type', 'status', 'exit_date', 'last_working_day', 'reason', 'notes'
      ],
      filters: filters,
      order_by: 'creation desc'
    })
    
    // Get detailed information for each exit process
    const processesWithDetails = await Promise.all(
      response.map(async (process) => {
        // Get checklist items
        const checklistItems = await call('frappe.client.get_list', {
          doctype: 'Exit Checklist',
          fields: ['name', 'checklist_item', 'is_completed', 'notes'],
          filters: { parent: process.name }
        })
        
        // Get handover details
        let handoverDetails = null
        const handover = await call('frappe.client.get_list', {
          doctype: 'Employee Handover',
          fields: ['name', 'handover_to', 'handover_date', 'assets_returned', 'clearance_status', 'notes'],
          filters: { employee_separation: process.name }
        })
        
        if (handover.length > 0) {
          handoverDetails = handover[0]
        }
        
        // Get exit interview details
        let exitInterview = null
        const interview = await call('frappe.client.get_list', {
          doctype: 'Exit Interview',
          fields: ['name', 'interview_date', 'interviewer', 'feedback', 'recommendations', 'notes'],
          filters: { employee_separation: process.name }
        })
        
        if (interview.length > 0) {
          exitInterview = interview[0]
        }
        
        // Get final settlement details
        let finalSettlement = null
        const settlement = await call('frappe.client.get_list', {
          doctype: 'Final Settlement',
          fields: ['name', 'settlement_date', 'total_amount', 'status', 'payment_method', 'notes'],
          filters: { employee_separation: process.name }
        })
        
        if (settlement.length > 0) {
          finalSettlement = settlement[0]
        }
        
        return {
          ...process,
          checklist_items: checklistItems,
          handover_details: handoverDetails,
          exit_interview: exitInterview,
          final_settlement: finalSettlement
        }
      })
    )
    
    exitProcesses.value = processesWithDetails
  } catch (error) {
    console.error('Error loading exit processes:', error)
    exitProcesses.value = []
  } finally {
    loading.value = false
  }
}

const viewExitDetails = (process) => {
  selectedProcess.value = process
}

// Initialize component
onMounted(async () => {
  await loadExitProcesses()
})
</script>
