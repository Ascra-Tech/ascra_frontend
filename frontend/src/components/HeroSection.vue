<template>
  <section id="home" class="bg-gradient-to-br from-blue-50 via-white to-purple-50 pt-20 pb-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="lg:grid lg:grid-cols-12 lg:gap-8 items-center">
        <!-- Content -->
        <div class="lg:col-span-6">
          <div class="text-center lg:text-left">
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
              Welcome to
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                Ascratech
              </span>
              Solutions
            </h1>
            <p class="mt-6 text-xl text-gray-600 max-w-3xl">
              Your trusted partner for innovative technology solutions and business transformation. 
              We specialize in ERP systems, custom software development, and digital solutions that drive growth.
            </p>
            <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button theme="blue" variant="solid" size="lg" class="px-8 py-3">
                Start Your Project
              </Button>
              <Button theme="gray" variant="outline" size="lg" class="px-8 py-3">
                View Our Work
              </Button>
            </div>
            
            <!-- Stats -->
            <div class="mt-12 grid grid-cols-3 gap-8 text-center lg:text-left">
              <div>
                <div class="text-3xl font-bold text-blue-600">50+</div>
                <div class="text-sm text-gray-600">ERP Implementations</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-purple-600">100%</div>
                <div class="text-sm text-gray-600">Client Success Rate</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-green-600">24/7</div>
                <div class="text-sm text-gray-600">Support Available</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Hero Image/Animation -->
        <div class="mt-12 lg:mt-0 lg:col-span-6">
          <div class="relative">
            <!-- Floating Cards Animation -->
            <div class="relative h-96 lg:h-[500px]">
              <!-- Main Card -->
              <div class="absolute top-8 left-8 right-8 bg-white rounded-2xl shadow-2xl p-6 transform hover:scale-105 transition-transform duration-300">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                  <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                </div>
                <div class="space-y-3">
                  <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div class="h-4 bg-blue-200 rounded w-1/2"></div>
                  <div class="h-4 bg-purple-200 rounded w-2/3"></div>
                  <div class="h-20 bg-gradient-to-r from-blue-100 to-purple-100 rounded-lg"></div>
                </div>
              </div>

              <!-- Floating Elements -->
              <div class="absolute top-4 right-4 w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold shadow-lg animate-bounce">
                <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              
              <div class="absolute bottom-4 left-4 w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center text-white shadow-lg animate-pulse">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
                </svg>
              </div>

              <div class="absolute top-1/2 -right-2 w-8 h-8 bg-green-500 rounded-full shadow-lg animate-ping"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Hero section component for software agency landing page
</script>
