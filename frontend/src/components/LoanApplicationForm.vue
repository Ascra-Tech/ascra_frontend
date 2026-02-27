<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-semibold text-gray-900">Apply for Loan</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="submitApplication" class="space-y-6">
        <!-- Loan Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Loan Type *</label>
          <select v-model="loan.loan_type" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option value="">Select Loan Type</option>
            <option v-for="loanType in loanTypes" :key="loanType.name" :value="loanType.name">
              {{ loanType.loan_type_name }}
            </option>
          </select>
        </div>

        <!-- Loan Amount and Terms -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Loan Amount (₹) *</label>
            <input 
              v-model.number="loan.loan_amount" 
              type="number" 
              step="0.01" 
              min="0" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="0.00"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Repayment Period (Months) *</label>
            <input 
              v-model.number="loan.repayment_period" 
              type="number" 
              min="1" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="12"
            />
          </div>
        </div>

        <!-- EMI Calculation -->
        <div v-if="loan.loan_amount && loan.repayment_period" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <span class="text-sm font-medium text-blue-900">EMI Amount:</span>
              <p class="text-lg font-bold text-blue-600">₹{{ calculatedEMI.toFixed(2) }}</p>
            </div>
            <div>
              <span class="text-sm font-medium text-blue-900">Total Interest:</span>
              <p class="text-lg font-bold text-blue-600">₹{{ totalInterest.toFixed(2) }}</p>
            </div>
            <div>
              <span class="text-sm font-medium text-blue-900">Total Payment:</span>
              <p class="text-lg font-bold text-blue-600">₹{{ totalPayment.toFixed(2) }}</p>
            </div>
          </div>
          <p class="text-xs text-blue-700 mt-2">
            Calculated at {{ interestRate }}% interest rate per annum
          </p>
        </div>

        <!-- Loan Purpose -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Loan Purpose *</label>
          <textarea 
            v-model="loan.purpose" 
            rows="3" 
            required 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="Describe the purpose of this loan..."
          ></textarea>
        </div>

        <!-- Loan Details -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Application Date</label>
            <input 
              v-model="loan.application_date" 
              type="date" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Requested Disbursement Date</label>
            <input 
              v-model="loan.requested_disbursement_date" 
              type="date" 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        <!-- Guarantor Information -->
        <div class="space-y-4">
          <h4 class="text-sm font-medium text-gray-900">Guarantor Information</h4>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Guarantor Name *</label>
              <input 
                v-model="loan.guarantor_name" 
                type="text" 
                required 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Full name of guarantor"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Guarantor Relation *</label>
              <input 
                v-model="loan.guarantor_relation" 
                type="text" 
                required 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Father, Spouse, Friend"
              />
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Guarantor Contact *</label>
              <input 
                v-model="loan.guarantor_contact" 
                type="text" 
                required 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Mobile number or email"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Guarantor Address</label>
              <textarea 
                v-model="loan.guarantor_address" 
                rows="2" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
                placeholder="Guarantor's address"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Supporting Documents -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Supporting Documents</label>
          <FileUploadComponent 
            ref="fileUpload"
            doctype="Loan Application"
            :is-private="true"
            accept="image/*,.pdf,.doc,.docx"
            @files-changed="handleFilesChanged"
          />
          <p class="text-xs text-gray-500 mt-1">Upload ID proof, address proof, income proof, etc.</p>
        </div>

        <!-- Additional Information -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Additional Information</label>
          <textarea 
            v-model="loan.additional_info" 
            rows="3" 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="Any additional information about the loan application..."
          ></textarea>
        </div>

        <!-- Terms and Conditions -->
        <div>
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h4 class="text-sm font-medium text-gray-900 mb-2">Terms and Conditions</h4>
            <div class="space-y-2 text-sm text-gray-600">
              <p>1. I declare that all information provided in this loan application is true and correct.</p>
              <p>2. I understand that the loan approval is subject to company policy and management discretion.</p>
              <p>3. I agree to repay the loan amount as per the approved terms and conditions.</p>
              <p>4. I authorize the company to verify all information provided and conduct necessary background checks.</p>
              <p>5. I understand that the company may reject this application without providing any reason.</p>
            </div>
            
            <div class="mt-4">
              <label class="flex items-center">
                <input 
                  v-model="loan.accept_terms" 
                  type="checkbox" 
                  required 
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span class="ml-2 text-sm text-gray-700">I accept the terms and conditions</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Submit Buttons -->
        <div class="flex space-x-4 pt-4 border-t border-gray-200">
          <button 
            type="submit" 
            :disabled="loading || !loan.accept_terms"
            class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Submitting...
            </span>
            <span v-else>Submit Loan Application</span>
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
import { ref, computed, onMounted } from 'vue'
import { call } from 'frappe-ui'
import FileUploadComponent from './FileUploadComponent.vue'

