<template>
  <nav class="bg-white shadow-md fixed w-full top-0 z-50 border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex-shrink-0 flex items-center">
            <div v-if="companyInfo?.logo && !logoError" class="h-10 w-auto max-w-[120px] flex items-center">
              <img 
                :src="companyInfo.logo" 
                :alt="companyInfo.company_name || 'Company Logo'"
                class="h-full w-auto object-contain max-h-10"
                @error="handleLogoError"
              />
            </div>
            <div v-else class="h-10 w-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-lg">{{ getCompanyInitials() }}</span>
            </div>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-1">
          <router-link 
            to="/" 
            class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition-colors"
          >
            Home
          </router-link>
          
          <a 
            @click="navigateToSection('services')" 
            class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition-colors cursor-pointer"
          >
            Services
          </a>
          
          <router-link 
            to="/erpnext" 
            class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition-colors"
          >
            ERPNext
          </router-link>
          
          <a 
            @click="navigateToSection('portfolio')" 
            class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition-colors cursor-pointer"
          >
            Portfolio
          </a>
          
          <a 
            @click="navigateToSection('about')" 
            class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition-colors cursor-pointer"
          >
            About
          </a>
          
          <a 
            @click="navigateToSection('contact')" 
            class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition-colors cursor-pointer"
          >
            Contact
          </a>
        </div>

        <!-- Right Side Actions -->
        <div class="flex items-center space-x-3">
          <!-- Notifications (for logged in users) -->
          <button 
            v-if="session.isLoggedIn"
            class="p-2 text-gray-600 hover:text-blue-600 hover:bg-gray-50 rounded-lg transition-colors relative"
            @click="showNotifications = !showNotifications"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
            </svg>
            <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          <!-- Help Dropdown -->
          <Dropdown :options="helpMenuOptions" v-if="session.isLoggedIn">
            <template #default="{ open }">
              <button class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 rounded-lg transition-colors flex items-center space-x-1">
                <span>Help</span>
                <svg class="w-4 h-4" :class="{ 'rotate-180': open }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
            </template>
          </Dropdown>

          <!-- User Menu Dropdown (for logged in users) -->
          <Dropdown :options="userMenuOptions" v-if="session.isLoggedIn">
            <template #default="{ open }">
              <button class="flex items-center space-x-2 px-2 py-1 rounded-lg hover:bg-gray-50 transition-colors">
                <Avatar 
                  :label="getUserInitials(session.user)" 
                  :image="userProfile?.user_image"
                  size="sm"
                  class="w-8 h-8"
                />
                <svg class="w-4 h-4 text-gray-600" :class="{ 'rotate-180': open }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
            </template>
          </Dropdown>

          <!-- Login/Signup Buttons (for guests) -->
          <div v-else class="flex items-center space-x-2">
            <router-link to="/account/login">
              <Button theme="gray" variant="outline" size="sm">
                Login
              </Button>
            </router-link>
            <router-link to="/account/signup">
              <Button theme="blue" variant="solid" size="sm">
                Sign Up
              </Button>
            </router-link>
          </div>

          <!-- Mobile Menu Button -->
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen" 
            class="md:hidden p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-50"
          >
            <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200 bg-white">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link 
          to="/" 
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
          @click="mobileMenuOpen = false"
        >
          Home
        </router-link>
        <a 
          @click="navigateToSection('services'); mobileMenuOpen = false" 
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 cursor-pointer"
        >
          Services
        </a>
        <router-link 
          to="/erpnext" 
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
          @click="mobileMenuOpen = false"
        >
          ERPNext
        </router-link>
        <a 
          @click="navigateToSection('portfolio'); mobileMenuOpen = false" 
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 cursor-pointer"
        >
          Portfolio
        </a>
        <a 
          @click="navigateToSection('about'); mobileMenuOpen = false" 
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 cursor-pointer"
        >
          About
        </a>
        <a 
          @click="navigateToSection('contact'); mobileMenuOpen = false" 
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 cursor-pointer"
        >
          Contact
        </a>

        <!-- Mobile User Menu -->
        <div v-if="session.isLoggedIn" class="border-t border-gray-200 pt-4 mt-4">
          <div class="flex items-center px-3 py-2 mb-2">
            <Avatar 
              :label="getUserInitials(session.user)" 
              :image="userProfile?.user_image"
              size="md"
              class="w-10 h-10"
            />
            <div class="ml-3">
              <div class="text-sm font-medium text-gray-900">{{ userProfile?.full_name || session.user }}</div>
              <div class="text-xs text-gray-500">{{ session.user }}</div>
            </div>
          </div>
          <router-link 
            to="/my-account" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
            @click="mobileMenuOpen = false"
          >
            My Account
          </router-link>
          <a 
            href="/app" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
          >
            Open Desk
          </a>
          <router-link 
            v-if="userRoles.is_employee" 
            to="/employee-dashboard" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
            @click="mobileMenuOpen = false"
          >
            Employee Dashboard
          </router-link>
          <button 
            @click="handleLogout" 
            class="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-red-600 hover:bg-red-50"
          >
            Log out
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { call, Button, Dropdown, Avatar } from 'frappe-ui'
import { session } from '../data/session'
import { usePWA } from '@/composables/usePWA'

