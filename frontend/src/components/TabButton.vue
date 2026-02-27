<template>
  <button
    @click="$emit('click')"
    :class="[
      'py-4 px-3 border-b-2 font-medium text-sm whitespace-nowrap transition-colors duration-200',
      active
        ? 'border-blue-500 text-blue-600 bg-blue-50'
        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 hover:bg-gray-50'
    ]"
  >
    {{ label }}
  </button>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    required: true
  },
  active: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>
