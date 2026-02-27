<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200">
    <div class="p-6 border-b border-gray-200">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-900">Shift Schedule</h3>
        <div class="flex items-center space-x-2">
          <button 
            @click="previousMonth"
            class="p-2 text-gray-500 hover:text-gray-700 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <span class="text-sm font-medium text-gray-900 min-w-[120px] text-center">
            {{ currentMonthYear }}
          </span>
          <button 
            @click="nextMonth"
            class="p-2 text-gray-500 hover:text-gray-700 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div class="p-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Calendar Grid -->
      <div v-else class="space-y-4">
        <!-- Weekday Headers -->
        <div class="grid grid-cols-7 gap-1">
          <div v-for="day in weekDays" :key="day" class="text-center text-xs font-medium text-gray-500 py-2">
            {{ day }}
          </div>
        </div>

        <!-- Calendar Days -->
        <div class="grid grid-cols-7 gap-1">
          <!-- Empty cells for days before month starts -->
          <div 
            v-for="n in firstDayOfWeek" 
            :key="`empty-${n}`" 
            class="h-20 border border-gray-100 rounded-lg"
          ></div>
          
          <!-- Actual days of the month -->
          <div 
            v-for="day in daysInMonth" 
            :key="day.date"
            :class="[
              'h-20 border rounded-lg p-2 cursor-pointer transition-colors',
              day.isToday ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:bg-gray-50',
              day.isWeekend ? 'bg-gray-50' : ''
            ]"
            @click="selectDate(day)"
          >
            <div class="flex flex-col h-full">
              <div class="flex justify-between items-start">
                <span :class="[
                  'text-sm font-medium',
                  day.isToday ? 'text-blue-600' : 'text-gray-900'
                ]">{{ day.dayNumber }}</span>
                <span v-if="day.shift" class="text-xs px-1 py-0.5 rounded" :class="getShiftClass(day.shift)">
                  {{ day.shift.shift_name }}
                </span>
              </div>
              
              <div v-if="day.shift" class="mt-auto">
                <div class="text-xs text-gray-600">
                  {{ formatTime(day.shift.start_time) }} - {{ formatTime(day.shift.end_time) }}
                </div>
                <div v-if="day.shift.location" class="text-xs text-gray-500 truncate">
                  {{ day.shift.location }}
                </div>
              </div>
              
              <div v-else-if="!day.isWeekend" class="mt-auto">
                <div class="text-xs text-gray-400">No shift assigned</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Legend -->
      <div class="mt-6 pt-4 border-t border-gray-200">
        <h4 class="text-sm font-medium text-gray-900 mb-3">Shift Types</h4>
        <div class="flex flex-wrap gap-3">
          <div v-for="shiftType in uniqueShiftTypes" :key="shiftType.name" class="flex items-center space-x-2">
            <span :class="getShiftClass(shiftType)" class="text-xs px-2 py-1 rounded">
              {{ shiftType.shift_name }}
            </span>
            <span class="text-xs text-gray-500">{{ formatTime(shiftType.start_time) }} - {{ formatTime(shiftType.end_time) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Shift Details Modal -->
    <div v-if="selectedDate" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Shift Details</h3>
          <button @click="selectedDate = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Date</label>
            <p class="text-gray-900">{{ formatDate(selectedDate.date) }}</p>
          </div>
          
          <div v-if="selectedDate.shift">
            <div>
              <label class="block text-sm font-medium text-gray-700">Shift Type</label>
              <p class="text-gray-900">{{ selectedDate.shift.shift_name }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Working Hours</label>
              <p class="text-gray-900">{{ formatTime(selectedDate.shift.start_time) }} - {{ formatTime(selectedDate.shift.end_time) }}</p>
            </div>
            
            <div v-if="selectedDate.shift.location">
              <label class="block text-sm font-medium text-gray-700">Location</label>
              <p class="text-gray-900">{{ selectedDate.shift.location }}</p>
            </div>
            
            <div v-if="selectedDate.shift.description">
              <label class="block text-sm font-medium text-gray-700">Description</label>
              <p class="text-gray-900">{{ selectedDate.shift.description }}</p>
            </div>
          </div>
          
          <div v-else>
            <p class="text-gray-500">No shift assigned for this date</p>
          </div>
        </div>
        
        <div class="mt-6 pt-4 border-t border-gray-200">
          <button 
            @click="selectedDate = null"
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
import { ref, computed, onMounted, watch } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
  employeeId: {
    type: String,
    required: true
  }
})

// Reactive data
const loading = ref(false)
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())
const shiftAssignments = ref([])
const selectedDate = ref(null)

