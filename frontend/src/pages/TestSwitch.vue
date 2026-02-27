<template>
  <div class="p-4">
    <h2>Testing Frappe UI Components</h2>
    
    <!-- Test Button (should work) -->
    <Button class="mr-2">Test Button</Button>
    
    <!-- Test Switch (might not work) -->
    <Switch v-model="isTestSwitch" class="mr-2" />
    
    <!-- Debug info -->
    <div class="mt-4">
      <p>Switch value: {{ isTestSwitch }}</p>
      <p>Available components: {{ Object.keys(frappeUIComponents).join(', ') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import * as frappeUIComponents from 'frappe-ui'

const isTestSwitch = ref(false)

console.log('Available Frappe UI components:', Object.keys(frappeUIComponents))
</script>
