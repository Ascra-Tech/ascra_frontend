<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800">
    <!-- Navigation -->
    <Navigation />
    
    <!-- My Account Content -->
    <div class="pt-20 pb-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">My Account</h1>
          <p class="text-gray-600 dark:text-gray-300 mt-2">Manage your profile and account settings</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Sidebar - Profile Card -->
          <div class="lg:col-span-1">
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <!-- Profile Image -->
              <div class="text-center mb-6">
                <div v-if="userProfile.user_image" class="w-32 h-32 mx-auto rounded-full overflow-hidden border-4 border-blue-100">
                  <img :src="userProfile.user_image" :alt="userProfile.full_name" class="w-full h-full object-cover" />
                </div>
                <div v-else class="w-32 h-32 mx-auto rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-4xl font-bold">
                  {{ getUserInitials }}
                </div>
                <h2 class="mt-4 text-xl font-bold text-gray-900 dark:text-white">{{ userProfile.full_name || userProfile.email }}</h2>
                <p class="text-gray-600 dark:text-gray-300 text-sm">{{ userProfile.email }}</p>
                <p v-if="userProfile.location" class="text-gray-500 dark:text-gray-400 text-sm mt-2">
                  <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  {{ userProfile.location }}
                </p>
              </div>

              <!-- User Stats -->
              <div class="border-t border-gray-200 dark:border-gray-600 pt-6">
                <div class="space-y-4">
                  <div class="flex items-center justify-between">
                    <span class="text-sm text-gray-600 dark:text-gray-400">Member Since</span>
                    <span class="text-sm font-medium text-gray-900 dark:text-white">{{ formatDate(userProfile.creation) }}</span>
                  </div>
                  <div v-if="userProfile.interest" class="flex items-center justify-between">
                    <span class="text-sm text-gray-600 dark:text-gray-400">Interests</span>
                    <span class="text-sm font-medium text-gray-900 dark:text-white">{{ userProfile.interest }}</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="text-sm text-gray-600 dark:text-gray-400">Account Status</span>
                    <span :class="userProfile.enabled ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'" class="text-sm font-medium">
                      {{ userProfile.enabled ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="border-t border-gray-200 dark:border-gray-600 pt-6 mt-6 space-y-3">
                <Button 
                  variant="solid" 
                  class="w-full"
                  @click="activeTab = 'profile'"
                >
                  <template #prefix>
                    <svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                  </template>
                  Edit Profile
                </Button>
                <Button 
                  variant="outline" 
                  class="w-full"
                  @click="activeTab = 'security'"
                >
                  <template #prefix>
                    <svg class="size-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                  </template>
                  Change Password
                </Button>
              </div>
            </div>
          </div>

          <!-- Main Content Area -->
          <div class="lg:col-span-2">
            <!-- Success/Error Messages -->
            <div v-if="successMessage" class="mb-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
              <div class="flex items-center">
                <svg class="w-5 h-5 text-green-600 dark:text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="text-green-800 dark:text-green-200">{{ successMessage }}</p>
              </div>
            </div>

            <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <div class="flex items-center">
                <svg class="w-5 h-5 text-red-600 dark:text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="text-red-800 dark:text-red-200">{{ errorMessage }}</p>
              </div>
            </div>

            <!-- Profile Edit Tab -->
            <div v-if="activeTab === 'profile'" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
              <div class="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Profile Information</h2>
                <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">Update your personal information and profile details</p>
              </div>
              
              <form @submit.prevent="updateProfile" class="p-6 space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <FormControl
                    type="text"
                    v-model="profileForm.first_name"
                    label="First Name"
                    placeholder="John"
                  />
                  <FormControl
                    type="text"
                    v-model="profileForm.last_name"
                    label="Last Name"
                    placeholder="Doe"
                  />
                </div>

                <FormControl
                  type="text"
                  v-model="profileForm.location"
                  label="Location"
                  placeholder="New York, USA"
                />

                <FormControl
                  type="text"
                  v-model="profileForm.interest"
                  label="Interests"
                  placeholder="Technology, Design, Innovation"
                />

                <FormControl
                  type="text"
                  v-model="profileForm.phone"
                  label="Phone"
                  placeholder="+1 234 567 8900"
                />

                <FormControl
                  type="text"
                  v-model="profileForm.mobile_no"
                  label="Mobile"
                  placeholder="+1 234 567 8900"
                />

                <Textarea
                  v-model="profileForm.bio"
                  label="Bio"
                  placeholder="Tell us about yourself..."
                  rows="4"
                />

                <div class="flex justify-end space-x-4">
                  <Button 
                    type="button"
                    variant="outline"
                    @click="resetProfileForm"
                  >
                    Cancel
                  </Button>
                  <Button 
                    type="submit"
                    variant="solid"
                    :loading="isUpdating"
                  >
                    Save Changes
                  </Button>
                </div>
              </form>
            </div>

            <!-- Security/Password Tab -->
            <div v-if="activeTab === 'security'" class="bg-white rounded-xl shadow-sm border border-gray-200">
              <div class="p-6 border-b border-gray-200">
                <h2 class="text-lg font-semibold text-gray-900">Change Password</h2>
                <p class="text-sm text-gray-600 mt-1">Update your password to keep your account secure</p>
              </div>
              
              <form @submit.prevent="changePassword" class="p-6 space-y-6">
                <FormControl
                  type="password"
                  v-model="passwordForm.old_password"
                  label="Current Password"
                  placeholder="Enter your current password"
                  required
                />

                <FormControl
                  type="password"
                  v-model="passwordForm.new_password"
                  label="New Password"
                  placeholder="Enter new password"
                  required
                />

                <FormControl
                  type="password"
                  v-model="passwordForm.confirm_password"
                  label="Confirm New Password"
                  placeholder="Confirm new password"
                  required
                />

                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 class="text-sm font-medium text-blue-900 mb-2">Password Requirements:</h4>
                  <ul class="text-sm text-blue-800 space-y-1">
                    <li>• At least 8 characters long</li>
                    <li>• Include uppercase and lowercase letters</li>
                    <li>• Include at least one number</li>
                    <li>• Include at least one special character</li>
                  </ul>
                </div>

                <div class="flex justify-end space-x-4">
                  <Button 
                    type="button"
                    variant="outline"
                    @click="resetPasswordForm"
                  >
                    Cancel
                  </Button>
                  <Button 
                    type="submit"
                    variant="solid"
                    :loading="isUpdatingPassword"
                  >
                    Update Password
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { call, Button, FormControl, Textarea } from 'frappe-ui'
import { session } from '../data/session'
import Navigation from '../components/Navigation.vue'

// Active tab
const activeTab = ref('profile')

// User profile data
const userProfile = ref({
  name: '',
  email: '',
  first_name: '',
  last_name: '',
  full_name: '',
  user_image: '',
  bio: '',
  location: '',
  interest: '',
  phone: '',
  mobile_no: '',
  birth_date: '',
  gender: '',
  enabled: true,
  creation: ''
})

// Profile form
const profileForm = ref({
  first_name: '',
  last_name: '',
  location: '',
  interest: '',
  phone: '',
  mobile_no: '',
  bio: ''
})

// Password form
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// Loading states
const isLoading = ref(false)
const isUpdating = ref(false)
const isUpdatingPassword = ref(false)

// Messages
const successMessage = ref('')
const errorMessage = ref('')

// Computed
const getUserInitials = computed(() => {
  if (userProfile.value.first_name && userProfile.value.last_name) {
    return userProfile.value.first_name.charAt(0) + userProfile.value.last_name.charAt(0)
  }
  if (userProfile.value.full_name) {
    const names = userProfile.value.full_name.split(' ')
    return names.length > 1 ? names[0].charAt(0) + names[1].charAt(0) : names[0].charAt(0)
  }
  return userProfile.value.email.charAt(0).toUpperCase()
})

// Load user profile
const loadUserProfile = async () => {
  isLoading.value = true
  try {
    const response = await call('ascra_frontend.api.get_user_profile')
    if (response && response.success) {
      userProfile.value = response.user
      // Populate profile form
      profileForm.value = {
        first_name: response.user.first_name || '',
        last_name: response.user.last_name || '',
        location: response.user.location || '',
        interest: response.user.interest || '',
        phone: response.user.phone || '',
        mobile_no: response.user.mobile_no || '',
        bio: response.user.bio || ''
      }
    }
  } catch (err) {
    console.error('Error loading user profile:', err)
    errorMessage.value = 'Failed to load user profile'
  } finally {
    isLoading.value = false
  }
}

// Update profile
const updateProfile = async () => {
  isUpdating.value = true
  successMessage.value = ''
  errorMessage.value = ''
  
  try {
    const response = await call('ascra_frontend.api.update_user_profile', {
      profile_data: JSON.stringify(profileForm.value)
    })
    
    if (response && response.success) {
      successMessage.value = 'Profile updated successfully!'
      userProfile.value = { ...userProfile.value, ...response.user }
      setTimeout(() => {
        successMessage.value = ''
      }, 5000)
    } else {
      errorMessage.value = response?.message || 'Failed to update profile'
    }
  } catch (err) {
    console.error('Error updating profile:', err)
    errorMessage.value = 'An error occurred while updating your profile'
  } finally {
    isUpdating.value = false
  }
}

// Change password
const changePassword = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  
  // Validate passwords match
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    errorMessage.value = 'New passwords do not match'
    return
  }
  
  // Validate password strength
  if (passwordForm.value.new_password.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters long'
    return
  }
  
  isUpdatingPassword.value = true
  
  try {
    const response = await call('ascra_frontend.api.update_password', {
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    })
    
    if (response && response.success) {
      successMessage.value = 'Password updated successfully!'
      resetPasswordForm()
      setTimeout(() => {
        successMessage.value = ''
      }, 5000)
    } else {
      errorMessage.value = response?.message || 'Failed to update password'
    }
  } catch (err) {
    console.error('Error updating password:', err)
    errorMessage.value = 'An error occurred while updating your password'
  } finally {
    isUpdatingPassword.value = false
  }
}

// Reset forms
const resetProfileForm = () => {
  profileForm.value = {
    first_name: userProfile.value.first_name || '',
    last_name: userProfile.value.last_name || '',
    location: userProfile.value.location || '',
    interest: userProfile.value.interest || '',
    phone: userProfile.value.phone || '',
    mobile_no: userProfile.value.mobile_no || '',
    bio: userProfile.value.bio || ''
  }
  successMessage.value = ''
  errorMessage.value = ''
}

const resetPasswordForm = () => {
  passwordForm.value = {
    old_password: '',
    new_password: '',
    confirm_password: ''
  }
  successMessage.value = ''
  errorMessage.value = ''
}

// Format date
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

// Initialize
onMounted(() => {
  loadUserProfile()
})
</script>
