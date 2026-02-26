<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <!-- Navigation -->
    <Navigation />
    
    <div class="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 pt-20">
    <!-- Background Pattern -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full opacity-10 blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full opacity-10 blur-3xl"></div>
    </div>

    <div class="relative max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
            </svg>
          </div>
        </div>
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Create your account</h2>
        <p class="text-gray-600">Join Ascra and start building amazing projects</p>
      </div>

      <!-- Sign Up Form -->
      <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <form class="space-y-6" @submit.prevent="submit">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <Input
                required
                name="first_name"
                type="text"
                placeholder="John"
                label="First Name"
                class="w-full"
              />
            </div>
            <div>
              <Input
                required
                name="last_name"
                type="text"
                placeholder="Doe"
                label="Last Name"
                class="w-full"
              />
            </div>
          </div>
          
          <div>
            <Input
              required
              name="email"
              type="email"
              placeholder="john.doe@example.com"
              label="Email Address"
              class="w-full"
            />
          </div>

          <div>
            <Input
              required
              name="password"
              type="password"
              placeholder="Create a strong password"
              label="Password"
              class="w-full"
            />
            <p class="mt-1 text-xs text-gray-500">
              Password must be at least 8 characters long
            </p>
          </div>

          <div>
            <Input
              required
              name="confirm_password"
              type="password"
              placeholder="Confirm your password"
              label="Confirm Password"
              class="w-full"
            />
          </div>

          <div>
            <Input
              name="company"
              type="text"
              placeholder="Your company name (optional)"
              label="Company"
              class="w-full"
            />
          </div>

          <div class="flex items-start">
            <div class="flex items-center h-5">
              <input 
                id="terms" 
                name="terms" 
                type="checkbox" 
                required
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              >
            </div>
            <div class="ml-3 text-sm">
              <label for="terms" class="text-gray-700">
                I agree to the 
                <a href="#" class="font-medium text-blue-600 hover:text-blue-500">Terms of Service</a> 
                and 
                <a href="#" class="font-medium text-blue-600 hover:text-blue-500">Privacy Policy</a>
              </label>
            </div>
          </div>

          <div>
            <Button 
              type="submit"
              :loading="signupLoading" 
              theme="blue" 
              variant="solid" 
              class="w-full py-3 text-base font-medium"
            >
              Create Account
            </Button>
          </div>

          <!-- Success Message -->
          <div v-if="signupSuccess" class="rounded-md bg-green-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-green-800">
                  Account created successfully!
                </h3>
                <div class="mt-2 text-sm text-green-700">
                  <p>You can now login with your email and password. You'll be redirected to the login page shortly.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="signupError" class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  Registration failed
                </h3>
                <div class="mt-2 text-sm text-red-700">
                  <p>{{ signupError }}</p>
                </div>
              </div>
            </div>
          </div>
        </form>

        <!-- Login Link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Already have an account?
            <router-link to="/account/login" class="font-medium text-blue-600 hover:text-blue-500 transition-colors">
              Sign in here
            </router-link>
          </p>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center">
        <p class="text-xs text-gray-500">
          By creating an account, you agree to our 
          <a href="#" class="text-blue-600 hover:text-blue-500">Terms of Service</a> and 
          <a href="#" class="text-blue-600 hover:text-blue-500">Privacy Policy</a>
        </p>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { call } from 'frappe-ui'
import { useRouter } from 'vue-router'
import Navigation from '../components/Navigation.vue'

const router = useRouter()

// Form state
const signupLoading = ref(false)
const signupSuccess = ref(false)
const signupError = ref('')

function validateForm(formData) {
  const email = formData.get('email')
  const password = formData.get('password')
  const confirmPassword = formData.get('confirm_password')
  const firstName = formData.get('first_name')
  const lastName = formData.get('last_name')

  // Basic validation
  if (!firstName || !lastName || !email || !password) {
    return 'Please fill in all required fields.'
  }

  if (password.length < 8) {
    return 'Password must be at least 8 characters long.'
  }

  if (password !== confirmPassword) {
    return 'Passwords do not match.'
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    return 'Please enter a valid email address.'
  }

  return null
}

async function submit(e) {
  const formData = new FormData(e.target)
  
  // Reset states
  signupError.value = ''
  signupSuccess.value = false
  
  // Validate form
  const validationError = validateForm(formData)
  if (validationError) {
    signupError.value = validationError
    return
  }

  // Check terms acceptance
  if (!formData.get('terms')) {
    signupError.value = 'Please accept the Terms of Service and Privacy Policy.'
    return
  }

  signupLoading.value = true

  try {
    // Submit signup request using our custom API
    const response = await call('ascra_frontend.api.create_user_account', {
      email: formData.get('email'),
      first_name: formData.get('first_name'),
      last_name: formData.get('last_name'),
      password: formData.get('password'),
      company: formData.get('company') || null
    })

    signupLoading.value = false
    signupSuccess.value = true
    signupError.value = ''
    
    console.log('Signup successful:', response)
    
    // Redirect to login after 3 seconds
    setTimeout(() => {
      router.push('/account/login')
    }, 3000)
    
  } catch (error) {
    signupLoading.value = false
    signupSuccess.value = false
    signupError.value = error.message || 'An error occurred during registration. Please try again.'
    console.error('Signup error:', error)
  }
}
</script>
