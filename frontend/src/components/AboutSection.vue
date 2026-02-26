<template>
  <section id="about" class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
          About <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">Ascratech</span>
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          We are a passionate team of developers, designers, and strategists dedicated to creating exceptional digital experiences
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <!-- Content -->
        <div>
          <h3 class="text-2xl font-bold text-gray-900 mb-6">
            Transforming Ideas into Digital Reality
          </h3>
          <p class="text-gray-600 mb-6">
            Founded with a vision to bridge the gap between innovative ideas and cutting-edge technology, 
            Ascratech has been at the forefront of digital transformation for businesses across various industries.
          </p>
          <p class="text-gray-600 mb-8">
            Our team combines technical expertise with creative thinking to deliver solutions that not only 
            meet your current needs but also scale with your future growth. We believe in building long-term 
            partnerships with our clients, ensuring their success in the digital landscape.
          </p>

          <!-- Values -->
          <div class="space-y-4">
            <div class="flex items-start space-x-4">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h4 class="font-semibold text-gray-900">Innovation First</h4>
                <p class="text-gray-600">We stay ahead of technology trends to deliver cutting-edge solutions</p>
              </div>
            </div>
            
            <div class="flex items-start space-x-4">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                </svg>
              </div>
              <div>
                <h4 class="font-semibold text-gray-900">Client-Centric</h4>
                <p class="text-gray-600">Your success is our priority, and we tailor solutions to your unique needs</p>
              </div>
            </div>
            
            <div class="flex items-start space-x-4">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h4 class="font-semibold text-gray-900">Quality Assured</h4>
                <p class="text-gray-600">We maintain the highest standards in code quality and project delivery</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Team Stats & Image -->
        <div>
          <div class="bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl p-8 mb-8">
            <div class="grid grid-cols-2 gap-8 text-center">
              <div>
                <div class="text-3xl font-bold text-blue-600 mb-2">15+</div>
                <div class="text-sm text-gray-600">Expert Developers</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-purple-600 mb-2">50+</div>
                <div class="text-sm text-gray-600">Technologies</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-green-600 mb-2">24/7</div>
                <div class="text-sm text-gray-600">Support</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-orange-600 mb-2">100%</div>
                <div class="text-sm text-gray-600">Commitment</div>
              </div>
            </div>
          </div>

          <!-- Team Avatars -->
          <div class="bg-white rounded-2xl p-8 shadow-lg">
            <h4 class="text-lg font-semibold text-gray-900 mb-6 text-center">Meet Our Team</h4>
            <div class="flex justify-center space-x-4 mb-6">
              <div class="w-12 h-12 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                AK
              </div>
              <div class="w-12 h-12 bg-gradient-to-r from-purple-400 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold">
                SM
              </div>
              <div class="w-12 h-12 bg-gradient-to-r from-green-400 to-green-600 rounded-full flex items-center justify-center text-white font-semibold">
                RJ
              </div>
              <div class="w-12 h-12 bg-gradient-to-r from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white font-semibold">
                NK
              </div>
              <div class="w-12 h-12 bg-gradient-to-r from-pink-400 to-pink-600 rounded-full flex items-center justify-center text-white font-semibold">
                +10
              </div>
            </div>
            <p class="text-center text-gray-600 text-sm">
              Passionate professionals from around the world
            </p>
          </div>
        </div>
      </div>

      <!-- Technologies -->
      <div class="mt-20">
        <h3 class="text-2xl font-bold text-gray-900 text-center mb-12">
          Technologies We Master
        </h3>
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-8 items-center opacity-60">
          <!-- Tech logos as text badges -->
          <div class="text-center">
            <div class="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center mx-auto mb-2">
              <span class="text-blue-600 font-bold text-sm">React</span>
            </div>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-green-100 rounded-xl flex items-center justify-center mx-auto mb-2">
              <span class="text-green-600 font-bold text-sm">Vue</span>
            </div>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-yellow-100 rounded-xl flex items-center justify-center mx-auto mb-2">
              <span class="text-yellow-600 font-bold text-sm">JS</span>
            </div>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center mx-auto mb-2">
              <span class="text-blue-600 font-bold text-sm">Node</span>
            </div>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-red-100 rounded-xl flex items-center justify-center mx-auto mb-2">
              <span class="text-red-600 font-bold text-sm">Angular</span>
            </div>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-purple-100 rounded-xl flex items-center justify-center mx-auto mb-2">
              <span class="text-purple-600 font-bold text-sm">PHP</span>
            </div>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center mx-auto mb-2">
              <span class="text-blue-600 font-bold text-sm">Python</span>
            </div>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-orange-100 rounded-xl flex items-center justify-center mx-auto mb-2">
              <span class="text-orange-600 font-bold text-sm">AWS</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// About section component
</script>
