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

        <!-- Employee Profile Card -->
        <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Profile Picture and Basic Info -->
            <div class="flex flex-col items-center lg:items-start">
              <div class="relative mb-4">
                <img 
                  v-if="employeeInfo?.image" 
                  :src="employeeInfo.image" 
                  :alt="employeeInfo.employee_name"
                  class="w-24 h-24 rounded-full object-cover border-4 border-white shadow-lg"
                  @error="handleImageError"
                />
                <div 
                  v-else 
                  class="w-24 h-24 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg"
                >
                  {{ getInitials(employeeInfo?.employee_name || currentUser?.full_name || 'User') }}
                </div>
                <div class="absolute -bottom-1 -right-1 w-6 h-6 bg-green-500 rounded-full border-2 border-white"></div>
              </div>
              <div class="text-center lg:text-left">
                <h2 class="text-2xl font-bold text-gray-900 mb-1">{{ employeeInfo?.employee_name || currentUser?.full_name || 'Employee' }}</h2>
                <p class="text-blue-600 font-semibold">{{ employeeInfo?.designation || 'Employee' }}</p>
                <p class="text-gray-500">{{ employeeInfo?.department || 'General' }}</p>
                <p class="text-sm text-gray-400 mt-1">ID: {{ employeeInfo?.employee_number || 'Not Available' }}</p>
              </div>
            </div>

            <!-- Personal Information -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Personal Information</h3>
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-gray-600">Gender:</span>
                  <span class="font-medium text-gray-900">{{ employeeInfo?.gender || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Date of Birth:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(employeeInfo?.date_of_birth) || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Marital Status:</span>
                  <span class="font-medium text-gray-900">{{ employeeInfo?.marital_status || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Blood Group:</span>
                  <span class="font-medium text-gray-900">{{ employeeInfo?.blood_group || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Mobile:</span>
                  <span class="font-medium text-gray-900">{{ employeeInfo?.cell_number || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Personal Email:</span>
                  <span class="font-medium text-gray-900 text-sm">{{ employeeInfo?.personal_email || 'Not specified' }}</span>
                </div>
              </div>
            </div>

            <!-- Employment Details -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Employment Details</h3>
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-gray-600">Company:</span>
                  <span class="font-medium text-gray-900">{{ employeeInfo?.company || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Branch:</span>
                  <span class="font-medium text-gray-900">{{ employeeInfo?.branch || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Date of Joining:</span>
                  <span class="font-medium text-gray-900">{{ formatDate(employeeInfo?.date_of_joining) || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Reports To:</span>
                  <span class="font-medium text-gray-900">{{ employeeInfo?.reports_to_name || 'Not specified' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Status:</span>
                  <span :class="getStatusClass(employeeInfo?.status)">{{ employeeInfo?.status || 'Active' }}</span>
                </div>
                <div class="flex justify-between" v-if="employeeInfo?.holiday_list">
                  <span class="text-gray-600">Holiday List:</span>
                  <span class="font-medium text-gray-900">{{ employeeInfo.holiday_list }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Emergency Contact Information -->
          <div v-if="employeeInfo?.person_to_be_contacted || employeeInfo?.emergency_phone_number" class="mt-8 pt-6 border-t border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Emergency Contact</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div v-if="employeeInfo?.person_to_be_contacted">
                <span class="text-gray-600">Contact Person:</span>
                <p class="font-medium text-gray-900">{{ employeeInfo.person_to_be_contacted }}</p>
              </div>
              <div v-if="employeeInfo?.relation">
                <span class="text-gray-600">Relation:</span>
                <p class="font-medium text-gray-900">{{ employeeInfo.relation }}</p>
              </div>
              <div v-if="employeeInfo?.emergency_phone_number">
                <span class="text-gray-600">Emergency Phone:</span>
                <p class="font-medium text-gray-900">{{ employeeInfo.emergency_phone_number }}</p>
              </div>
            </div>
          </div>

          <!-- Address Information -->
          <div v-if="employeeInfo?.current_address || employeeInfo?.permanent_address" class="mt-8 pt-6 border-t border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Address Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-if="employeeInfo?.current_address">
                <h4 class="font-medium text-gray-700 mb-2">Current Address</h4>
                <p class="text-gray-600 text-sm">{{ employeeInfo.current_address }}</p>
              </div>
              <div v-if="employeeInfo?.permanent_address">
                <h4 class="font-medium text-gray-700 mb-2">Permanent Address</h4>
                <p class="text-gray-600 text-sm">{{ employeeInfo.permanent_address }}</p>
              </div>
            </div>
          </div>

          <div v-if="!employeeInfo && !error" class="mt-4">
            <p class="text-sm text-orange-600 bg-orange-50 px-3 py-2 rounded-lg">
              Employee record not linked. Contact administrator to link your user account with an Employee record.
            </p>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="flex justify-center mb-6">
          <div class="flex space-x-4">
            <button 
              @click="showAttendanceForm = true"
              class="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg border border-blue-600 hover:bg-blue-700 hover:border-blue-700 transition-colors duration-200 shadow-sm"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="font-medium">Mark Attendance</span>
            </button>
            
            <button 
              @click="showLeaveForm = true"
              class="flex items-center space-x-2 px-6 py-3 bg-white text-green-600 rounded-lg border border-green-600 hover:bg-green-50 hover:border-green-700 hover:text-green-700 transition-colors duration-200 shadow-sm"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              <span class="font-medium">Apply Leave</span>
            </button>
          </div>
        </div>

        <!-- Tab Navigation -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
          <div class="border-b border-gray-200">
            <nav class="flex space-x-8 px-6" aria-label="Tabs">
              <button 
                @click="activeTab = 'attendance'"
                :class="[
                  'py-4 px-1 border-b-2 font-medium text-sm',
                  activeTab === 'attendance' 
                    ? 'border-blue-500 text-blue-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                View Attendance
              </button>
              <button 
                @click="activeTab = 'leaves'"
                :class="[
                  'py-4 px-1 border-b-2 font-medium text-sm',
                  activeTab === 'leaves' 
                    ? 'border-blue-500 text-blue-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                Leave Applications
              </button>
              <button 
                @click="activeTab = 'salary'; loadSalarySlips()"
                :class="[
                  'py-4 px-1 border-b-2 font-medium text-sm',
                  activeTab === 'salary' 
                    ? 'border-blue-500 text-blue-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                Salary Slips
              </button>
            </nav>
          </div>

          <!-- Tab Content -->
          <div class="p-6">
            <!-- Attendance Tab -->
            <div v-if="activeTab === 'attendance'">
              <!-- Date Filter Controls -->
              <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                <div class="flex items-center space-x-4">
                  <label class="text-sm font-medium text-blue-900">Filter by Date:</label>
                  <div class="flex items-center space-x-2">
                    <label class="text-xs text-blue-700">From:</label>
                    <input
                      type="date"
                      v-model="attendanceFromDate"
                      class="px-2 py-1 text-sm border border-blue-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                    />
                  </div>
                  <div class="flex items-center space-x-2">
                    <label class="text-xs text-blue-700">To:</label>
                    <input
                      type="date"
                      v-model="attendanceToDate"
                      class="px-2 py-1 text-sm border border-blue-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                    />
                  </div>
                  <button
                    @click="filterAttendanceRecords"
                    class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                  >
                    Apply Filter
                  </button>
                  <button
                    @click="clearAttendanceFilter"
                    class="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
                  >
                    Clear
                  </button>
                </div>
              </div>
              
              <div v-if="attendanceRecords.length === 0" class="text-center py-8 text-gray-500">
                No attendance records found
              </div>
              <div v-else class="space-y-3">
                <div v-for="record in attendanceRecords" :key="record.name" class="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p class="font-medium text-gray-900">{{ formatDate(record.attendance_date) }}</p>
                    <p class="text-sm text-gray-600">{{ record.status }}</p>
                    <p v-if="record.in_time" class="text-xs text-gray-500">In: {{ formatTime(record.in_time) }}</p>
                    <p v-if="record.out_time" class="text-xs text-gray-500">Out: {{ formatTime(record.out_time) }}</p>
                    <p class="text-xs text-gray-400">Status: {{ record.docstatus_label || 'Unknown' }}</p>
                  </div>
                  <div class="flex flex-col items-end space-y-1">
                    <span :class="getAttendanceStatusClass(record.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                      {{ record.status }}
                    </span>
                    <span :class="getDocStatusClass(record.docstatus)" class="px-2 py-1 text-xs font-medium rounded-full">
                      {{ record.docstatus_label }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Leave Applications Tab -->
            <div v-if="activeTab === 'leaves'">
              <!-- Date Filter Controls -->
              <div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                <div class="flex items-center space-x-4">
                  <label class="text-sm font-medium text-green-900">Filter by Date:</label>
                  <div class="flex items-center space-x-2">
                    <label class="text-xs text-green-700">From:</label>
                    <input
                      type="date"
                      v-model="leaveFromDate"
                      class="px-2 py-1 text-sm border border-green-300 rounded focus:outline-none focus:ring-1 focus:ring-green-500"
                    />
                  </div>
                  <div class="flex items-center space-x-2">
                    <label class="text-xs text-green-700">To:</label>
                    <input
                      type="date"
                      v-model="leaveToDate"
                      class="px-2 py-1 text-sm border border-green-300 rounded focus:outline-none focus:ring-1 focus:ring-green-500"
                    />
                  </div>
                  <button
                    @click="filterLeaveApplications"
                    class="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                  >
                    Apply Filter
                  </button>
                  <button
                    @click="clearLeaveFilter"
                    class="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
                  >
                    Clear
                  </button>
                </div>
              </div>
              
              <div v-if="leaveApplications.length === 0" class="text-center py-8 text-gray-500">
                No leave applications found
              </div>
              <div v-else class="space-y-3">
                <div v-for="leave in leaveApplications" :key="leave.name" class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p class="font-medium text-gray-900">{{ leave.leave_type }}</p>
                    <p class="text-sm text-gray-600">{{ formatDate(leave.from_date) }} - {{ formatDate(leave.to_date) }}</p>
                    <p class="text-xs text-gray-500">{{ leave.total_leave_days }} days</p>
                  </div>
                  <span :class="getLeaveStatusClass(leave.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ leave.status }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Salary Slips Tab -->
            <div v-if="activeTab === 'salary'" class="space-y-4">
              <!-- Date Filter Controls -->
              <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <div class="flex items-center space-x-4 mb-3">
                  <label class="text-sm font-medium text-purple-900">Filter by Date:</label>
                  <div class="flex items-center space-x-2">
                    <label class="text-xs text-purple-700">From:</label>
                    <input
                      type="date"
                      v-model="salaryFromDate"
                      class="px-2 py-1 text-sm border border-purple-300 rounded focus:outline-none focus:ring-1 focus:ring-purple-500"
                    />
                  </div>
                  <div class="flex items-center space-x-2">
                    <label class="text-xs text-purple-700">To:</label>
                    <input
                      type="date"
                      v-model="salaryToDate"
                      class="px-2 py-1 text-sm border border-purple-300 rounded focus:outline-none focus:ring-1 focus:ring-purple-500"
                    />
                  </div>
                  <button
                    @click="filterSalarySlips"
                    class="px-3 py-1 text-sm bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors"
                  >
                    Apply Filter
                  </button>
                  <button
                    @click="clearSalaryFilter"
                    class="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
                  >
                    Clear
                  </button>
                </div>
              </div>
              
              <!-- Print Format Selection -->
              <div v-if="salarySlips.length > 0" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="flex items-center space-x-4">
                  <label for="printFormat" class="text-sm font-medium text-blue-900">
                    Select Print Format:
                  </label>
                  <select
                    id="printFormat"
                    v-model="selectedPrintFormat"
                    class="block w-64 px-3 py-2 text-sm border border-blue-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option v-for="format in printFormats" :key="format.name" :value="format.name">
                      {{ format.label }}
                    </option>
                  </select>
                  <span class="text-xs text-blue-600">
                    This format will be used for both preview and download
                  </span>
                </div>
              </div>
              
              <div v-if="salarySlips.length === 0" class="text-center py-12 bg-gray-50 rounded-lg">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
                </svg>
                <p class="text-lg font-medium text-gray-900 mb-2">No Salary Slips Found</p>
                <p class="text-sm text-gray-500">Salary slips don't exist in the system yet.<br>Contact HR or administrator for salary slip generation.</p>
              </div>
              <div v-else class="space-y-3">
                <div v-for="slip in salarySlips" :key="slip.name" class="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <div class="flex-1">
                    <p class="font-medium text-gray-900">{{ formatDate(slip.start_date) }} - {{ formatDate(slip.end_date) }}</p>
                    <p class="text-sm text-gray-600">Gross: ₹{{ slip.gross_pay }} | Net: ₹{{ slip.net_pay }}</p>
                    <div class="flex items-center space-x-4 mt-1">
                      <span :class="getSalarySlipStatusClass(slip.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                        {{ slip.status }}
                      </span>
                      <span :class="getDocStatusClass(slip.docstatus)" class="px-2 py-1 text-xs font-medium rounded-full">
                        {{ slip.docstatus_label }}
                      </span>
                    </div>
                  </div>
                  <div class="flex space-x-2">
                    <button
                      @click="previewSalarySlip(slip.name)"
                      class="px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 hover:border-blue-300 transition-colors duration-200"
                    >
                      Preview
                    </button>
                    <button
                      @click="downloadSalarySlip(slip.name)"
                      class="px-3 py-1.5 text-sm font-medium text-green-600 bg-green-50 border border-green-200 rounded-md hover:bg-green-100 hover:border-green-300 transition-colors duration-200"
                    >
                      Download
                    </button>
                  </div>
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
                <p class="text-2xl font-bold text-blue-600">{{ balance.leaves_remaining || (balance.total_leaves_allocated - (balance.leaves_taken || 0)) }}</p>
                <p class="text-sm text-gray-600">Available out of {{ balance.total_leaves_allocated }}</p>
                <p class="text-xs text-gray-500">Used: {{ balance.leaves_taken || 0 }}</p>
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
              <option v-for="leaveType in availableLeaveTypes" :key="leaveType.name" :value="leaveType.name">
                {{ leaveType.leave_type_name }}
              </option>
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

    <!-- Attendance Marking Modal -->
    <div v-if="showAttendanceForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Mark Attendance</h3>
          <button @click="showAttendanceForm = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="submitAttendance" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Attendance Date</label>
            <input v-model="attendanceForm.attendanceDate" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select v-model="attendanceForm.status" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="Present">Present</option>
              <option value="Absent">Absent</option>
              <option value="Work From Home">Work From Home</option>
              <option value="Half Day">Half Day</option>
              <option value="On Leave">On Leave</option>
            </select>
          </div>
          
          <div class="grid grid-cols-2 gap-4" v-if="attendanceForm.status === 'Present' || attendanceForm.status === 'Work From Home'">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">In Time</label>
              <input v-model="attendanceForm.inTime" type="time" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Out Time</label>
              <input v-model="attendanceForm.outTime" type="time" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Remarks (Optional)</label>
            <textarea v-model="attendanceForm.remarks" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none" placeholder="Any additional notes..."></textarea>
          </div>
          
          <div class="flex space-x-3">
            <Button type="submit" theme="blue" variant="solid" class="flex-1" :loading="attendanceLoading">
              Mark Attendance
            </Button>
            <Button type="button" theme="gray" variant="outline" @click="showAttendanceForm = false">
              Cancel
            </Button>
          </div>
        </form>
      </div>
    </div>

    <!-- Salary Slip Preview Modal -->
    <div v-if="showPreviewModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
        <div class="flex justify-between items-center p-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Salary Slip Preview</h3>
          <button @click="closePreviewModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="p-4 overflow-y-auto max-h-[calc(90vh-120px)]">
          <div v-if="previewLoading" class="flex justify-center items-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
          <div v-else-if="previewHtml" v-html="previewHtml" class="salary-slip-preview"></div>
          <div v-else class="text-center py-8 text-gray-500">
            Failed to load salary slip preview
          </div>
        </div>
        <div class="flex justify-end space-x-2 p-4 border-t border-gray-200">
          <button
            @click="downloadCurrentSlip"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors duration-200"
          >
            Download PDF
          </button>
          <button
            @click="closePreviewModal"
            class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition-colors duration-200"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Custom Confirmation Modal -->
    <div v-if="showConfirmationModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="p-6">
          <div class="flex items-center mb-4">
            <!-- Success Icon -->
            <div v-if="confirmationType === 'success'" class="flex-shrink-0 w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <!-- Error Icon -->
            <div v-else-if="confirmationType === 'error'" class="flex-shrink-0 w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </div>
            <!-- Warning Icon -->
            <div v-else-if="confirmationType === 'warning'" class="flex-shrink-0 w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">
                {{ confirmationType === 'success' ? 'Success' : confirmationType === 'error' ? 'Error' : 'Warning' }}
              </h3>
            </div>
          </div>
          
          <p class="text-gray-600 mb-6">{{ confirmationMessage }}</p>
          
          <div class="flex justify-end">
            <button 
              @click="closeConfirmationModal"
              :class="[
                'px-4 py-2 rounded-md font-medium transition-colors duration-200',
                confirmationType === 'success' ? 'bg-green-600 hover:bg-green-700 text-white' :
                confirmationType === 'error' ? 'bg-red-600 hover:bg-red-700 text-white' :
                'bg-yellow-600 hover:bg-yellow-700 text-white'
              ]"
            >
              OK
            </button>
          </div>
        </div>
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
const currentUser = ref(null)
const attendanceRecords = ref([])
const leaveApplications = ref([])
const leaveBalance = ref([])
const attendanceLoading = ref(false)
const leaveLoading = ref(false)
const showLeaveForm = ref(false)
const showAttendanceForm = ref(false)
const activeTab = ref('attendance')
const salarySlips = ref([])
const showPreviewModal = ref(false)
const previewLoading = ref(false)
const previewHtml = ref('')
const currentSlipName = ref('')
const printFormats = ref([])
const selectedPrintFormat = ref('Salary Slip Standard')

// Date filter reactive variables
const attendanceFromDate = ref('')
const attendanceToDate = ref('')
const salaryFromDate = ref('')
const salaryToDate = ref('')
const leaveFromDate = ref('')
const leaveToDate = ref('')
const availableLeaveTypes = ref([])

// Custom confirmation modal
const showConfirmationModal = ref(false)
const confirmationMessage = ref('')
const confirmationType = ref('success') // 'success', 'error', 'warning'

const leaveForm = ref({
  leaveType: '',
  fromDate: '',
  toDate: '',
  description: ''
})

const attendanceForm = ref({
  status: 'Present',
  attendanceDate: new Date().toISOString().split('T')[0], // Today's date
  inTime: '',
  outTime: '',
  remarks: ''
})

// Helper functions
const getInitials = (name) => {
  if (!name) return 'E'
  return name.split(' ').map(n => n.charAt(0)).join('').toUpperCase().substring(0, 2)
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
    // Don't set error for missing employee record, just log it
    if (err.message && err.message.includes('Employee record not found')) {
      console.log('No employee record found for user, showing fallback data')
    } else {
      error.value = err.message || 'Failed to load employee information'
    }
  }
}

const loadCurrentUser = async () => {
  try {
    // Get current user info from session
    const userResponse = await call('frappe.auth.get_logged_user')
    if (userResponse) {
      currentUser.value = {
        email: userResponse,
        full_name: 'Amit Kumar' // Fallback name
      }
    }
  } catch (err) {
    console.error('Error loading current user:', err)
  }
}

const loadAttendanceRecords = async (fromDate = null, toDate = null) => {
  try {
    const params = {}
    if (fromDate) params.from_date = fromDate
    if (toDate) params.to_date = toDate
    
    const response = await call('ascra_frontend.api.get_attendance_records', params)
    console.log('Attendance API response:', response)
    
    if (response.success === false) {
      console.error('API returned error:', response.message)
      attendanceRecords.value = []
      return
    }
    
    console.log('Attendance records received:', response.attendance_records)
    console.log('Total attendance records:', response.attendance_records ? response.attendance_records.length : 0)
    attendanceRecords.value = response.attendance_records || []
    console.log('Attendance records set in frontend:', attendanceRecords.value)
  } catch (err) {
    console.error('Error loading attendance records:', err)
    attendanceRecords.value = []
  }
}

const loadLeaveApplications = async (fromDate = null, toDate = null) => {
  try {
    const params = {}
    if (fromDate) params.from_date = fromDate
    if (toDate) params.to_date = toDate
    
    const response = await call('ascra_frontend.api.get_leave_applications', params)
    
    if (response.success === false) {
      console.error('API returned error:', response.message)
      leaveApplications.value = []
      return
    }
    
    if (response.success) {
      leaveApplications.value = response.leave_applications
    }
  } catch (err) {
    console.error('Error loading leave applications:', err)
    leaveApplications.value = []
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
    // Don't show error for missing employee record
  }
}

const loadAvailableLeaveTypes = async () => {
  try {
    const response = await call('ascra_frontend.api.get_leave_types')
    
    if (response.success === false) {
      console.error('API returned error:', response.message)
      availableLeaveTypes.value = []
      return
    }
    
    if (response.success) {
      availableLeaveTypes.value = response.leave_types
      console.log('Leave types loaded:', availableLeaveTypes.value)
    }
  } catch (err) {
    console.error('Error loading leave types:', err)
    availableLeaveTypes.value = []
  }
}

const loadSalarySlips = async (fromDate = null, toDate = null) => {
  try {
    const params = {}
    if (fromDate) params.from_date = fromDate
    if (toDate) params.to_date = toDate
    
    const response = await call('ascra_frontend.api.get_salary_slips', params)
    console.log('Salary slips API response:', response)
    
    if (response.success === false) {
      console.error('API returned error:', response.message)
      salarySlips.value = []
      return
    }
    
    if (response.success) {
      salarySlips.value = response.salary_slips
      console.log('Salary slips loaded:', salarySlips.value)
    } else {
      console.log('API returned unsuccessful response:', response)
      salarySlips.value = []
    }
  } catch (err) {
    console.error('Error loading salary slips:', err)
    // Keep salarySlips empty to show the "No Salary Slips Found" message
    salarySlips.value = []
  }
}

const submitAttendance = async () => {
  attendanceLoading.value = true
  try {
    // Prepare attendance data
    const attendanceData = {
      status: attendanceForm.value.status,
      attendance_date: attendanceForm.value.attendanceDate
    }
    
    // Add time fields if present
    if (attendanceForm.value.inTime) {
      attendanceData.in_time = `${attendanceForm.value.attendanceDate} ${attendanceForm.value.inTime}:00`
    }
    if (attendanceForm.value.outTime) {
      attendanceData.out_time = `${attendanceForm.value.attendanceDate} ${attendanceForm.value.outTime}:00`
    }
    
    const response = await call('ascra_frontend.api.mark_attendance', attendanceData)
    
    if (response.success) {
      showCustomConfirmation('Attendance marked successfully!', 'success')
      showAttendanceForm.value = false
      // Reset form
      attendanceForm.value = {
        status: 'Present',
        attendanceDate: new Date().toISOString().split('T')[0],
        inTime: '',
        outTime: '',
        remarks: ''
      }
      await loadAttendanceRecords()
    } else if (response.already_exists) {
      showCustomConfirmation(response.message || 'Attendance already marked for this date', 'warning')
    }
  } catch (err) {
    console.error('Error marking attendance:', err)
    showCustomConfirmation(err.message || 'Failed to mark attendance', 'error')
  } finally {
    attendanceLoading.value = false
  }
}

const submitLeaveApplication = async () => {
  leaveLoading.value = true
  try {
    console.log('Submitting leave application with data:', {
      leave_type: leaveForm.value.leaveType,
      from_date: leaveForm.value.fromDate,
      to_date: leaveForm.value.toDate,
      description: leaveForm.value.description
    })
    
    const response = await call('ascra_frontend.api.apply_leave', {
      leave_type: leaveForm.value.leaveType,
      from_date: leaveForm.value.fromDate,
      to_date: leaveForm.value.toDate,
      description: leaveForm.value.description
    })
    
    console.log('Leave application response:', response)
    
    if (response.success) {
      showCustomConfirmation('Leave application submitted successfully!', 'success')
      showLeaveForm.value = false
      // Reset form
      leaveForm.value = {
        leaveType: '',
        fromDate: '',
        toDate: '',
        description: ''
      }
      await loadLeaveApplications()
    } else {
      console.error('Leave application failed:', response.message)
      showCustomConfirmation(response.message || 'Failed to submit leave application', 'error')
    }
  } catch (err) {
    console.error('Error submitting leave application:', err)
    showCustomConfirmation(err.message || 'Failed to submit leave application', 'error')
  } finally {
    leaveLoading.value = false
  }
}

// Load print formats
const loadPrintFormats = async () => {
  try {
    const response = await call('ascra_frontend.api.get_salary_slip_print_formats')
    if (response.success) {
      printFormats.value = response.print_formats
    }
  } catch (err) {
    console.error('Error loading print formats:', err)
    // Set default formats if API fails
    printFormats.value = [
      {"name": "Salary Slip Standard", "label": "Standard Format"},
      {"name": "Salary Slip with Year to Date", "label": "With Year to Date"},
      {"name": "Salary Slip based on Timesheet", "label": "Based on Timesheet"}
    ]
  }
}

// Salary Slip Functions
const previewSalarySlip = async (slipName) => {
  try {
    showPreviewModal.value = true
    previewLoading.value = true
    previewHtml.value = ''
    currentSlipName.value = slipName
    
    const response = await call('ascra_frontend.api.get_salary_slip_html', {
      salary_slip_name: slipName,
      print_format: selectedPrintFormat.value
    })
    
    if (response.success) {
      previewHtml.value = response.html
    } else {
      console.error('Failed to load salary slip preview:', response.message)
      showCustomConfirmation('Failed to load salary slip preview: ' + response.message, 'error')
      closePreviewModal()
    }
  } catch (err) {
    console.error('Error loading salary slip preview:', err)
    showCustomConfirmation('Error loading salary slip preview: ' + err.message, 'error')
    closePreviewModal()
  } finally {
    previewLoading.value = false
  }
}

const downloadSalarySlip = async (slipName) => {
  try {
    // Create a temporary link to trigger the download with selected print format
    const downloadUrl = `/api/method/ascra_frontend.api.download_salary_slip_pdf?salary_slip_name=${encodeURIComponent(slipName)}&print_format=${encodeURIComponent(selectedPrintFormat.value)}`
    
    // Create a temporary anchor element and trigger download
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = `salary_slip_${slipName}_${selectedPrintFormat.value.replace(/\s+/g, '_')}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    console.log('Salary slip download initiated for:', slipName, 'with format:', selectedPrintFormat.value)
  } catch (err) {
    console.error('Error downloading salary slip:', err)
    showCustomConfirmation('Error downloading salary slip: ' + err.message, 'error')
  }
}

const downloadCurrentSlip = () => {
  if (currentSlipName.value) {
    downloadSalarySlip(currentSlipName.value)
  }
}

const closePreviewModal = () => {
  showPreviewModal.value = false
  previewLoading.value = false
  previewHtml.value = ''
  currentSlipName.value = ''
}

// Custom confirmation modal functions
const showCustomConfirmation = (message, type = 'success') => {
  confirmationMessage.value = message
  confirmationType.value = type
  showConfirmationModal.value = true
}

const closeConfirmationModal = () => {
  showConfirmationModal.value = false
  confirmationMessage.value = ''
  confirmationType.value = 'success'
}

// Utility functions for enhanced employee profile
const handleImageError = (event) => {
  // Hide the broken image and show initials instead
  event.target.style.display = 'none'
}

const formatDate = (dateString) => {
  if (!dateString) return null
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (err) {
    return dateString
  }
}

const getStatusClass = (status) => {
  switch (status) {
    case 'Active': return 'bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium'
    case 'Inactive': return 'bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs font-medium'
    case 'Suspended': return 'bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-medium'
    case 'Left': return 'bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-medium'
    default: return 'bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium'
  }
}

// Status styling functions
const getDocStatusClass = (docstatus) => {
  switch (docstatus) {
    case 0: return 'bg-yellow-100 text-yellow-800' // Draft
    case 1: return 'bg-green-100 text-green-800'   // Submitted
    case 2: return 'bg-red-100 text-red-800'       // Cancelled
    default: return 'bg-gray-100 text-gray-800'
  }
}

const getSalarySlipStatusClass = (status) => {
  switch (status) {
    case 'Draft': return 'bg-yellow-100 text-yellow-800'
    case 'Submitted': return 'bg-green-100 text-green-800'
    case 'Cancelled': return 'bg-red-100 text-red-800'
    case 'Withheld': return 'bg-orange-100 text-orange-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

// Date filter functions
const filterAttendanceRecords = () => {
  loadAttendanceRecords(attendanceFromDate.value, attendanceToDate.value)
}

const clearAttendanceFilter = () => {
  attendanceFromDate.value = ''
  attendanceToDate.value = ''
  loadAttendanceRecords()
}

const filterSalarySlips = () => {
  loadSalarySlips(salaryFromDate.value, salaryToDate.value)
}

const clearSalaryFilter = () => {
  salaryFromDate.value = ''
  salaryToDate.value = ''
  loadSalarySlips()
}

const filterLeaveApplications = () => {
  loadLeaveApplications(leaveFromDate.value, leaveToDate.value)
}

const clearLeaveFilter = () => {
  leaveFromDate.value = ''
  leaveToDate.value = ''
  loadLeaveApplications()
}

// Initialize dashboard
onMounted(async () => {
  try {
    await Promise.all([
      loadCurrentUser(),
      loadEmployeeInfo(),
      loadAttendanceRecords(),
      loadLeaveApplications(),
      loadLeaveBalance(),
      loadPrintFormats(),
      loadAvailableLeaveTypes()
    ])
  } catch (err) {
    console.error('Error initializing employee dashboard:', err)
    error.value = 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.salary-slip-preview {
  font-family: Arial, sans-serif;
  line-height: 1.4;
}

.salary-slip-preview table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
}

.salary-slip-preview table, 
.salary-slip-preview th, 
.salary-slip-preview td {
  border: 1px solid #ddd;
}

.salary-slip-preview th, 
.salary-slip-preview td {
  padding: 8px;
  text-align: left;
}

.salary-slip-preview th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.salary-slip-preview .text-right {
  text-align: right;
}

.salary-slip-preview .text-center {
  text-align: center;
}

.salary-slip-preview h1, 
.salary-slip-preview h2, 
.salary-slip-preview h3 {
  margin: 10px 0;
  color: #333;
}
</style>
