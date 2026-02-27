<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200">
    <div class="p-6 border-b border-gray-200">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-900">Training Programs</h3>
        <div class="flex items-center space-x-2">
          <select v-model="selectedStatus" @change="loadTrainingPrograms" class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm">
            <option value="">All Status</option>
            <option value="Planned">Planned</option>
            <option value="Ongoing">Ongoing</option>
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

      <!-- Training Programs List -->
      <div v-else-if="trainingPrograms.length > 0" class="space-y-4">
        <div v-for="program in trainingPrograms" :key="program.name" class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h4 class="font-medium text-gray-900">{{ program.event_name }}</h4>
                <span :class="getStatusClass(program.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ program.status }}
                </span>
                <span v-if="program.is_mandatory" class="px-2 py-1 text-xs font-medium bg-orange-100 text-orange-800 rounded-full">
                  Mandatory
                </span>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Start Date:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(program.start_date) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">End Date:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(program.end_date) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Location:</span>
                  <p class="font-medium text-gray-900">{{ program.location || 'Online' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Trainer:</span>
                  <p class="font-medium text-gray-900">{{ program.trainer || 'N/A' }}</p>
                </div>
              </div>
              
              <div v-if="program.description" class="mt-3">
                <span class="text-gray-600 text-sm">Description:</span>
                <p class="text-gray-900 text-sm mt-1">{{ program.description }}</p>
              </div>
              
              <div v-if="program.skills" class="mt-3">
                <span class="text-gray-600 text-sm">Skills:</span>
                <div class="flex flex-wrap gap-1 mt-1">
                  <span v-for="skill in program.skills.split(',')" :key="skill" class="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                    {{ skill.trim() }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="ml-4 flex-shrink-0">
              <button 
                @click="viewTrainingDetails(program)"
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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332-.523 4.5-1.747M4 7l8 4 8-4"/>
        </svg>
        <p class="text-lg font-medium text-gray-900 mb-2">No Training Programs Found</p>
        <p class="text-sm text-gray-500">Training programs will appear here when available</p>
      </div>
    </div>

    <!-- Training Details Modal -->
    <div v-if="selectedProgram" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-semibold text-gray-900">Training Program Details</h3>
          <button @click="selectedProgram = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <div class="space-y-6">
          <!-- Basic Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Program Information</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Name:</span>
                  <span class="font-medium text-gray-900">{{ selectedProgram.event_name }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Type:</span>
                  <span class="font-medium text-gray-900">{{ selectedProgram.event_type || 'N/A' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Status:</span>
                  <span :class="getStatusClass(selectedProgram.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ selectedProgram.status }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Mandatory:</span>
                  <span class="font-medium text-gray-900">{{ selectedProgram.is_mandatory ? 'Yes' : 'No' }}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Schedule Information</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Start Date:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(selectedProgram.start_date) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">End Date:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(selectedProgram.end_date) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Duration:</span>
                  <span class="font-medium text-gray-900">{{ calculateDuration(selectedProgram.start_date, selectedProgram.end_date) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Location:</span>
                  <span class="font-medium text-gray-900">{{ selectedProgram.location || 'Online' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Training Details -->
          <div>
            <h4 class="text-sm font-medium text-gray-700 mb-3">Training Details</h4>
            <div class="space-y-3">
              <div v-if="selectedProgram.description" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
                <h5 class="font-medium text-gray-900 mb-1">Description</h5>
                <p class="text-sm text-gray-700">{{ selectedProgram.description }}</p>
              </div>
              
              <div v-if="selectedProgram.skills" class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <h5 class="font-medium text-blue-900 mb-1">Skills Covered</h5>
                <div class="flex flex-wrap gap-1">
                  <span v-for="skill in selectedProgram.skills.split(',')" :key="skill" class="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                    {{ skill.trim() }}
                  </span>
                </div>
              </div>
              
              <div v-if="selectedProgram.objectives" class="bg-green-50 border border-green-200 rounded-lg p-3">
                <h5 class="font-medium text-green-900 mb-1">Objectives</h5>
                <p class="text-sm text-green-700">{{ selectedProgram.objectives }}</p>
              </div>
            </div>
          </div>

          <!-- Trainer Information -->
          <div v-if="selectedProgram.trainer">
            <h4 class="text-sm font-medium text-gray-700 mb-3">Trainer Information</h4>
            <div class="bg-purple-50 border border-purple-200 rounded-lg p-3">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Trainer:</span>
                  <p class="font-medium text-gray-900">{{ selectedProgram.trainer }}</p>
                </div>
                <div v-if="selectedProgram.trainer_email">
                  <span class="text-gray-600">Email:</span>
                  <p class="font-medium text-gray-900">{{ selectedProgram.trainer_email }}</p>
                </div>
                <div v-if="selectedProgram.trainer_qualification">
                  <span class="text-gray-600">Qualification:</span>
                  <p class="font-medium text-gray-900">{{ selectedProgram.trainer_qualification }}</p>
                </div>
                <div v-if="selectedProgram.trainer_experience">
                  <span class="text-gray-600">Experience:</span>
                  <p class="font-medium text-gray-900">{{ selectedProgram.trainer_experience }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Enrollment Information -->
          <div>
            <h4 class="text-sm font-medium text-gray-700 mb-3">Enrollment Information</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="text-center bg-gray-50 border border-gray-200 rounded-lg p-3">
                <span class="text-sm text-gray-600">Total Seats</span>
                <p class="text-2xl font-bold text-gray-900">{{ selectedProgram.capacity || 'N/A' }}</p>
              </div>
              <div class="text-center bg-blue-50 border border-blue-200 rounded-lg p-3">
                <span class="text-sm text-gray-600">Enrolled</span>
                <p class="text-2xl font-bold text-blue-600">{{ selectedProgram.enrolled_count || '0' }}</p>
              </div>
              <div class="text-center bg-green-50 border border-green-200 rounded-lg p-3">
                <span class="text-sm text-gray-600">Available</span>
                <p class="text-2xl font-bold text-green-600">{{ calculateAvailableSeats(selectedProgram) }}</p>
              </div>
            </div>
          </div>

          <!-- Training Result (if completed) -->
          <div v-if="selectedProgram.status === 'Completed' && selectedProgram.training_result">
            <h4 class="text-sm font-medium text-gray-700 mb-3">Training Result</h4>
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Status:</span>
                  <p class="font-medium text-gray-900">{{ selectedProgram.training_result.status }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Score:</span>
                  <p class="font-medium text-gray-900">{{ selectedProgram.training_result.score || 'N/A' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Grade:</span>
                  <p class="font-medium text-gray-900">{{ selectedProgram.training_result.grade || 'N/A' }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Certificate:</span>
                  <p class="font-medium text-gray-900">{{ selectedProgram.training_result.certificate_issued ? 'Issued' : 'Not Issued' }}</p>
                </div>
              </div>
              <div v-if="selectedProgram.training_result.feedback" class="mt-3">
                <span class="text-gray-600 text-sm">Feedback:</span>
                <p class="text-sm text-gray-700 mt-1">{{ selectedProgram.training_result.feedback }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 pt-4 border-t border-gray-200">
          <button 
            @click="selectedProgram = null"
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
const trainingPrograms = ref([])
const selectedStatus = ref('')
const selectedProgram = ref(null)

// Methods
const getStatusClass = (status) => {
  const classes = {
    'Planned': 'bg-blue-100 text-blue-800',
    'Ongoing': 'bg-yellow-100 text-yellow-800',
    'Completed': 'bg-green-100 text-green-800',
    'Cancelled': 'bg-red-100 text-red-800'
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

const calculateDuration = (startDate, endDate) => {
  if (!startDate || !endDate) return 'N/A'
  
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diffTime = Math.abs(end - start)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  return `${diffDays} days`
}

const calculateAvailableSeats = (program) => {
  if (!program.capacity) return 'N/A'
  const enrolled = program.enrolled_count || 0
  return Math.max(0, program.capacity - enrolled)
}

const loadTrainingPrograms = async () => {
  loading.value = true
  
  try {
    const filters = {
      employee: props.employeeId
    }
    
    if (selectedStatus.value) {
      filters.status = selectedStatus.value
    }
    
    const response = await call('frappe.client.get_list', {
      doctype: 'Training Event',
      fields: [
        'name', 'event_name', 'event_type', 'start_date', 'end_date', 'status',
        'location', 'trainer', 'trainer_email', 'trainer_qualification', 'trainer_experience',
        'capacity', 'enrolled_count', 'description', 'skills', 'objectives', 'is_mandatory'
      ],
      filters: filters,
      order_by: 'start_date desc'
    })
    
    // Get training results for completed programs
    const programsWithResults = await Promise.all(
      response.map(async (program) => {
        let trainingResult = null
        
        if (program.status === 'Completed') {
          const result = await call('frappe.client.get_list', {
            doctype: 'Training Result',
            fields: ['status', 'score', 'grade', 'certificate_issued', 'feedback'],
            filters: { 
              training_event: program.name,
              employee: props.employeeId
            }
          })
          
          trainingResult = result.length > 0 ? result[0] : null
        }
        
        return {
          ...program,
          training_result: trainingResult
        }
      })
    )
    
    trainingPrograms.value = programsWithResults
  } catch (error) {
    console.error('Error loading training programs:', error)
    trainingPrograms.value = []
  } finally {
    loading.value = false
  }
}

const viewTrainingDetails = (program) => {
  selectedProgram.value = program
}

// Initialize component
onMounted(async () => {
  await loadTrainingPrograms()
})
</script>
