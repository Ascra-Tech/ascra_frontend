<template>
  <section id="portfolio" class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
          Our <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">Portfolio</span>
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Showcasing our latest projects and successful implementations across various industries
        </p>
      </div>

      <!-- Portfolio Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Project 1 -->
        <div class="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300">
          <div class="relative h-48 bg-gradient-to-br from-blue-400 to-blue-600 overflow-hidden">
            <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-white text-center">
                <svg class="w-16 h-16 mx-auto mb-4 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
                <h4 class="text-lg font-semibold">E-Commerce Platform</h4>
              </div>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Modern E-Commerce Solution</h3>
            <p class="text-gray-600 mb-4">
              Full-stack e-commerce platform with advanced inventory management, payment processing, and analytics dashboard.
            </p>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">React</span>
              <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">Node.js</span>
              <span class="px-3 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">MongoDB</span>
            </div>
            <Button theme="blue" variant="outline" size="sm" class="w-full">
              View Project
            </Button>
          </div>
        </div>

        <!-- Project 2 -->
        <div class="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300">
          <div class="relative h-48 bg-gradient-to-br from-purple-400 to-purple-600 overflow-hidden">
            <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-white text-center">
                <svg class="w-16 h-16 mx-auto mb-4 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a1 1 0 001-1V4a1 1 0 00-1-1H8a1 1 0 00-1 1v16a1 1 0 001 1z"/>
                </svg>
                <h4 class="text-lg font-semibold">Mobile Banking App</h4>
              </div>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Secure Banking Application</h3>
            <p class="text-gray-600 mb-4">
              Cross-platform mobile banking app with biometric authentication, real-time transactions, and financial insights.
            </p>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">React Native</span>
              <span class="px-3 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">Firebase</span>
              <span class="px-3 py-1 bg-red-100 text-red-800 text-xs rounded-full">Security</span>
            </div>
            <Button theme="purple" variant="outline" size="sm" class="w-full">
              View Project
            </Button>
          </div>
        </div>

        <!-- Project 3 -->
        <div class="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300">
          <div class="relative h-48 bg-gradient-to-br from-green-400 to-green-600 overflow-hidden">
            <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-white text-center">
                <svg class="w-16 h-16 mx-auto mb-4 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                </svg>
                <h4 class="text-lg font-semibold">Analytics Dashboard</h4>
              </div>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Business Intelligence Platform</h3>
            <p class="text-gray-600 mb-4">
              Real-time analytics dashboard with interactive charts, data visualization, and automated reporting features.
            </p>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">Vue.js</span>
              <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">D3.js</span>
              <span class="px-3 py-1 bg-orange-100 text-orange-800 text-xs rounded-full">Python</span>
            </div>
            <Button theme="green" variant="outline" size="sm" class="w-full">
              View Project
            </Button>
          </div>
        </div>

        <!-- Project 4 -->
        <div class="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300">
          <div class="relative h-48 bg-gradient-to-br from-pink-400 to-pink-600 overflow-hidden">
            <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-white text-center">
                <svg class="w-16 h-16 mx-auto mb-4 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
                <h4 class="text-lg font-semibold">Learning Management</h4>
              </div>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Online Learning Platform</h3>
            <p class="text-gray-600 mb-4">
              Comprehensive LMS with video streaming, interactive quizzes, progress tracking, and certification management.
            </p>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-3 py-1 bg-pink-100 text-pink-800 text-xs rounded-full">Angular</span>
              <span class="px-3 py-1 bg-indigo-100 text-indigo-800 text-xs rounded-full">Laravel</span>
              <span class="px-3 py-1 bg-gray-100 text-gray-800 text-xs rounded-full">MySQL</span>
            </div>
            <Button theme="pink" variant="outline" size="sm" class="w-full">
              View Project
            </Button>
          </div>
        </div>

        <!-- Project 5 -->
        <div class="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300">
          <div class="relative h-48 bg-gradient-to-br from-indigo-400 to-indigo-600 overflow-hidden">
            <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-white text-center">
                <svg class="w-16 h-16 mx-auto mb-4 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"/>
                </svg>
                <h4 class="text-lg font-semibold">Cloud Infrastructure</h4>
              </div>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Scalable Cloud Solution</h3>
            <p class="text-gray-600 mb-4">
              Enterprise cloud infrastructure with auto-scaling, load balancing, and comprehensive monitoring solutions.
            </p>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-3 py-1 bg-indigo-100 text-indigo-800 text-xs rounded-full">AWS</span>
              <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Docker</span>
              <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">Kubernetes</span>
            </div>
            <Button theme="indigo" variant="outline" size="sm" class="w-full">
              View Project
            </Button>
          </div>
        </div>

        <!-- Project 6 -->
        <div class="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300">
          <div class="relative h-48 bg-gradient-to-br from-orange-400 to-orange-600 overflow-hidden">
            <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-white text-center">
                <svg class="w-16 h-16 mx-auto mb-4 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
                <h4 class="text-lg font-semibold">IoT Platform</h4>
              </div>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Smart IoT Management</h3>
            <p class="text-gray-600 mb-4">
              IoT device management platform with real-time monitoring, data analytics, and automated control systems.
            </p>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-3 py-1 bg-orange-100 text-orange-800 text-xs rounded-full">MQTT</span>
              <span class="px-3 py-1 bg-red-100 text-red-800 text-xs rounded-full">Redis</span>
              <span class="px-3 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">InfluxDB</span>
            </div>
            <Button theme="orange" variant="outline" size="sm" class="w-full">
              View Project
            </Button>
          </div>
        </div>
      </div>

      <!-- Call to Action -->
      <div class="text-center mt-16">
        <Button theme="blue" variant="solid" size="lg" class="px-8 py-3">
          View All Projects
        </Button>
      </div>
    </div>
  </section>
</template>

<script setup>
// Portfolio section component
</script>
