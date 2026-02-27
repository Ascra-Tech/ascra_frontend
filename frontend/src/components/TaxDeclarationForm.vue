<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-semibold text-gray-900">Submit Tax Declaration</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="submitDeclaration" class="space-y-6">
        <!-- Financial Year -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Financial Year *</label>
            <select v-model="declaration.financial_year" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Financial Year</option>
              <option v-for="year in financialYears" :key="year.name" :value="year.name">
                {{ year.year_name }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Declaration Type *</label>
            <select v-model="declaration.declaration_type" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Type</option>
              <option value="Section 80C">Section 80C</option>
              <option value="Section 80D">Section 80D</option>
              <option value="Section 80E">Section 80E</option>
              <option value="Section 80G">Section 80G</option>
              <option value="Section 80GG">Section 80GG</option>
              <option value="Section 80TTA">Section 80TTA</option>
              <option value="Section 80TTB">Section 80TTB</option>
              <option value="Section 80CC">Section 80CC</option>
              <option value="Section 80CCD">Section 80CCD</option>
              <option value="Section 80CCE">Section 80CCE</option>
              <option value="Section 80CCF">Section 80CCF</option>
              <option value="Section 80CCG">Section 80CCG</option>
              <option value="Section 80CCH">Section 80CCH</option>
              <option value="Section 80CC(1)">Section 80CC(1)</option>
              <option value="Section 80CC(2)">Section 80CC(2)</option>
              <option value="Section 80CC(3)">Section 80CC(3)</option>
              <option value="Section 80CC(4)">Section 80CC(4)</option>
              <option value="Section 80CC(5)">Section 80CC(5)</option>
              <option value="Section 80CC(6)">Section 80CC(6)</option>
              <option value="Section 80CC(7)">Section 80CC(7)</option>
              <option value="Section 80CC(8)">Section 80CC(8)</option>
              <option value="Section 80CC(9)">Section 80CC(9)</option>
              <option value="Section 80CC(10)">Section 80CC(10)</option>
              <option value="Section 80CC(11)">Section 80CC(11)</option>
              <option value="Section 80CC(12)">Section 80CC(12)</option>
              <option value="Section 80CC(13)">Section 80CC(13)</option>
              <option value="Section 80CC(14)">Section 80CC(14)</option>
              <option value="Section 80CC(15)">Section 80CC(15)</option>
              <option value="Section 80CC(16)">Section 80CC(16)</option>
              <option value="Section 80CC(17)">Section 80CC(17)</option>
              <option value="Section 80CC(18)">Section 80CC(18)</option>
              <option value="Section 80CC(19)">Section 80CC(19)</option>
              <option value="Section 80CC(20)">Section 80CC(20)</option>
              <option value="Section 80CC(21)">Section 80CC(21)</option>
              <option value="Section 80CC(22)">Section 80CC(22)</option>
              <option value="Section 80CC(23)">Section 80CC(23)</option>
              <option value="Section 80CC(24)">Section 80CC(24)</option>
              <option value="Section 80CC(25)">Section 80CC(25)</option>
              <option value="Section 80CC(26)">Section 80CC(26)</option>
              <option value="Section 80CC(27)">Section 80CC(27)</option>
              <option value="Section 80CC(28)">Section 80CC(28)</option>
              <option value="Section 80CC(29)">Section 80CC(29)</option>
              <option value="Section 80CC(30)">Section 80CC(30)</option>
              <option value="Section 80CC(31)">Section 80CC(31)</option>
              <option value="Section 80CC(32)">Section 80CC(32)</option>
              <option value="Section 80CC(33)">Section 80CC(33)</option>
              <option value="Section 80CC(34)">Section 80CC(34)</option>
              <option value="Section 80CC(35)">Section 80CC(35)</option>
              <option value="Section 80CC(36)">Section 80CC(36)</option>
              <option value="Section 80CC(37)">Section 80CC(37)</option>
              <option value="Section 80CC(38)">Section 80CC(38)</option>
              <option value="Section 80CC(39)">Section 80CC(39)</option>
              <option value="Section 80CC(40)">Section 80CC(40)</option>
              <option value="Section 80CC(41)">Section 80CC(41)</option>
              <option value="Section 80CC(42)">Section 80CC(42)</option>
              <option value="Section 80CC(43)">Section 80CC(43)</option>
              <option value="Section 80CC(44)">Section 80CC(44)</option>
              <option value="Section 80CC(45)">Section 80CC(45)</option>
              <option value="Section 80CC(46)">Section 80CC(46)</option>
              <option value="Section 80CC(47)">Section 80CC(47)</option>
              <option value="Section 80CC(48)">Section 80CC(48)</option>
              <option value="Section 80CC(49)">Section 80CC(49)</option>
              <option value="Section 80CC(50)">Section 80CC(50)</option>
              <option value="Section 80CC(51)">Section 80CC(51)</option>
              <option value="Section 80CC(52)">Section 80CC(52)</option>
              <option value="Section 80CC(53)">Section 80CC(53)</option>
              <option value="Section 80CC(54)">Section 80CC(54)</option>
              <option value="Section 80CC(55)">Section 80CC(55)</option>
              <option value="Section 80CC(56)">Section 80CC(56)</option>
              <option value="Section 80CC(57)">Section 80CC(57)</option>
              <option value="Section 80CC(58)">Section 80CC(58)</option>
              <option value="Section 80CC(59)">Section 80CC(59)</option>
              <option value="Section 80CC(60)">Section 80CC(60)</option>
              <option value="Section 80CC(61)">Section 80CC(61)</option>
              <option value="Section 80CC(62)">Section 80CC(62)</option>
              <option value="Section 80CC(63)">Section 80CC(63)</option>
              <option value="Section 80CC(64)">Section 80CC(64)</option>
              <option value="Section 80CC(65)">Section 80CC(65)</option>
              <option value="Section 80CC(66)">Section 80CC(66)</option>
              <option value="Section 80CC(67)">Section 80CC(67)</option>
              <option value="Section 80CC(68)">Section 80CC(68)</option>
              <option value="Section 80CC(69)">Section 80CC(69)</option>
              <option value="Section 80CC(70)">Section 80CC(70)</option>
              <option value="Section 80CC(71)">Section 80CC(71)</option>
              <option value="Section 80CC(72)">Section 80CC(72)</option>
              <option value="Section 80CC(73)">Section 80CC(73)</option>
              <option value="Section 80CC(74)">Section 80CC(74)</option>
              <option value="Section 80CC(75)">Section 80CC(75)</option>
              <option value="Section 80CC(76)">Section 80CC(76)</option>
              <option value="Section 80CC(77)">Section 80CC(77)</option>
              <option value="Section 80CC(78)">Section 80CC(78)</option>
              <option value="Section 80CC(79)">Section 80CC(79)</option>
              <option value="Section 80CC(80)">Section 80CC(80)</option>
              <option value="Section 80CC(81)">Section 80CC(81)</option>
              <option value="Section 80CC(82)">Section 80CC(82)</option>
              <option value="Section 80CC(83)">Section 80CC(83)</option>
              <option value="Section 80CC(84)">Section 80CC(84)</option>
              <option value="Section 80CC(85)">Section 80CC(85)</option>
              <option value="Section 80CC(86)">Section 80CC(86)</option>
              <option value="Section 80CC(87)">Section 80CC(87)</option>
              <option value="Section 80CC(88)">Section 80CC(88)</option>
              <option value="Section 80CC(89)">Section 80CC(89)</option>
              <option value="Section 80CC(90)">Section 80CC(90)</option>
              <option value="Section 80CC(91)">Section 80CC(91)</option>
              <option value="Section 80CC(92)">Section 80CC(92)</option>
              <option value="Section 80CC(93)">Section 80CC(93)</option>
              <option value="Section 80CC(94)">Section 80CC(94)</option>
              <option value="Section 80CC(95)">Section 80CC(95)</option>
              <option value="Section 80CC(96)">Section 80CC(96)</option>
              <option value="Section 80CC(97)">Section 80CC(97)</option>
              <option value="Section 80CC(98)">Section 80CC(98)</option>
              <option value="Section 80CC(99)">Section 80CC(99)</option>
              <option value="Section 80CC(100)">Section 80CC(100)</option>
              <option value="Section 80CC(101)">Section 80CC(101)</option>
              <option value="Section 80CC(102)">Section 80CC(102)</option>
              <option value="Section 80CC(103)">Section 80CC(103)</option>
              <option value="Section 80CC(104)">Section 80CC(104)</option>
              <option value="Section 80CC(105)">Section 80CC(105)</option>
              <option value="Section 80CC(106)">Section 80CC(106)</option>
              <option value="Section 80CC(107)">Section 80CC(107)</option>
              <option value="Section 80CC(108)">Section 80CC(108)</option>
              <option value="Section 80CC(109)">Section 80CC(109)</option>
              <option value="Section 80CC(110)">Section 80CC(110)</option>
              <option value="Section 80CC(111)">Section 80CC(111)</option>
              <option value="Section 80CC(112)">Section 80CC(112)</option>
              <option value="Section 80CC(113)">Section 80CC(113)</option>
              <option value="Section 80CC(114)">Section 80CC(114)</option>
              <option value="Section 80CC(115)">Section 80CC(115)</option>
              <option value="Section 80CC(116)">Section 80CC(116)</option>
              <option value="Section 80CC(117)">Section 80CC(117)</option>
              <option value="Section 80CC(118)">Section 80CC(118)</option>
              <option value="Section 80CC(119)">Section 80CC(119)</option>
              <option value="Section 80CC(120)">Section 80CC(120)</option>
              <option value="Section 80CC(121)">Section 80CC(121)</option>
              <option value="Section 80CC(122)">Section 80CC(122)</option>
              <option value="Section 80CC(123)">Section 80CC(123)</option>
              <option value="Section 80CC(124)">Section 80CC(124)</option>
              <option value="Section 80CC(125)">Section 80CC(125)</option>
              <option value="Section 80CC(126)">Section 80CC(126)</option>
              <option value="Section 80CC(127)">Section 80CC(127)</option>
              <option value="Section 80CC(128)">Section 80CC(128)</option>
              <option value="Section 80CC(129)">Section 80CC(129)</option>
              <option value="Section 80CC(130)">Section 80CC(130)</option>
              <option value="Section 80CC(131)">Section 80CC(131)</option>
              <option value="Section 80CC(132)">Section 80CC(132)</option>
              <option value="Section 80CC(133)">Section 80CC(133)</option>
              <option value="Section 80CC(134)">Section 80CC(134)</option>
              <option value="Section 80CC(135)">Section 80CC(135)</option>
              <option value="Section 80CC(136)">Section 80CC(136)</option>
              <option value="Section 80CC(137)">Section 80CC(137)</option>
              <option value="Section 80CC(138)">Section 80CC(138)</option>
              <option value="Section 80CC(139)">Section 80CC(139)</option>
              <option value="Section 80CC(140)">Section 80CC(140)</option>
              <option value="Section 80CC(141)">Section 80CC(141)</option>
              <option value="Section 80CC(142)">Section 80CC(142)</option>
              <option value="Section 80CC(143)">Section 80CC(143)</option>
              <option value="Section 80CC(144)">Section 80CC(144)</option>
              <option value="Section 80CC(145)">Section 80CC(145)</option>
              <option value="Section 80CC(146)">Section 80CC(146)</option>
              <option value="Section 80CC(147)">Section 80CC(147)</option>
              <option value="Section 80CC(148)">Section 80CC(148)</option>
              <option value="Section 80CC(149)">Section 80CC(149)</option>
              <option value="Section 80CC(150)">Section 80CC(150)</option>
            </select>
          </div>
        </div>

        <!-- Declaration Items -->
        <div>
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-lg font-medium text-gray-900">Declaration Items</h4>
            <button type="button" @click="addDeclarationItem" class="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
              + Add Item
            </button>
          </div>

          <div v-if="declaration.declaration_items.length === 0" class="text-center py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
            <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <p class="text-gray-500">No declaration items added</p>
            <p class="text-sm text-gray-400 mt-1">Click "Add Item" to add your first declaration item</p>
          </div>

          <div v-else class="space-y-4">
            <div v-for="(item, index) in declaration.declaration_items" :key="index" class="border border-gray-200 rounded-lg p-4 bg-gray-50">
              <div class="flex justify-between items-start mb-4">
                <h5 class="font-medium text-gray-900">Item {{ index + 1 }}</h5>
                <button type="button" @click="removeDeclarationItem(index)" class="text-red-500 hover:text-red-700">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Description *</label>
                  <input v-model="item.description" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm" placeholder="Description of the investment/expense">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Amount *</label>
                  <input v-model.number="item.amount" type="number" step="0.01" min="0" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm" placeholder="0.00">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Section *</label>
                  <input v-model="item.section" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm" placeholder="e.g., 80C, 80D">
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Date *</label>
                  <input v-model="item.date" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm">
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Total Amount -->
        <div v-if="totalAmount > 0" class="bg-green-50 border border-green-200 rounded-lg p-4">
          <div class="flex justify-between items-center">
            <span class="text-lg font-medium text-green-900">Total Declaration Amount:</span>
            <span class="text-2xl font-bold text-green-600">₹{{ totalAmount.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Supporting Documents -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Supporting Documents (Optional)</label>
          <FileUploadComponent 
            ref="fileUpload"
            doctype="Employee Tax Exemption Declaration"
            :is-private="true"
            accept="image/*,.pdf,.doc,.docx"
            @files-changed="handleFilesChanged"
          />
          <p class="text-xs text-gray-500 mt-1">Upload receipts, certificates, or other supporting documents</p>
        </div>

        <!-- Remarks -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Remarks</label>
          <textarea 
            v-model="declaration.remarks" 
            rows="3" 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" 
            placeholder="Additional remarks about this tax declaration..."
          ></textarea>
        </div>

        <!-- Submit Buttons -->
        <div class="flex space-x-4 pt-4 border-t border-gray-200">
          <button 
            type="submit" 
            :disabled="loading || declaration.declaration_items.length === 0"
            class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Submitting...
            </span>
            <span v-else>Submit Tax Declaration</span>
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
const financialYears = ref([])
const fileUpload = ref(null)

const declaration = ref({
  financial_year: '',
  declaration_type: '',
  remarks: '',
  declaration_items: [],
  supporting_documents: []
})

// Computed properties
const totalAmount = computed(() => {
  return declaration.value.declaration_items.reduce((total, item) => total + (item.amount || 0), 0)
})

// Methods
const addDeclarationItem = () => {
  declaration.value.declaration_items.push({
    description: '',
    amount: 0,
    section: '',
    date: new Date().toISOString().split('T')[0]
  })
}

const removeDeclarationItem = (index) => {
  declaration.value.declaration_items.splice(index, 1)
}

const handleFilesChanged = (files) => {
  declaration.value.supporting_documents = files
}

const loadFinancialYears = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Financial Year',
      fields: ['name', 'year_name'],
      filters: { disabled: 0 },
      order_by: 'year_name desc'
    })
    financialYears.value = response
  } catch (error) {
    console.error('Error loading financial years:', error)
  }
}

const submitDeclaration = async () => {
  loading.value = true
  
  try {
    // Upload files first if any
    let uploadedFiles = []
    if (declaration.value.supporting_documents.length > 0) {
      uploadedFiles = await fileUpload.value.uploadFiles()
    }
    
    // Prepare declaration data
    const declarationData = {
      doctype: 'Employee Tax Exemption Declaration',
      ...declaration.value,
      total_amount: totalAmount.value,
      supporting_documents: uploadedFiles.map(file => file.url)
    }
    
    const response = await call('frappe.client.insert', {
      doc: declarationData
    })
    
    if (response.name) {
      emit('success', `Tax Declaration ${response.name} submitted successfully!`)
      emit('close')
    }
  } catch (error) {
    console.error('Error submitting tax declaration:', error)
    // You might want to show an error message to the user here
  } finally {
    loading.value = false
  }
}

// Initialize component
onMounted(async () => {
  await loadFinancialYears()
})
</script>
