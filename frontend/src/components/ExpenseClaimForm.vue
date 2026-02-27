<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-semibold text-gray-900">Submit Expense Claim</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="submitClaim" class="space-y-6">
        <!-- Basic Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Expense Type *</label>
            <select v-model="claim.expense_type" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Expense Type</option>
              <option v-for="type in expenseTypes" :key="type.name" :value="type.name">
                {{ type.expense_type_name }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Posting Date *</label>
            <input v-model="claim.posting_date" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
          </div>
        </div>

        <!-- Employee Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Expense Approver *</label>
            <select v-model="claim.expense_approver" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Approver</option>
              <option v-for="approver in approvers" :key="approver.name" :value="approver.name">
                {{ approver.employee_name }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Company *</label>
            <select v-model="claim.company" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Company</option>
              <option v-for="company in companies" :key="company.name" :value="company.name">
                {{ company.company_name }}
              </option>
            </select>
          </div>
        </div>

        <!-- Remarks -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Remarks</label>
          <textarea v-model="claim.remarks" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" placeholder="Additional remarks about this expense claim..."></textarea>
        </div>

        <!-- Expense Items -->
        <div>
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-lg font-medium text-gray-900">Expense Items</h4>
            <button type="button" @click="addExpenseItem" class="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
              + Add Item
            </button>
          </div>

          <div v-if="claim.expenses.length === 0" class="text-center py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
            <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <p class="text-gray-500">No expense items added</p>
            <p class="text-sm text-gray-400 mt-1">Click "Add Item" to add your first expense</p>
          </div>

          <div v-else class="space-y-4">
            <div v-for="(item, index) in claim.expenses" :key="index" class="border border-gray-200 rounded-lg p-4 bg-gray-50">
              <div class="flex justify-between items-start mb-4">
                <h5 class="font-medium text-gray-900">Item {{ index + 1 }}</h5>
                <button type="button" @click="removeExpenseItem(index)" class="text-red-500 hover:text-red-700">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Expense Date *</label>
                  <input v-model="item.expense_date" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Amount *</label>
                  <input v-model.number="item.amount" type="number" step="0.01" min="0" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm" placeholder="0.00">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Description *</label>
                  <input v-model="item.description" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm" placeholder="Expense description">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Receipt</label>
                  <div class="relative">
                    <input 
                      type="file" 
                      @change="(e) => handleFileUpload(e, index)"
                      accept="image/*,.pdf"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm file:mr-4 file:py-1 file:px-2 file:rounded file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                    />
                    <div v-if="item.receipt_url" class="mt-2">
                      <a :href="item.receipt_url" target="_blank" class="text-xs text-blue-600 hover:text-blue-800 underline">View Receipt</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Total Amount -->
        <div v-if="totalAmount > 0" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex justify-between items-center">
            <span class="text-lg font-medium text-blue-900">Total Claim Amount:</span>
            <span class="text-2xl font-bold text-blue-600">₹{{ totalAmount.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Submit Buttons -->
        <div class="flex space-x-4 pt-4 border-t border-gray-200">
          <button 
            type="submit" 
            :disabled="loading || claim.expenses.length === 0"
            class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Submitting...
            </span>
            <span v-else>Submit Expense Claim</span>
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

const emit = defineEmits(['close', 'success'])

// Reactive data
const loading = ref(false)
const expenseTypes = ref([])
const approvers = ref([])
const companies = ref([])

const claim = ref({
  expense_type: '',
  posting_date: new Date().toISOString().split('T')[0],
  expense_approver: '',
  company: '',
  remarks: '',
  expenses: []
})

// Computed properties
const totalAmount = computed(() => {
  return claim.value.expenses.reduce((total, item) => total + (item.amount || 0), 0)
})

// Methods
const addExpenseItem = () => {
  claim.value.expenses.push({
    expense_date: new Date().toISOString().split('T')[0],
    amount: 0,
    description: '',
    receipt_url: ''
  })
}

const removeExpenseItem = (index) => {
  claim.value.expenses.splice(index, 1)
}

const handleFileUpload = async (event, index) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('doctype', 'Expense Claim')
    formData.append('is_private', '1')

    const response = await call('/api/method/upload_file', formData)
    
    if (response.message === 'OK' && response.file_url) {
      claim.value.expenses[index].receipt_url = response.file_url
    }
  } catch (error) {
    console.error('Error uploading file:', error)
    // You might want to show an error message to the user here
  }
}

const loadExpenseTypes = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Expense Claim Type',
      fields: ['name', 'expense_type_name'],
      filters: { disabled: 0 }
    })
    expenseTypes.value = response
  } catch (error) {
    console.error('Error loading expense types:', error)
  }
}

const loadApprovers = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Employee',
      fields: ['name', 'employee_name'],
      filters: { status: 'Active' }
    })
    approvers.value = response
  } catch (error) {
    console.error('Error loading approvers:', error)
  }
}

const loadCompanies = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Company',
      fields: ['name', 'company_name']
    })
    companies.value = response
  } catch (error) {
    console.error('Error loading companies:', error)
  }
}

const submitClaim = async () => {
  loading.value = true
  
  try {
    const response = await call('frappe.client.insert', {
      doc: {
        doctype: 'Expense Claim',
        ...claim.value
      }
    })
    
    if (response.name) {
      emit('success', `Expense Claim ${response.name} submitted successfully!`)
      emit('close')
    }
  } catch (error) {
    console.error('Error submitting expense claim:', error)
    // You might want to show an error message to the user here
  } finally {
    loading.value = false
  }
}

// Initialize component
onMounted(async () => {
  await Promise.all([
    loadExpenseTypes(),
    loadApprovers(),
    loadCompanies()
  ])
})
</script>
