<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <Navigation />
    
    <!-- Employee Dashboard Content -->
    <div id="employee-dashboard" class="pt-20 pb-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">
            Employee Dashboard
          </h1>
          <p class="text-gray-600 mt-2" v-if="employeeInfo">
            Welcome, {{ employeeInfo.employee_name }}! Manage your attendance, leaves, and view salary information.
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 mb-8">
          <div class="flex items-center">
            <svg class="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <p class="text-red-800">{{ error }}</p>
          </div>
        </div>

        <!-- Employee Info Card -->
        <div v-else-if="employeeInfo" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <div class="flex items-center space-x-4">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-xl font-bold">
              {{ getInitials(employeeInfo.employee_name) }}
            </div>
            <div>
              <h2 class="text-xl font-bold text-gray-900">{{ employeeInfo.employee_name }}</h2>
              <p class="text-gray-600">{{ employeeInfo.designation }} - {{ employeeInfo.department }}</p>
              <p class="text-sm text-gray-500">Employee ID: {{ employeeInfo.employee_number }}</p>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Button 
            theme="blue" 
            variant="solid" 
            class="h-20 flex flex-col items-center justify-center space-y-2"
            @click="markTodayAttendance"
            :loading="attendanceLoading"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>Mark Attendance</span>
          </Button>
          
          <Button 
            theme="green" 
            variant="outline" 
            class="h-20 flex flex-col items-center justify-center space-y-2"
            @click="showLeaveForm = true"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z"/>
            </svg>
            <span>Apply Leave</span>
          </Button>
          
          <Button 
            theme="purple" 
            variant="outline" 
            class="h-20 flex flex-col items-center justify-center space-y-2"
            @click="loadAttendanceRecords"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            <span>View Attendance</span>
          </Button>
          
          <Button 
            theme="orange" 
            variant="outline" 
            class="h-20 flex flex-col items-center justify-center space-y-2"
            @click="loadSalarySlips"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
            </svg>
            <span>Salary Slips</span>
          </Button>
        </div>

        <!-- Content Sections -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Attendance Records -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200">
            <div class="p-6 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">Recent Attendance</h3>
            </div>
            <div class="p-6">
              <div v-if="attendanceRecords.length === 0" class="text-center py-8 text-gray-500">
                No attendance records found
              </div>
              <div v-else class="space-y-3">
                <div v-for="record in attendanceRecords.slice(0, 5)" :key="record.name" class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p class="font-medium text-gray-900">{{ formatDate(record.attendance_date) }}</p>
                    <p class="text-sm text-gray-600">{{ record.in_time ? formatTime(record.in_time) : 'N/A' }}</p>
                  </div>
                  <span :class="getAttendanceStatusClass(record.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ record.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Leave Applications -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200">
            <div class="p-6 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">Leave Applications</h3>
            </div>
            <div class="p-6">
              <div v-if="leaveApplications.length === 0" class="text-center py-8 text-gray-500">
                No leave applications found
              </div>
              <div v-else class="space-y-3">
                <div v-for="leave in leaveApplications.slice(0, 5)" :key="leave.name" class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p class="font-medium text-gray-900">{{ leave.leave_type }}</p>
                    <p class="text-sm text-gray-600">{{ formatDate(leave.from_date) }} - {{ formatDate(leave.to_date) }}</p>
                  </div>
                  <span :class="getLeaveStatusClass(leave.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ leave.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Leave Balance -->
        <div v-if="leaveBalance.length > 0" class="mt-8 bg-white rounded-xl shadow-sm border border-gray-200">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900">Leave Balance</h3>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div v-for="balance in leaveBalance" :key="balance.leave_type" class="bg-blue-50 rounded-lg p-4">
                <h4 class="font-medium text-gray-900">{{ balance.leave_type }}</h4>
                <p class="text-2xl font-bold text-blue-600">{{ balance.total_leaves_allocated - balance.leaves_taken }}</p>
                <p class="text-sm text-gray-600">Available out of {{ balance.total_leaves_allocated }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Leave Application Modal -->
    <div v-if="showLeaveForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Apply for Leave</h3>
          <button @click="showLeaveForm = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="submitLeaveApplication" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Leave Type</label>
            <select v-model="leaveForm.leaveType" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Leave Type</option>
              <option value="Annual Leave">Annual Leave</option>
              <option value="Sick Leave">Sick Leave</option>
              <option value="Casual Leave">Casual Leave</option>
              <option value="Emergency Leave">Emergency Leave</option>
            </select>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">From Date</label>
              <input v-model="leaveForm.fromDate" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">To Date</label>
              <input v-model="leaveForm.toDate" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Reason</label>
            <textarea v-model="leaveForm.description" rows="3" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" placeholder="Reason for leave..."></textarea>
          </div>
          
          <div class="flex space-x-3">
            <Button type="submit" theme="blue" variant="solid" class="flex-1" :loading="leaveLoading">
              Submit Application
            </Button>
            <Button type="button" theme="gray" variant="outline" @click="showLeaveForm = false">
              Cancel
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { call } from 'frappe-ui'
import Navigation from '../components/Navigation.vue'

// Reactive data
const loading = ref(true)
const error = ref('')
const employeeInfo = ref(null)
const attendanceRecords = ref([])
const leaveApplications = ref([])
const leaveBalance = ref([])
const attendanceLoading = ref(false)
const leaveLoading = ref(false)
const showLeaveForm = ref(false)

const leaveForm = ref({
  leaveType: '',
  fromDate: '',
  toDate: '',
  description: ''
})

// Helper functions
const getInitials = (name) => {
  if (!name) return 'E'
  return name.split(' ').map(n => n.charAt(0)).join('').toUpperCase().substring(0, 2)
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const formatTime = (timeString) => {
  if (!timeString) return 'N/A'
  return new Date(timeString).toLocaleTimeString()
}

const getAttendanceStatusClass = (status) => {
  const classes = {
    'Present': 'bg-green-100 text-green-800',
    'Absent': 'bg-red-100 text-red-800',
    'On Leave': 'bg-yellow-100 text-yellow-800',
    'Half Day': 'bg-blue-100 text-blue-800',
    'Work From Home': 'bg-purple-100 text-purple-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getLeaveStatusClass = (status) => {
  const classes = {
    'Open': 'bg-yellow-100 text-yellow-800',
    'Approved': 'bg-green-100 text-green-800',
    'Rejected': 'bg-red-100 text-red-800',
    'Cancelled': 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

// API functions
const loadEmployeeInfo = async () => {
  try {
    const response = await call('ascra_frontend.api.get_employee_info')
    if (response.success) {
      employeeInfo.value = response.employee
    }
  } catch (err) {
    console.error('Error loading employee info:', err)
    error.value = err.message || 'Failed to load employee information'
  }
}

const loadAttendanceRecords = async () => {
  try {
    const response = await call('ascra_frontend.api.get_attendance_records')
    if (response.success) {
      attendanceRecords.value = response.attendance_records
    }
  } catch (err) {
    console.error('Error loading attendance records:', err)
  }
}

const loadLeaveApplications = async () => {
  try {
    const response = await call('ascra_frontend.api.get_leave_applications')
    if (response.success) {
      leaveApplications.value = response.leave_applications
    }
  } catch (err) {
    console.error('Error loading leave applications:', err)
  }
}

const loadLeaveBalance = async () => {
  try {
    const response = await call('ascra_frontend.api.get_leave_balance')
    if (response.success) {
      leaveBalance.value = response.leave_balance
    }
  } catch (err) {
    console.error('Error loading leave balance:', err)
  }
}

const markTodayAttendance = async () => {
  attendanceLoading.value = true
  try {
    const response = await call('ascra_frontend.api.mark_attendance', {
      status: 'Present'
    })
    if (response.success) {
      alert('Attendance marked successfully!')
      await loadAttendanceRecords()
    }
  } catch (err) {
    console.error('Error marking attendance:', err)
    alert(err.message || 'Failed to mark attendance')
  } finally {
    attendanceLoading.value = false
  }
}

const submitLeaveApplication = async () => {
  leaveLoading.value = true
  try {
    const response = await call('ascra_frontend.api.apply_leave', {
      leave_type: leaveForm.value.leaveType,
      from_date: leaveForm.value.fromDate,
      to_date: leaveForm.value.toDate,
      description: leaveForm.value.description
    })
    if (response.success) {
      alert('Leave application submitted successfully!')
      showLeaveForm.value = false
      leaveForm.value = {
        leaveType: '',
        fromDate: '',
        toDate: '',
        description: ''
      }
      await loadLeaveApplications()
    }
  } catch (err) {
    console.error('Error submitting leave application:', err)
    alert(err.message || 'Failed to submit leave application')
  } finally {
    leaveLoading.value = false
  }
}

// Initialize dashboard
onMounted(async () => {
  try {
    await Promise.all([
      loadEmployeeInfo(),
      loadAttendanceRecords(),
      loadLeaveApplications(),
      loadLeaveBalance()
    ])
  } catch (err) {
    console.error('Error initializing employee dashboard:', err)
    error.value = 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
})
</script>
