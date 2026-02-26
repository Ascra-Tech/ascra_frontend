<template>
  <nav class="bg-white shadow-lg fixed w-full top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <div class="flex-shrink-0 flex items-center">
            <div class="h-8 w-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-lg">A</span>
            </div>
            <span class="ml-2 text-xl font-bold text-gray-900">Ascratech</span>
          </div>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <router-link v-if="session.isLoggedIn" to="/dashboard" class="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
            Dashboard
          </router-link>
          <router-link v-else to="/" class="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
            Home
          </router-link>
          
          <a @click="navigateToSection('services')" class="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors cursor-pointer">
            Services
          </a>
          <a @click="navigateToSection('portfolio')" class="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors cursor-pointer">
            Portfolio
          </a>
          <a @click="navigateToSection('about')" class="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors cursor-pointer">
            About
          </a>
          <a @click="navigateToSection('contact')" class="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors cursor-pointer">
            Contact
          </a>
          
          <!-- Authentication Section -->
          <div v-if="session.isLoggedIn" class="flex items-center space-x-4 ml-4">
            <router-link v-if="userRoles.is_employee" to="/employee-dashboard" class="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors bg-blue-50 rounded-lg">
              Employee Dashboard
            </router-link>
            <div class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                {{ getUserInitials(session.user) }}
              </div>
              <span class="text-sm text-gray-700">{{ session.user }}</span>
            </div>
            <Button theme="gray" variant="outline" @click="handleLogout" :loading="session.logout.loading">
              Logout
            </Button>
          </div>
          
          <div v-else class="flex items-center space-x-4 ml-4">
            <router-link to="/account/login">
              <Button theme="gray" variant="outline">
                Login
              </Button>
            </router-link>
            <router-link to="/account/signup">
              <Button theme="blue" variant="solid">
                Sign Up
              </Button>
            </router-link>
          </div>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="text-gray-700 hover:text-blue-600 focus:outline-none focus:text-blue-600">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <div v-show="mobileMenuOpen" class="md:hidden bg-white border-t border-gray-200">
      <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
        <router-link v-if="session.isLoggedIn" to="/dashboard" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-blue-600 px-3 py-2 text-base font-medium">
          Dashboard
        </router-link>
        <router-link v-else to="/" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-blue-600 px-3 py-2 text-base font-medium">
          Home
        </router-link>
        
        <a @click="navigateToSectionMobile('services')" class="block text-gray-700 hover:text-blue-600 px-3 py-2 text-base font-medium cursor-pointer">
          Services
        </a>
        <a @click="navigateToSectionMobile('portfolio')" class="block text-gray-700 hover:text-blue-600 px-3 py-2 text-base font-medium cursor-pointer">
          Portfolio
        </a>
        <a @click="navigateToSectionMobile('about')" class="block text-gray-700 hover:text-blue-600 px-3 py-2 text-base font-medium cursor-pointer">
          About
        </a>
        <a @click="navigateToSectionMobile('contact')" class="block text-gray-700 hover:text-blue-600 px-3 py-2 text-base font-medium cursor-pointer">
          Contact
        </a>
        
        <!-- Mobile Authentication Section -->
        <div v-if="session.isLoggedIn" class="border-t border-gray-200 pt-3">
          <router-link v-if="userRoles.is_employee" to="/employee-dashboard" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-blue-600 px-3 py-2 text-base font-medium bg-blue-50 rounded-lg mx-3 mb-3">
            Employee Dashboard
          </router-link>
          <div class="flex items-center px-3 py-2">
            <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm font-semibold mr-3">
              {{ getUserInitials(session.user) }}
            </div>
            <span class="text-sm text-gray-700">{{ session.user }}</span>
          </div>
          <div class="px-3 py-2">
            <Button theme="gray" variant="outline" class="w-full" @click="handleLogout" :loading="session.logout.loading">
              Logout
            </Button>
          </div>
        </div>
        
        <div v-else class="border-t border-gray-200 pt-3">
          <div class="px-3 py-2 space-y-2">
            <router-link to="/account/login" @click="mobileMenuOpen = false">
              <Button theme="gray" variant="outline" class="w-full">
                Login
              </Button>
            </router-link>
            <router-link to="/account/signup" @click="mobileMenuOpen = false">
              <Button theme="blue" variant="solid" class="w-full">
                Sign Up
              </Button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { call } from 'frappe-ui'
import { session } from '../data/session'

const mobileMenuOpen = ref(false)
const userRoles = ref({ roles: [], is_employee: false })

import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()

const navigateToSection = (sectionId) => {
  // If we're on dashboard, go to home with hash
  if (route.name === 'Dashboard') {
    router.push(`/#${sectionId}`)
  } else {
    // If we're on home, scroll to section
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    } else {
      // If element not found, navigate to home with hash
      router.push(`/#${sectionId}`)
    }
  }
}

const navigateToSectionMobile = (sectionId) => {
  mobileMenuOpen.value = false
  setTimeout(() => navigateToSection(sectionId), 100)
}

const scrollTo = (elementId) => {
  const element = document.getElementById(elementId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

const getUserInitials = (email) => {
  if (!email) return 'U'
  const name = email.split('@')[0]
  return name.charAt(0).toUpperCase()
}

const loadUserRoles = async () => {
  if (session.isLoggedIn) {
    try {
      const response = await call('ascra_frontend.api.get_user_roles')
      if (response.success) {
        userRoles.value = response
      }
    } catch (err) {
      console.error('Error loading user roles:', err)
      userRoles.value = { roles: [], is_employee: false }
    }
  } else {
    userRoles.value = { roles: [], is_employee: false }
  }
}

const handleLogout = () => {
  session.logout.submit()
}

// Watch for session changes to reload roles
watch(() => session.isLoggedIn, (newValue) => {
  if (newValue) {
    loadUserRoles()
  } else {
    userRoles.value = { roles: [], is_employee: false }
  }
})

// Load roles on mount
onMounted(() => {
  if (session.isLoggedIn) {
    loadUserRoles()
  }
})
</script>
