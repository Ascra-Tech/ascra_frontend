<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-semibold text-gray-900">Request Attendance Regularization</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="submitRequest" class="space-y-6">
        <!-- Attendance Date -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Attendance Date *</label>
          <input 
            v-model="request.attendance_date" 
            type="date" 
            required 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <!-- Current vs Requested Status -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Current Status</label>
            <div class="p-3 bg-gray-50 rounded-lg border border-gray-200">
              <p class="text-sm text-gray-600">Current attendance status will be shown here</p>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Requested Status *</label>
            <select v-model="request.status" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Status</option>
              <option value="Present">Present</option>
              <option value="Absent">Absent</option>
              <option value="Half Day">Half Day</option>
              <option value="Work From Home">Work From Home</option>
              <option value="On Leave">On Leave</option>
            </select>
          </div>
        </div>

        <!-- Time Details -->
        <div v-if="request.status === 'Present' || request.status === 'Half Day'" class="space-y-4">
          <h4 class="text-sm font-medium text-gray-900">Time Details</h4>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Check In Time</label>
              <input 
                v-model="request.in_time" 
                type="time" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Check Out Time</label>
              <input 
                v-model="request.out_time" 
                type="time" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        <!-- Reason for Regularization -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Reason for Regularization *</label>
          <textarea 
            v-model="request.reason" 
            rows="4" 
            required 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="Please explain why this attendance needs to be regularized..."
          ></textarea>
        </div>

        <!-- Supporting Documents -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Supporting Documents (Optional)</label>
          <FileUploadComponent 
            ref="fileUpload"
            doctype="Attendance Request"
            :is-private="true"
            accept="image/*,.pdf,.doc,.docx"
            @files-changed="handleFilesChanged"
          />
        </div>

        <!-- Shift Details -->
        <div>
          <h4 class="text-sm font-medium text-gray-900 mb-3">Shift Details</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Shift Type</label>
              <select v-model="request.shift_type" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="">Select Shift Type</option>
                <option v-for="shift in shiftTypes" :key="shift.name" :value="shift.name">
                  {{ shift.shift_name }}
                </option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Working Hours</label>
              <input 
                v-model="request.working_hours" 
                type="text" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., 9:00 AM - 6:00 PM"
              />
            </div>
          </div>
        </div>

        <!-- Additional Information -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Additional Information</label>
          <textarea 
            v-model="request.additional_info" 
            rows="3" 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="Any additional information that might help in processing this request..."
          ></textarea>
        </div>

        <!-- Submit Buttons -->
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
            <span v-else>Submit Regularization Request</span>
          </button>
          <button 
            type="button" 
            @click="$emit('close')"
            class="px-6 py-3 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors font-medium"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { call } from 'frappe-ui'
import FileUploadComponent from './FileUploadComponent.vue'

const emit = defineEmits(['close', 'success'])

// Reactive data
const loading = ref(false)
const shiftTypes = ref([])
const fileUpload = ref(null)

const request = ref({
  attendance_date: new Date().toISOString().split('T')[0],
  status: '',
  in_time: '',
  out_time: '',
  reason: '',
  shift_type: '',
  working_hours: '',
  additional_info: '',
  supporting_documents: []
})

// Methods
const handleFilesChanged = (files) => {
  request.value.supporting_documents = files
}

const loadShiftTypes = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Shift Type',
      fields: ['name', 'shift_name'],
      filters: { disabled: 0 }
    })
    shiftTypes.value = response
  } catch (error) {
    console.error('Error loading shift types:', error)
  }
}

const submitRequest = async () => {
  loading.value = true
  
  try {
    // Upload files first if any
    let uploadedFiles = []
    if (request.value.supporting_documents.length > 0) {
      uploadedFiles = await fileUpload.value.uploadFiles()
    }
    
    // Prepare request data
    const requestData = {
      doctype: 'Attendance Request',
      ...request.value,
      supporting_documents: uploadedFiles.map(file => file.url)
    }
    
    const response = await call('frappe.client.insert', {
      doc: requestData
    })
    
    if (response.name) {
      emit('success', `Attendance Request ${response.name} submitted successfully!`)
      emit('close')
    }
  } catch (error) {
    console.error('Error submitting attendance request:', error)
    // You might want to show an error message to the user here
  } finally {
    loading.value = false
  }
}

// Initialize component
onMounted(async () => {
  await loadShiftTypes()
})
</script>
