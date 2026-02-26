<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <Navigation />
    
    <!-- Dashboard Content -->
    <div id="dashboard" class="pt-20 pb-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">
            Welcome back, {{ userDisplayName }}!
          </h1>
          <p class="text-gray-600 mt-2">
            Here's your personalized dashboard with project insights and quick actions.
          </p>
        </div>

        <!-- Quick Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div class="flex items-center">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Active Projects</p>
                <p class="text-2xl font-bold text-gray-900">{{ stats.activeProjects }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div class="flex items-center">
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Completed Tasks</p>
                <p class="text-2xl font-bold text-gray-900">{{ stats.completedTasks }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div class="flex items-center">
              <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Revenue</p>
                <p class="text-2xl font-bold text-gray-900">${{ stats.revenue.toLocaleString() }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div class="flex items-center">
              <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Team Members</p>
                <p class="text-2xl font-bold text-gray-900">{{ stats.teamMembers }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Recent Projects -->
          <div class="lg:col-span-2">
            <div class="bg-white rounded-xl shadow-sm border border-gray-200">
              <div class="p-6 border-b border-gray-200">
                <div class="flex items-center justify-between">
                  <h2 class="text-lg font-semibold text-gray-900">Recent Projects</h2>
                  <Button theme="blue" variant="outline" size="sm">
                    View All
                  </Button>
                </div>
              </div>
              <div class="p-6">
                <div v-if="projects.loading" class="text-center py-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p class="text-gray-600 mt-2">Loading projects...</p>
                </div>
                <div v-else-if="projects.error" class="text-center py-8">
                  <p class="text-red-600">Failed to load projects</p>
                </div>
                <div v-else class="space-y-4">
                  <div v-for="project in recentProjects" :key="project.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div class="flex items-center space-x-4">
                      <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white font-semibold">
                        {{ project.name.charAt(0) }}
                      </div>
                      <div>
                        <h3 class="font-medium text-gray-900">{{ project.name }}</h3>
                        <p class="text-sm text-gray-600">{{ project.description }}</p>
                      </div>
                    </div>
                    <div class="text-right">
                      <span :class="getStatusClass(project.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                        {{ project.status }}
                      </span>
                      <p class="text-sm text-gray-600 mt-1">{{ project.progress }}% complete</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions & Activity -->
          <div class="space-y-8">
            <!-- Quick Actions -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-200">
              <div class="p-6 border-b border-gray-200">
                <h2 class="text-lg font-semibold text-gray-900">Quick Actions</h2>
              </div>
              <div class="p-6 space-y-3">
                <Button theme="blue" variant="solid" class="w-full justify-start" @click="createProject">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  New Project
                </Button>
                <Button theme="green" variant="outline" class="w-full justify-start" @click="navigateToServices">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                  View Services
                </Button>
                <Button theme="purple" variant="outline" class="w-full justify-start" @click="navigateToPortfolio">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                  </svg>
                  View Portfolio
                </Button>
                <Button theme="orange" variant="outline" class="w-full justify-start" @click="navigateToContact">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  Contact Us
                </Button>
              </div>
            </div>

            <!-- Recent Activity -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-200">
              <div class="p-6 border-b border-gray-200">
                <h2 class="text-lg font-semibold text-gray-900">Recent Activity</h2>
              </div>
              <div class="p-6">
                <div class="space-y-4">
                  <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-3">
                    <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                      </svg>
                    </div>
                    <div class="flex-1">
                      <p class="text-sm text-gray-900">{{ activity.description }}</p>
                      <p class="text-xs text-gray-600 mt-1">{{ activity.time }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import { session } from '../data/session'
import Navigation from '../components/Navigation.vue'

// User display name
const userDisplayName = computed(() => {
  if (!session.user) return 'User'
  const name = session.user.split('@')[0]
  return name.charAt(0).toUpperCase() + name.slice(1)
})

// Mock stats data (replace with real API calls)
const stats = ref({
  activeProjects: 8,
  completedTasks: 142,
  revenue: 85000,
  teamMembers: 12
})

// Projects resource
const projects = createResource({
  url: 'ping', // Replace with actual projects endpoint
  auto: true,
  onSuccess(data) {
    console.log('Projects loaded:', data)
  },
  onError(error) {
    console.error('Failed to load projects:', error)
  }
})

// Mock project data (replace with real data from projects resource)
const recentProjects = ref([
  {
    id: 1,
    name: 'E-commerce Platform',
    description: 'Modern online shopping experience',
    status: 'In Progress',
    progress: 75
  },
  {
    id: 2,
    name: 'Mobile Banking App',
    description: 'Secure financial transactions',
    status: 'Review',
    progress: 90
  },
  {
    id: 3,
    name: 'Analytics Dashboard',
    description: 'Business intelligence platform',
    status: 'Planning',
    progress: 25
  }
])

// Mock activity data
const recentActivity = ref([
  {
    id: 1,
    description: 'Completed user authentication module',
    time: '2 hours ago'
  },
  {
    id: 2,
    description: 'Updated project timeline for Q2',
    time: '4 hours ago'
  },
  {
    id: 3,
    description: 'Client meeting scheduled for tomorrow',
    time: '1 day ago'
  },
  {
    id: 4,
    description: 'Code review completed for payment gateway',
    time: '2 days ago'
  }
])

// Helper functions
const getStatusClass = (status) => {
  const classes = {
    'In Progress': 'bg-blue-100 text-blue-800',
    'Review': 'bg-yellow-100 text-yellow-800',
    'Planning': 'bg-gray-100 text-gray-800',
    'Completed': 'bg-green-100 text-green-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

// Navigation functions
import { useRouter } from 'vue-router'
const router = useRouter()

const navigateToServices = () => {
  router.push('/#services')
}

const navigateToPortfolio = () => {
  router.push('/#portfolio')
}

const navigateToContact = () => {
  router.push('/#contact')
}

// Action handlers
const createProject = () => {
  console.log('Create new project')
  // Implement project creation logic
}

// Initialize dashboard data
onMounted(() => {
  console.log('Dashboard mounted for user:', session.user)
})
</script>
