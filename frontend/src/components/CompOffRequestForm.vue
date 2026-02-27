<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-semibold text-gray-900">Request Compensatory Leave</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="submitRequest" class="space-y-6">
        <!-- Work Date Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Work Date *</label>
          <input 
            v-model="request.work_from_date" 
            type="date" 
            required 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p class="text-xs text-gray-500 mt-1">Select the date on which you worked extra hours</p>
        </div>

        <!-- Work Details -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Work From Time *</label>
            <input 
              v-model="request.work_from_time" 
              type="time" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Work To Time *</label>
            <input 
              v-model="request.work_to_time" 
              type="time" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        <!-- Calculated Extra Hours -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex justify-between items-center">
            <span class="text-sm font-medium text-blue-900">Extra Hours Worked:</span>
            <span class="text-lg font-bold text-blue-600">{{ calculatedExtraHours }} hours</span>
          </div>
          <p class="text-xs text-blue-700 mt-1">Calculated based on standard working hours ({{ standardWorkingHours }} hours)</p>
        </div>

        <!-- Comp-off Date -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Comp-off Date *</label>
          <input 
            v-model="request.leave_date" 
            type="date" 
            required 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p class="text-xs text-gray-500 mt-1">Date on which you want to take the compensatory leave</p>
        </div>

        <!-- Reason -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Reason for Extra Work *</label>
          <textarea 
            v-model="request.reason" 
            rows="3" 
            required 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="Please explain why you worked extra hours..."
          ></textarea>
        </div>

        <!-- Leave Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Comp-off Leave Type *</label>
          <select v-model="request.compensatory_leave_type" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option value="">Select Leave Type</option>
            <option v-for="leaveType in compOffLeaveTypes" :key="leaveType.name" :value="leaveType.name">
              {{ leaveType.leave_type_name }}
            </option>
          </select>
        </div>

        <!-- Supporting Documents -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Supporting Documents (Optional)</label>
          <FileUploadComponent 
            ref="fileUpload"
            doctype="Compensatory Leave Request"
            :is-private="true"
            accept="image/*,.pdf,.doc,.docx"
            @files-changed="handleFilesChanged"
          />
          <p class="text-xs text-gray-500 mt-1">Upload any documents that support your extra work claim</p>
        </div>

        <!-- Additional Information -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Additional Information</label>
          <textarea 
            v-model="request.additional_info" 
            rows="3" 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="Any additional information about the work or request..."
          ></textarea>
        </div>

        <!-- Submit Buttons -->
        <div class="flex space-x-4 pt-4 border-t border-gray-200">
          <button 
            type="submit" 
            :disabled="loading || calculatedExtraHours <= 0"
            class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Submitting...
            </span>
            <span v-else>Submit Comp-off Request</span>
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
import { ref, computed, onMounted, watch } from 'vue'
import { call } from 'frappe-ui'
import FileUploadComponent from './FileUploadComponent.vue'

const emit = defineEmits(['close', 'success'])

// Reactive data
const loading = ref(false)
const compOffLeaveTypes = ref([])
const fileUpload = ref(null)
const standardWorkingHours = ref(8) // Can be made configurable

const request = ref({
  work_from_date: new Date().toISOString().split('T')[0],
  work_from_time: '',
  work_to_time: '',
  leave_date: '',
  reason: '',
  compensatory_leave_type: '',
  additional_info: '',
  supporting_documents: []
})

// Computed properties
const calculatedExtraHours = computed(() => {
  if (!request.value.work_from_time || !request.value.work_to_time) {
    return 0
  }
  
  const fromTime = new Date(`2000-01-01T${request.value.work_from_time}`)
  const toTime = new Date(`2000-01-01T${request.value.work_to_time}`)
  
  let hours = (toTime - fromTime) / (1000 * 60 * 60)
  
  // Subtract standard working hours
  hours = Math.max(0, hours - standardWorkingHours.value)
  
  // Round to 2 decimal places
  return Math.round(hours * 100) / 100
})

// Methods
const handleFilesChanged = (files) => {
  request.value.supporting_documents = files
}

const loadCompOffLeaveTypes = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Leave Type',
      fields: ['name', 'leave_type_name'],
      filters: { 
        allow_compensatory_leave: 1,
        disabled: 0
      }
    })
    compOffLeaveTypes.value = response
  } catch (error) {
    console.error('Error loading comp-off leave types:', error)
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
      doctype: 'Compensatory Leave Request',
      ...request.value,
      extra_hours_worked: calculatedExtraHours.value,
      supporting_documents: uploadedFiles.map(file => file.url)
    }
    
    const response = await call('frappe.client.insert', {
      doc: requestData
    })
    
    if (response.name) {
      emit('success', `Comp-off Request ${response.name} submitted successfully!`)
      emit('close')
    }
  } catch (error) {
    console.error('Error submitting comp-off request:', error)
    // You might want to show an error message to the user here
  } finally {
    loading.value = false
  }
}

// Watch for time changes to update calculations
watch([() => request.value.work_from_time, () => request.value.work_to_time], () => {
  // This will trigger the computed property recalculation
}, { deep: true })

// Initialize component
onMounted(async () => {
  await loadCompOffLeaveTypes()
})
</script>
