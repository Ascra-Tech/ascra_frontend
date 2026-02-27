<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200">
    <div class="p-6 border-b border-gray-200">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-900">Performance Appraisals</h3>
        <div class="flex items-center space-x-2">
          <select v-model="selectedCycle" @change="loadAppraisals" class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm">
            <option value="">All Cycles</option>
            <option v-for="cycle in appraisalCycles" :key="cycle.name" :value="cycle.name">
              {{ cycle.cycle_name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div class="p-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Appraisals List -->
      <div v-else-if="appraisals.length > 0" class="space-y-4">
        <div v-for="appraisal in appraisals" :key="appraisal.name" class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h4 class="font-medium text-gray-900">{{ appraisal.employee_name }}</h4>
                <span :class="getStatusClass(appraisal.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ appraisal.status }}
                </span>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Appraisal Cycle:</span>
                  <p class="font-medium text-gray-900">{{ appraisal.appraisal_cycle }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Period:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(appraisal.start_date) }} - {{ formatDate(appraisal.end_date) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Total Score:</span>
                  <p class="font-medium text-gray-900">{{ appraisal.total_score || 'N/A' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Rating:</span>
                  <p class="font-medium text-gray-900">{{ appraisal.rating || 'Pending' }}</p>
                </div>
              </div>
              
              <div v-if="appraisal.remarks" class="mt-3">
                <span class="text-gray-600 text-sm">Remarks:</span>
                <p class="text-gray-900 text-sm mt-1">{{ appraisal.remarks }}</p>
              </div>
            </div>
            
            <div class="ml-4 flex-shrink-0">
              <button 
                @click="viewAppraisalDetails(appraisal)"
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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <p class="text-lg font-medium text-gray-900 mb-2">No Appraisals Found</p>
        <p class="text-sm text-gray-500">Performance appraisals will appear here when available</p>
      </div>
    </div>

    <!-- Appraisal Details Modal -->
    <div v-if="selectedAppraisal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-semibold text-gray-900">Appraisal Details</h3>
          <button @click="selectedAppraisal = null" class="text-gray-400 hover:text-gray-600">
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
                  <span class="font-medium text-gray-900">{{ selectedAppraisal.employee_name }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Department:</span>
                  <span class="font-medium text-gray-900">{{ selectedAppraisal.department || 'N/A' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Designation:</span>
                  <span class="font-medium text-gray-900">{{ selectedAppraisal.designation || 'N/A' }}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Appraisal Information</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Cycle:</span>
                  <span class="font-medium text-gray-900">{{ selectedAppraisal.appraisal_cycle }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Period:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(selectedAppraisal.start_date) }} - {{ formatDate(selectedAppraisal.end_date) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Status:</span>
                  <span :class="getStatusClass(selectedAppraisal.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ selectedAppraisal.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Performance Scores -->
          <div v-if="selectedAppraisal.kra_scores && selectedAppraisal.kra_scores.length > 0">
            <h4 class="text-sm font-medium text-gray-700 mb-3">Performance Scores</h4>
            <div class="space-y-3">
              <div v-for="kra in selectedAppraisal.kra_scores" :key="kra.kra" class="border border-gray-200 rounded-lg p-3">
                <div class="flex justify-between items-center mb-2">
                  <span class="font-medium text-gray-900">{{ kra.kra }}</span>
                  <div class="flex items-center space-x-2">
                    <span class="text-sm text-gray-600">{{ kra.score }}/{{ kra.max_score }}</span>
                    <div class="w-20 bg-gray-200 rounded-full h-2">
                      <div 
                        :style="{ width: `${(kra.score / kra.max_score) * 100}%` }"
                        class="bg-blue-600 h-2 rounded-full"
                      ></div>
                    </div>
                  </div>
                </div>
                <p class="text-sm text-gray-600">{{ kra.description || 'No description available' }}</p>
              </div>
            </div>
          </div>

          <!-- Overall Rating -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
              <div>
                <span class="text-sm text-gray-600">Total Score</span>
                <p class="text-2xl font-bold text-gray-900">{{ selectedAppraisal.total_score || 'N/A' }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-600">Percentage</span>
                <p class="text-2xl font-bold text-gray-900">{{ selectedAppraisal.percentage || 'N/A' }}%</p>
              </div>
              <div>
                <span class="text-sm text-gray-600">Rating</span>
                <p class="text-2xl font-bold text-gray-900">{{ selectedAppraisal.rating || 'Pending' }}</p>
              </div>
            </div>
          </div>

          <!-- Feedback -->
          <div v-if="selectedAppraisal.feedback || selectedAppraisal.employee_feedback">
            <h4 class="text-sm font-medium text-gray-700 mb-3">Feedback</h4>
            <div class="space-y-3">
              <div v-if="selectedAppraisal.feedback" class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <h5 class="font-medium text-blue-900 mb-1">Manager Feedback</h5>
                <p class="text-sm text-blue-800">{{ selectedAppraisal.feedback }}</p>
              </div>
              <div v-if="selectedAppraisal.employee_feedback" class="bg-green-50 border border-green-200 rounded-lg p-3">
                <h5 class="font-medium text-green-900 mb-1">Employee Feedback</h5>
                <p class="text-sm text-green-800">{{ selectedAppraisal.employee_feedback }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 pt-4 border-t border-gray-200">
          <button 
            @click="selectedAppraisal = null"
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
const appraisals = ref([])
const appraisalCycles = ref([])
const selectedCycle = ref('')
const selectedAppraisal = ref(null)

// Methods
const getStatusClass = (status) => {
  const classes = {
    'Draft': 'bg-gray-100 text-gray-800',
    'Submitted': 'bg-blue-100 text-blue-800',
    'In Review': 'bg-yellow-100 text-yellow-800',
    'Completed': 'bg-green-100 text-green-800',
    'Rejected': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const loadAppraisals = async () => {
  loading.value = true
  
  try {
    const filters = {
      employee: props.employeeId
    }
    
    if (selectedCycle.value) {
      filters.appraisal_cycle = selectedCycle.value
    }
    
    const response = await call('frappe.client.get_list', {
      doctype: 'Appraisal',
      fields: [
        'name', 'employee_name', 'appraisal_cycle', 'start_date', 'end_date',
        'status', 'total_score', 'percentage', 'rating', 'remarks',
        'feedback', 'employee_feedback', 'department', 'designation'
      ],
      filters: filters,
      order_by: 'creation desc'
    })
    
    // Get detailed KRA scores for each appraisal
    const appraisalsWithScores = await Promise.all(
      response.map(async (appraisal) => {
        const kraScores = await call('frappe.client.get_list', {
          doctype: 'Appraisal KRA',
          fields: ['kra', 'description', 'score', 'max_score'],
          filters: { parent: appraisal.name }
        })
        
        return {
          ...appraisal,
          kra_scores: kraScores
        }
      })
    )
    
    appraisals.value = appraisalsWithScores
  } catch (error) {
    console.error('Error loading appraisals:', error)
    appraisals.value = []
  } finally {
    loading.value = false
  }
}

const loadAppraisalCycles = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Appraisal Cycle',
      fields: ['name', 'cycle_name', 'start_date', 'end_date'],
      filters: { status: 'Active' },
      order_by: 'creation desc'
    })
    appraisalCycles.value = response
  } catch (error) {
    console.error('Error loading appraisal cycles:', error)
    appraisalCycles.value = []
  }
}

const viewAppraisalDetails = (appraisal) => {
  selectedAppraisal.value = appraisal
}

// Initialize component
onMounted(async () => {
  await Promise.all([
    loadAppraisalCycles(),
    loadAppraisals()
  ])
})
</script>
