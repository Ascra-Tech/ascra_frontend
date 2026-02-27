<template>
  <section id="contact" class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
          Get In <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">Touch</span>
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Ready to start your next project? Let's discuss how we can help bring your vision to life
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16">
        <!-- Contact Form -->
        <div class="bg-white rounded-2xl p-8 shadow-lg">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">Send us a message</h3>
          
          <!-- Success Message -->
          <div v-if="submitSuccess" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div class="flex items-center">
              <svg class="w-5 h-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <p class="text-green-800 font-medium">Thank you for your inquiry! We will get back to you soon.</p>
            </div>
          </div>
          
          <!-- Error Message -->
          <div v-if="submitError" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div class="flex items-center">
              <svg class="w-5 h-5 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <p class="text-red-800">{{ submitError }}</p>
            </div>
          </div>
          
          <form @submit.prevent="submitForm" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">First Name</label>
                <Input
                  v-model="form.firstName"
                  placeholder="John"
                  required
                  class="w-full"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
                <Input
                  v-model="form.lastName"
                  placeholder="Doe"
                  required
                  class="w-full"
                />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <Input
                v-model="form.email"
                type="email"
                placeholder="john@example.com"
                required
                class="w-full"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Phone *</label>
              <input
                v-model="form.phone"
                type="tel"
                placeholder="+1 (555) 123-4567"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Company *</label>
              <Input
                v-model="form.company"
                placeholder="Your Company"
                required
                class="w-full"
              />
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
                <Input
                  v-model="form.jobTitle"
                  placeholder="CEO, CTO, Manager, etc."
                  class="w-full"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Website</label>
                <Input
                  v-model="form.website"
                  type="url"
                  placeholder="https://yourcompany.com"
                  class="w-full"
                />
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">City</label>
                <Input
                  v-model="form.city"
                  placeholder="New York"
                  class="w-full"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">State</label>
                <Input
                  v-model="form.state"
                  placeholder="NY"
                  class="w-full"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Country</label>
                <Input
                  v-model="form.country"
                  placeholder="United States"
                  class="w-full"
                />
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                <select v-model="form.industry" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                  <option value="">Select Industry</option>
                  <option value="Technology">Technology</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Finance">Finance</option>
                  <option value="Education">Education</option>
                  <option value="Retail">Retail</option>
                  <option value="Manufacturing">Manufacturing</option>
                  <option value="Real Estate">Real Estate</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Company Size</label>
                <select v-model="form.noOfEmployees" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                  <option value="">Select Size</option>
                  <option value="1-10">1-10 employees</option>
                  <option value="11-50">11-50 employees</option>
                  <option value="51-200">51-200 employees</option>
                  <option value="201-500">201-500 employees</option>
                  <option value="501-1000">501-1000 employees</option>
                  <option value="1000+">1000+ employees</option>
                </select>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Project Type</label>
              <select v-model="form.projectType" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="">Select a service</option>
                <option value="Product Enquiry">Product Enquiry</option>
                <option value="Web Development">Web Development</option>
                <option value="Mobile Development">Mobile Development</option>
                <option value="Cloud Solutions">Cloud Solutions</option>
                <option value="UI/UX Design">UI/UX Design</option>
                <option value="API Development">API Development</option>
                <option value="Tech Consulting">Tech Consulting</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Message</label>
              <textarea
                v-model="form.message"
                rows="4"
                placeholder="Tell us about your project..."
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              ></textarea>
            </div>
            
            <Button 
              type="submit" 
              theme="blue" 
              variant="solid" 
              size="lg" 
              class="w-full"
              :loading="isSubmitting"
            >
              Send Message
            </Button>
          </form>
        </div>

        <!-- Contact Information -->
        <div class="space-y-8">
          <!-- Contact Cards -->
          <div class="bg-white rounded-2xl p-8 shadow-lg">
            <h3 class="text-2xl font-bold text-gray-900 mb-6">Reach Out to Our Office</h3>
            
            <div class="space-y-6">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900">Email</h4>
                  <p class="text-gray-600">connect@ascratech.com</p>
                  <p class="text-gray-600">careers@ascratech.com</p>
                </div>
              </div>
              
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900">Phone</h4>
                  <p class="text-gray-600">+91-9920536039</p>
                  <p class="text-gray-600">+91 95118 66889</p>
                </div>
              </div>
              
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900">India Office</h4>
                  <p class="text-gray-600">601, Nirmal Corporate Center</p>
                  <p class="text-gray-600">LBS Marg, Mulund West</p>
                  <p class="text-gray-600">Mumbai - 400080, India</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Business Hours -->
          <div class="bg-white rounded-2xl p-8 shadow-lg">
            <h3 class="text-xl font-bold text-gray-900 mb-6">Business Hours</h3>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">Monday - Friday</span>
                <span class="font-medium text-gray-900">9:00 AM - 6:00 PM</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Saturday</span>
                <span class="font-medium text-gray-900">10:00 AM - 4:00 PM</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Sunday</span>
                <span class="font-medium text-gray-900">Closed</span>
              </div>
            </div>
            <div class="mt-6 p-4 bg-blue-50 rounded-lg">
              <p class="text-sm text-blue-800">
                <strong>24/7 Support</strong> available for enterprise clients
              </p>
            </div>
          </div>

          <!-- Social Links -->
          <div class="bg-white rounded-2xl p-8 shadow-lg">
            <h3 class="text-xl font-bold text-gray-900 mb-6">Follow Us</h3>
            <div class="flex space-x-4">
              <a href="#" class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center hover:bg-blue-200 transition-colors">
                <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                </svg>
              </a>
              <a href="#" class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center hover:bg-blue-200 transition-colors">
                <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
              <a href="#" class="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center hover:bg-gray-200 transition-colors">
                <svg class="w-6 h-6 text-gray-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { call, Input, Button } from 'frappe-ui'

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  company: '',
  jobTitle: '',
  website: '',
  city: '',
  state: '',
  country: '',
  industry: '',
  noOfEmployees: '',
  annualRevenue: '',
  projectType: '',
  message: ''
})

const isSubmitting = ref(false)
const submitSuccess = ref(false)
const submitError = ref('')

const submitForm = async () => {
  isSubmitting.value = true
  submitError.value = ''
  
  try {
    // Prepare data for backend API
    const formData = {
      first_name: form.value.firstName,
      last_name: form.value.lastName,
      email: form.value.email,
      phone: form.value.phone,
      company_name: form.value.company,
      job_title: form.value.jobTitle,
      website: form.value.website,
      city: form.value.city,
      state: form.value.state,
      country: form.value.country,
      industry: form.value.industry,
      no_of_employees: form.value.noOfEmployees,
      annual_revenue: form.value.annualRevenue,
      request_type: form.value.projectType || 'Product Enquiry',
      message: form.value.message
    }
    
    // Call backend API to create Lead and Contact
    const response = await call('ascra_frontend.api.create_lead_and_contact', {
      data: JSON.stringify(formData)
    })
    
    if (response.success) {
      // Reset form
      form.value = {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        company: '',
        jobTitle: '',
        website: '',
        city: '',
        state: '',
        country: '',
        industry: '',
        noOfEmployees: '',
        annualRevenue: '',
        projectType: '',
        message: ''
      }
      
      submitSuccess.value = true
      setTimeout(() => {
        submitSuccess.value = false
      }, 5000)
    }
    
  } catch (error) {
    console.error('Form submission error:', error)
    submitError.value = error.message || 'There was an error sending your message. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>