// Computed properties
const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const currentMonthYear = computed(() => {
  return new Date(currentYear.value, currentMonth.value).toLocaleDateString('en-US', { 
    month: 'long', 
    year: 'numeric' 
  })
})

const firstDayOfWeek = computed(() => {
  return new Date(currentYear.value, currentMonth.value, 1).getDay()
})

const daysInMonth = computed(() => {
  const days = []
  const daysCount = new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
  const today = new Date()
  
  for (let day = 1; day <= daysCount; day++) {
    const date = new Date(currentYear.value, currentMonth.value, day)
    const dateString = date.toISOString().split('T')[0]
    
    // Find shift assignment for this date
    const shiftAssignment = shiftAssignments.value.find(assignment => {
      return assignment.start_date <= dateString && assignment.end_date >= dateString
    })
    
    days.push({
      dayNumber: day,
      date: dateString,
      isToday: date.toDateString() === today.toDateString(),
      isWeekend: date.getDay() === 0 || date.getDay() === 6,
      shift: shiftAssignment ? shiftAssignment.shift_type_details : null
    })
  }
  
  return days
})

const uniqueShiftTypes = computed(() => {
  const shifts = shiftAssignments.value
    .filter(assignment => assignment.shift_type_details)
    .map(assignment => assignment.shift_type_details)
  
  // Remove duplicates
  const unique = {}
  shifts.forEach(shift => {
    unique[shift.name] = shift
  })
  
  return Object.values(unique)
})

// Methods
const previousMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
  loadShiftAssignments()
}

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
  loadShiftAssignments()
}

const selectDate = (day) => {
  selectedDate.value = day
}

const getShiftClass = (shift) => {
  // Generate different colors for different shift types
  const colors = [
    'bg-blue-100 text-blue-800',
    'bg-green-100 text-green-800',
    'bg-purple-100 text-purple-800',
    'bg-orange-100 text-orange-800',
    'bg-pink-100 text-pink-800',
    'bg-indigo-100 text-indigo-800'
  ]
  
  const hash = shift.name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  const colorIndex = hash % colors.length
  
  return colors[colorIndex]
}

const formatTime = (time) => {
  if (!time) return 'N/A'
  const [hours, minutes] = time.split(':')
  const hour = parseInt(hours)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour
  return `${displayHour}:${minutes} ${ampm}`
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const loadShiftAssignments = async () => {
  loading.value = true
  
  try {
    const startDate = new Date(currentYear.value, currentMonth.value, 1).toISOString().split('T')[0]
    const endDate = new Date(currentYear.value, currentMonth.value + 1, 0).toISOString().split('T')[0]
    
    const response = await call('frappe.client.get_list', {
      doctype: 'Shift Assignment',
      fields: ['name', 'shift_type', 'start_date', 'end_date'],
      filters: {
        employee: props.employeeId,
        start_date: ['<=', endDate],
        end_date: ['>=', startDate],
        docstatus: 1
      }
    })
    
    // Get shift type details for each assignment
    const assignmentsWithDetails = await Promise.all(
      response.map(async (assignment) => {
        const shiftDetails = await call('frappe.client.get_value', {
          doctype: 'Shift Type',
          name: assignment.shift_type,
          fields: ['shift_name', 'start_time', 'end_time', 'location', 'description']
        })
        
        return {
          ...assignment,
          shift_type_details: shiftDetails
        }
      })
    )
    
    shiftAssignments.value = assignmentsWithDetails
  } catch (error) {
    console.error('Error loading shift assignments:', error)
    shiftAssignments.value = []
  } finally {
    loading.value = false
  }
}

// Watch for month changes
watch([currentMonth, currentYear], () => {
  loadShiftAssignments()
})

// Initialize component
onMounted(() => {
  loadShiftAssignments()
})
</script>
