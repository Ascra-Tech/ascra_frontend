<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200">
    <div class="p-6 border-b border-gray-200">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-900">Employee Grievances</h3>
        <button 
          @click="showGrievanceForm = true"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
        >
          + New Grievance
        </button>
      </div>
    </div>

    <div class="p-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Grievances List -->
      <div v-else-if="grievances.length > 0" class="space-y-4">
        <div v-for="grievance in grievances" :key="grievance.name" class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h4 class="font-medium text-gray-900">{{ grievance.subject }}</h4>
                <span :class="getStatusClass(grievance.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ grievance.status }}
                </span>
                <span :class="getPriorityClass(grievance.priority)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ grievance.priority }}
                </span>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Category:</span>
                  <p class="font-medium text-gray-900">{{ grievance.category }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Date:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(grievance.creation) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Expected Resolution:</span>
                  <p class="font-medium text-gray-900">{{ formatDate(grievance.expected_resolution_date) }}</p>
                </div>
                <div>
                  <span class="text-gray-600">Assigned To:</span>
                  <p class="font-medium text-gray-900">{{ grievance.assigned_to || 'Unassigned' }}</p>
                </div>
              </div>
              
              <div class="mt-3">
                <span class="text-gray-600 text-sm">Description:</span>
                <p class="text-gray-900 text-sm mt-1 line-clamp-2">{{ grievance.description }}</p>
              </div>
              
              <div v-if="grievance.resolution_details" class="mt-3">
                <span class="text-gray-600 text-sm">Resolution:</span>
                <p class="text-gray-900 text-sm mt-1">{{ grievance.resolution_details }}</p>
              </div>
            </div>
            
            <div class="ml-4 flex-shrink-0">
              <button 
                @click="viewGrievanceDetails(grievance)"
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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.651 2.032-3 3.772-3s3.223 1.349 3.772 3c.549 1.651 2.032 3 3.772 3s3.223-1.349 3.772-3c.549-1.651 2.032-3 3.772-3s-3.223-1.349-3.772-3z"/>
        </svg>
        <p class="text-lg font-medium text-gray-900 mb-2">No Grievances Found</p>
        <p class="text-sm text-gray-500">Submit a grievance to report any workplace issues</p>
      </div>
    </div>

    <!-- Grievance Form Modal -->
    <div v-if="showGrievanceForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-semibold text-gray-900">Submit Grievance</h3>
          <button @click="showGrievanceForm = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="submitGrievance" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Subject *</label>
            <input 
              v-model="grievanceForm.subject" 
              type="text" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Brief description of the issue"
            />
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Category *</label>
              <select v-model="grievanceForm.category" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="">Select Category</option>
                <option value="Work Environment">Work Environment</option>
                <option value="Harassment">Harassment</option>
                <option value="Discrimination">Discrimination</option>
                <option value="Salary & Benefits">Salary & Benefits</option>
                <option value="Workload">Workload</option>
                <option value="Policy & Procedures">Policy & Procedures</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Priority *</label>
              <select v-model="grievanceForm.priority" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="">Select Priority</option>
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description *</label>
            <textarea 
              v-model="grievanceForm.description" 
              rows="4" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
              placeholder="Detailed description of the grievance..."
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Expected Resolution Date *</label>
            <input 
              v-model="grievanceForm.expected_resolution_date" 
              type="date" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Suggested Resolution (Optional)</label>
            <textarea 
              v-model="grievanceForm.suggested_resolution" 
              rows="3" 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
              placeholder="How would you like this issue to be resolved?"
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Supporting Documents (Optional)</label>
            <FileUploadComponent 
              ref="fileUpload"
              doctype="Employee Grievance"
              :is-private="true"
              accept="image/*,.pdf,.doc,.docx"
              @files-changed="handleFilesChanged"
            />
            <p class="text-xs text-gray-500 mt-1">Upload any relevant documents to support your grievance</p>
          </div>
          
          <div class="flex space-x-4 pt-4 border-t border-gray-200">
            <button 
              type="submit" 
              :disabled="loading"
              class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              <span v-if="loading" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Submitting...
              </span>
              <span v-else>Submit Grievance</span>
            </button>
            <button 
              type="button" 
              @click="showGrievanceForm = false"
              class="px-6 py-3 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors font-medium"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Grievance Details Modal -->
    <div v-if="selectedGrievance" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-3xl mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-semibold text-gray-900">Grievance Details</h3>
          <button @click="selectedGrievance = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <div class="space-y-6">
          <!-- Basic Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Grievance Information</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Subject:</span>
                  <span class="font-medium text-gray-900">{{ selectedGrievance.subject }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Category:</span>
                  <span class="font-medium text-gray-900">{{ selectedGrievance.category }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Priority:</span>
                  <span :class="getPriorityClass(selectedGrievance.priority)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ selectedGrievance.priority }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Status:</span>
                  <span :class="getStatusClass(selectedGrievance.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ selectedGrievance.status }}
                  </span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Timeline Information</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Created:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(selectedGrievance.creation) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Expected Resolution:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(selectedGrievance.expected_resolution_date) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Assigned To:</span>
                  <span class="font-medium text-gray-900">{{ selectedGrievance.assigned_to || 'Unassigned' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Last Updated:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(selectedGrievance.modified) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div>
            <h4 class="text-sm font-medium text-gray-700 mb-2">Description</h4>
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <p class="text-sm text-gray-700">{{ selectedGrievance.description }}</p>
            </div>
          </div>

          <!-- Suggested Resolution -->
          <div v-if="selectedGrievance.suggested_resolution">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Suggested Resolution</h4>
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p class="text-sm text-blue-700">{{ selectedGrievance.suggested_resolution }}</p>
            </div>
          </div>

          <!-- Resolution Details -->
          <div v-if="selectedGrievance.resolution_details">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Resolution Details</h4>
            <div class="bg-green-50 border border-green-200 rounded-lg p-3">
              <p class="text-sm text-green-700">{{ selectedGrievance.resolution_details }}</p>
            </div>
          </div>

          <!-- Comments/Updates -->
          <div v-if="selectedGrievance.comments && selectedGrievance.comments.length > 0">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Comments & Updates</h4>
            <div class="space-y-3">
              <div v-for="comment in selectedGrievance.comments" :key="comment.name" class="border border-gray-200 rounded-lg p-3">
                <div class="flex justify-between items-start mb-2">
                  <span class="font-medium text-gray-900">{{ comment.commented_by }}</span>
                  <span class="text-xs text-gray-500">{{ formatDate(comment.creation) }}</span>
                </div>
                <p class="text-sm text-gray-700">{{ comment.comment }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 pt-4 border-t border-gray-200">
          <button 
            @click="selectedGrievance = null"
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
import FileUploadComponent from './FileUploadComponent.vue'

const props = defineProps({
  employeeId: {
    type: String,
    required: true
  }
})

// Reactive data
const loading = ref(false)
const grievances = ref([])
const showGrievanceForm = ref(false)
const selectedGrievance = ref(null)
const fileUpload = ref(null)

const grievanceForm = ref({
  subject: '',
  category: '',
  priority: '',
  description: '',
  expected_resolution_date: '',
  suggested_resolution: '',
  supporting_documents: []
})

// Methods
const getStatusClass = (status) => {
  const classes = {
    'Open': 'bg-yellow-100 text-yellow-800',
    'In Progress': 'bg-blue-100 text-blue-800',
    'Resolved': 'bg-green-100 text-green-800',
    'Closed': 'bg-gray-100 text-gray-800',
    'Rejected': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPriorityClass = (priority) => {
  const classes = {
    'Low': 'bg-gray-100 text-gray-800',
    'Medium': 'bg-blue-100 text-blue-800',
    'High': 'bg-orange-100 text-orange-800',
    'Critical': 'bg-red-100 text-red-800'
  }
  return classes[priority] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const handleFilesChanged = (files) => {
  grievanceForm.value.supporting_documents = files
}

const loadGrievances = async () => {
  loading.value = true
  
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Employee Grievance',
      fields: [
        'name', 'subject', 'category', 'priority', 'status', 'description',
        'creation', 'modified', 'expected_resolution_date', 'assigned_to',
        'suggested_resolution', 'resolution_details'
      ],
      filters: { employee: props.employeeId },
      order_by: 'creation desc'
    })
    
    // Get comments for each grievance
    const grievancesWithComments = await Promise.all(
      response.map(async (grievance) => {
        const comments = await call('frappe.client.get_list', {
          doctype: 'Comment',
          fields: ['name', 'comment', 'commented_by', 'creation'],
          filters: { 
            reference_doctype: 'Employee Grievance',
            reference_name: grievance.name
          },
          order_by: 'creation asc'
        })
        
        return {
          ...grievance,
          comments: comments
        }
      })
    )
    
    grievances.value = grievancesWithComments
  } catch (error) {
    console.error('Error loading grievances:', error)
    grievances.value = []
  } finally {
    loading.value = false
  }
}

const submitGrievance = async () => {
  loading.value = true
  
  try {
    // Upload files first if any
    let uploadedFiles = []
    if (grievanceForm.value.supporting_documents.length > 0) {
      uploadedFiles = await fileUpload.value.uploadFiles()
    }
    
    // Prepare grievance data
    const grievanceData = {
      doctype: 'Employee Grievance',
      ...grievanceForm,
      employee: props.employeeId,
      supporting_documents: uploadedFiles.map(file => file.url)
    }
    
    const response = await call('frappe.client.insert', {
      doc: grievanceData
    })
    
    if (response.name) {
      showGrievanceForm.value = false
      // Reset form
      grievanceForm.value = {
        subject: '',
        category: '',
        priority: '',
        description: '',
        expected_resolution_date: '',
        suggested_resolution: '',
        supporting_documents: []
      }
      
      // Reload grievances list
      await loadGrievances()
      
      // Show success message
      alert('Grievance submitted successfully!')
    }
  } catch (error) {
    console.error('Error submitting grievance:', error)
    alert('Failed to submit grievance. Please try again.')
  } finally {
    loading.value = false
  }
}

const viewGrievanceDetails = (grievance) => {
  selectedGrievance.value = grievance
}

// Initialize component
onMounted(async () => {
  await loadGrievances()
})
</script>