const emit = defineEmits(['close', 'success'])

// Reactive data
const loading = ref(false)
const loanTypes = ref([])
const fileUpload = ref(null)
const interestRate = ref(12) // Can be made configurable

const loan = ref({
  loan_type: '',
  loan_amount: 0,
  repayment_period: 12,
  purpose: '',
  application_date: new Date().toISOString().split('T')[0],
  requested_disbursement_date: '',
  guarantor_name: '',
  guarantor_relation: '',
  guarantor_contact: '',
  guarantor_address: '',
  additional_info: '',
  accept_terms: false,
  supporting_documents: []
})

// Computed properties
const calculatedEMI = computed(() => {
  if (!loan.value.loan_amount || !loan.value.repayment_period || !interestRate.value) {
    return 0
  }
  
  const principal = loan.value.loan_amount
  const monthlyRate = interestRate.value / 12 / 100
  const months = loan.value.repayment_period
  
  // EMI calculation formula: EMI = P × r × (1 + r)^n / ((1 + r)^n - 1)
  const emi = principal * monthlyRate * Math.pow(1 + monthlyRate, months) / (Math.pow(1 + monthlyRate, months) - 1)
  
  return emi
})

const totalInterest = computed(() => {
  if (!calculatedEMI.value || !loan.value.repayment_period) {
    return 0
  }
  
  return (calculatedEMI.value * loan.value.repayment_period) - loan.value.loan_amount
})

const totalPayment = computed(() => {
  return loan.value.loan_amount + totalInterest.value
})

// Methods
const handleFilesChanged = (files) => {
  loan.value.supporting_documents = files
}

const loadLoanTypes = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Loan Type',
      fields: ['name', 'loan_type_name', 'maximum_loan_amount', 'interest_rate'],
      filters: { disabled: 0 }
    })
    loanTypes.value = response
  } catch (error) {
    console.error('Error loading loan types:', error)
  }
}

const submitApplication = async () => {
  loading.value = true
  
  try {
    // Upload files first if any
    let uploadedFiles = []
    if (loan.value.supporting_documents.length > 0) {
      uploadedFiles = await fileUpload.value.uploadFiles()
    }
    
    // Prepare loan data
    const loanData = {
      doctype: 'Loan Application',
      ...loan.value,
      emi_amount: calculatedEMI.value,
      total_interest: totalInterest.value,
      total_payment: totalPayment.value,
      supporting_documents: uploadedFiles.map(file => file.url)
    }
    
    const response = await call('frappe.client.insert', {
      doc: loanData
    })
    
    if (response.name) {
      emit('success', `Loan Application ${response.name} submitted successfully!`)
      emit('close')
    }
  } catch (error) {
    console.error('Error submitting loan application:', error)
    // You might want to show an error message to the user here
  } finally {
    loading.value = false
  }
}

// Initialize component
onMounted(async () => {
  await loadLoanTypes()
})
</script>
