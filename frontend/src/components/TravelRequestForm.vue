<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-semibold text-gray-900">Submit Travel Request</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="submitRequest" class="space-y-6">
        <!-- Basic Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Purpose of Travel *</label>
            <input 
              v-model="request.purpose" 
              type="text" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., Client Meeting, Conference, Training"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Travel Type *</label>
            <select v-model="request.travel_type" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Travel Type</option>
              <option value="Domestic">Domestic</option>
              <option value="International">International</option>
            </select>
          </div>
        </div>

        <!-- Travel Dates -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Departure Date *</label>
            <input 
              v-model="request.departure_date" 
              type="date" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Return Date *</label>
            <input 
              v-model="request.return_date" 
              type="date" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              :min="request.departure_date"
            />
          </div>
        </div>

        <!-- Duration Calculation -->
        <div v-if="request.departure_date && request.return_date" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex justify-between items-center">
            <span class="text-sm font-medium text-blue-900">Travel Duration:</span>
            <span class="text-lg font-bold text-blue-600">{{ calculatedDuration }} days</span>
          </div>
        </div>

        <!-- Destination Details -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Destination Details *</label>
          <textarea 
            v-model="request.destination" 
            rows="3" 
            required 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="City, Country, Venue details..."
          ></textarea>
        </div>

        <!-- Accommodation -->
        <div class="space-y-4">
          <h4 class="text-sm font-medium text-gray-900">Accommodation Details</h4>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Accommodation Required</label>
              <select v-model="request.accommodation_required" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="">Select Option</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            </div>
            
            <div v-if="request.accommodation_required === 'Yes'">
              <label class="block text-sm font-medium text-gray-700 mb-2">Accommodation Type</label>
              <select v-model="request.accommodation_type" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="">Select Type</option>
                <option value="Hotel">Hotel</option>
                <option value="Guest House">Guest House</option>
                <option value="Apartment">Apartment</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Transportation -->
        <div class="space-y-4">
          <h4 class="text-sm font-medium text-gray-900">Transportation Details</h4>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Transportation Mode</label>
              <select v-model="request.transportation_mode" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="">Select Mode</option>
                <option value="Flight">Flight</option>
                <option value="Train">Train</option>
                <option value="Bus">Bus</option>
                <option value="Car">Car</option>
                <option value="Taxi">Taxi</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Class/Type</label>
              <input 
                v-model="request.transportation_class" 
                type="text" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Economy, Business, AC, Non-AC"
              />
            </div>
          </div>
        </div>

        <!-- Estimated Expenses -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Estimated Expenses</label>
          <div class="space-y-3">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs text-gray-600 mb-1">Transportation</label>
                <input 
                  v-model.number="request.estimated_transportation" 
                  type="number" 
                  step="0.01" 
                  min="0" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  placeholder="0.00"
                />
              </div>
              
              <div>
                <label class="block text-xs text-gray-600 mb-1">Accommodation</label>
                <input 
                  v-model.number="request.estimated_accommodation" 
                  type="number" 
                  step="0.01" 
                  min="0" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  placeholder="0.00"
                />
              </div>
              
              <div>
                <label class="block text-xs text-gray-600 mb-1">Meals & Others</label>
                <input 
                  v-model.number="request.estimated_meals" 
                  type="number" 
                  step="0.01" 
                  min="0" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  placeholder="0.00"
                />
              </div>
            </div>
            
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="flex justify-between items-center">
                <span class="text-sm font-medium text-gray-900">Total Estimated:</span>
                <span class="text-lg font-bold text-gray-900">₹{{ totalEstimatedExpenses.toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Business Purpose -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Business Purpose *</label>
          <textarea 
            v-model="request.business_purpose" 
            rows="4" 
            required 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="Describe the business purpose and expected outcomes of this travel..."
          ></textarea>
        </div>

        <!-- Supporting Documents -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Supporting Documents (Optional)</label>
          <FileUploadComponent 
            ref="fileUpload"
            doctype="Travel Request"
            :is-private="true"
            accept="image/*,.pdf,.doc,.docx"
            @files-changed="handleFilesChanged"
          />
          <p class="text-xs text-gray-500 mt-1">Upload invitation letters, conference details, etc.</p>
        </div>

        <!-- Additional Information -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Additional Information</label>
          <textarea 
            v-model="request.additional_info" 
            rows="3" 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="Any additional information about the travel request..."
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
            <span v-else>Submit Travel Request</span>
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
import { ref, computed } from 'vue'
import { call } from 'frappe-ui'
import FileUploadComponent from './FileUploadComponent.vue'

const emit = defineEmits(['close', 'success'])

// Reactive data
const loading = ref(false)
const fileUpload = ref(null)

const request = ref({
  purpose: '',
  travel_type: '',
  departure_date: '',
  return_date: '',
  destination: '',
  accommodation_required: '',
  accommodation_type: '',
  transportation_mode: '',
  transportation_class: '',
  estimated_transportation: 0,
  estimated_accommodation: 0,
  estimated_meals: 0,
  business_purpose: '',
  additional_info: '',
  supporting_documents: []
})

// Computed properties
const calculatedDuration = computed(() => {
  if (!request.value.departure_date || !request.value.return_date) {
    return 0
  }
  
  const departure = new Date(request.value.departure_date)
  const returnDate = new Date(request.value.return_date)
  const diffTime = Math.abs(returnDate - departure)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1
  
  return diffDays
})

const totalEstimatedExpenses = computed(() => {
  return (request.value.estimated_transportation || 0) +
         (request.value.estimated_accommodation || 0) +
         (request.value.estimated_meals || 0)
})

// Methods
const handleFilesChanged = (files) => {
  request.value.supporting_documents = files
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
      doctype: 'Travel Request',
      ...request.value,
      duration: calculatedDuration.value,
      total_estimated_expenses: totalEstimatedExpenses.value,
      supporting_documents: uploadedFiles.map(file => file.url)
    }
    
    const response = await call('frappe.client.insert', {
      doc: requestData
    })
    
    if (response.name) {
      emit('success', `Travel Request ${response.name} submitted successfully!`)
      emit('close')
    }
  } catch (error) {
    console.error('Error submitting travel request:', error)
    // You might want to show an error message to the user here
  } finally {
    loading.value = false
  }
}
</script>