const router = useRouter()
const pwa = usePWA()

// State
const mobileMenuOpen = ref(false)
const showSearchModal = ref(false)
const showNotifications = ref(false)
const companyInfo = ref(null)
const logoError = ref(false)
const userProfile = ref(null)
const userRoles = ref({
  is_employee: false
})

// User menu options
const userMenuOptions = computed(() => [
  {
    label: 'My Profile',
    icon: 'user',
    onClick: () => router.push('/my-account')
  },
  {
    label: 'My Settings',
    icon: 'settings',
    onClick: () => router.push('/my-account')
  },
  {
    label: 'Session Defaults',
    icon: 'sliders',
    onClick: () => window.location.href = '/app/user'
  },
  { label: '', component: 'divider' },
  {
    label: 'Employee Dashboard',
    icon: 'briefcase',
    onClick: () => router.push('/employee-dashboard'),
    condition: () => userRoles.value.is_employee
  }, 
  {
    label: 'Open Desk',
    icon: 'layout',
    onClick: () => window.location.href = '/app'
  },
  {
    label: 'View Website',
    icon: 'globe',
    onClick: () => router.push('/')
  },
  { label: '', component: 'divider' },
  {
    label: 'Log out',
    icon: 'log-out',
    onClick: handleLogout
  }
])

// Help menu options
const helpMenuOptions = computed(() => [
  {
    label: 'Documentation',
    icon: 'book',
    onClick: () => window.open('https://docs.erpnext.com', '_blank')
  },
  {
    label: 'Community Forum',
    icon: 'message-circle',
    onClick: () => window.open('https://discuss.frappe.io', '_blank')
  },
  {
    label: 'Report an Issue',
    icon: 'alert-circle',
    onClick: () => window.open('https://github.com/frappe/erpnext/issues', '_blank')
  },
  { label: '', component: 'divider' },
  {
    label: 'Install App',
    icon: 'download',
    onClick: () => pwa.install(),
    condition: () => pwa.isInstallable && session.isLoggedIn
  },
  {
    label: 'Keyboard Shortcuts',
    icon: 'command',
    onClick: () => alert('Ctrl+G: Search\nCtrl+K: Quick Actions')
  }
])

// Load company info
const loadCompanyInfo = async () => {
  try {
    const response = await call('ascra_frontend.api.get_company_info')
    if (response && response.success) {
      companyInfo.value = response.company
    }
  } catch (err) {
    console.error('Error loading company info:', err)
  }
}

// Load user profile
const loadUserProfile = async () => {
  if (!session.isLoggedIn) return
  
  try {
    const response = await call('ascra_frontend.api.get_user_profile')
    if (response && response.success) {
      userProfile.value = response.user
    }
  } catch (err) {
    console.error('Error loading user profile:', err)
  }
}

// Check user roles
const checkUserRoles = async () => {
  if (!session.isLoggedIn) return
  
  try {
    const response = await call('ascra_frontend.api.check_user_roles')
    if (response && response.success) {
      userRoles.value = response.roles
    }
  } catch (err) {
    console.error('Error checking user roles:', err)
  }
}

// Handle logo error
const handleLogoError = () => {
  logoError.value = true
}

// Get company initials
const getCompanyInitials = () => {
  if (companyInfo.value?.company_name) {
    return companyInfo.value.company_name
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }
  return 'AC'
}

// Get user initials
const getUserInitials = (email) => {
  if (!email) return 'U'
  const name = email.split('@')[0]
  return name.charAt(0).toUpperCase()
}

// Navigate to section
const navigateToSection = (sectionId) => {
  if (router.currentRoute.value.path !== '/') {
    router.push('/').then(() => {
      setTimeout(() => {
        const element = document.getElementById(sectionId)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' })
        }
      }, 100)
    })
  } else {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }
}

// Handle logout
const handleLogout = () => {
  session.logout.submit()
}

// Initialize
onMounted(() => {
  loadCompanyInfo()
  if (session.isLoggedIn) {
    loadUserProfile()
    checkUserRoles()
  }
})
</script>
