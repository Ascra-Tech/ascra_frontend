<template>
  <div class="space-y-4">
    <!-- Upload Area -->
    <div 
      @click="triggerFileInput"
      @dragover.prevent="dragOver = true"
      @dragleave.prevent="dragOver = false"
      @drop.prevent="handleDrop"
      :class="[
        'border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors',
        dragOver ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
      ]"
    >
      <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
      </svg>
      
      <div class="flex flex-col items-center">
        <p class="text-sm text-gray-600 mb-2">
          <span class="font-medium">Click to upload</span> or drag and drop
        </p>
        <p class="text-xs text-gray-500">
          {{ acceptTypes }} (Max {{ maxSize }}MB)
        </p>
      </div>
      
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        :multiple="multiple"
        @change="handleFileSelect"
        class="hidden"
      />
    </div>

    <!-- File List -->
    <div v-if="files.length > 0" class="space-y-2">
      <h4 class="text-sm font-medium text-gray-900">Uploaded Files</h4>
      
      <div v-for="(file, index) in files" :key="index" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
        <div class="flex items-center space-x-3 flex-1 min-w-0">
          <div class="flex-shrink-0">
            <div v-if="file.type.startsWith('image/')" class="w-10 h-10 bg-gray-200 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
            </div>
            <div v-else-if="file.type === 'application/pdf'" class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
              </svg>
            </div>
            <div v-else class="w-10 h-10 bg-gray-200 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
          </div>
          
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">{{ file.name }}</p>
            <p class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-2">
          <span v-if="file.uploaded" class="text-xs text-green-600 font-medium">Uploaded</span>
          <span v-else-if="file.uploading" class="text-xs text-blue-600 font-medium">Uploading...</span>
          <span v-else-if="file.error" class="text-xs text-red-600 font-medium">Error</span>
          
          <button 
            @click="removeFile(index)"
            class="text-red-500 hover:text-red-700 transition-colors"
            :disabled="file.uploading"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div v-if="uploading" class="w-full bg-gray-200 rounded-full h-2">
      <div 
        :style="{ width: uploadProgress + '%' }"
        class="bg-blue-600 h-2 rounded-full transition-all duration-300"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
  accept: {
    type: String,
    default: 'image/*,.pdf,.doc,.docx'
  },
  multiple: {
    type: Boolean,
    default: false
  },
  maxSize: {
    type: Number,
    default: 10 // MB
  },
  doctype: {
    type: String,
    required: true
  },
  docname: {
    type: String,
    default: ''
  },
  isPrivate: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['upload-success', 'upload-error', 'files-changed'])

// Reactive data
const fileInput = ref(null)
const files = ref([])
const dragOver = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)

// Computed properties
const acceptTypes = computed(() => {
  return props.accept.replace(/\*/g, '').replace(/,/g, ', ')
})

// Methods
const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

const handleDrop = (event) => {
  dragOver.value = false
  const droppedFiles = Array.from(event.dataTransfer.files)
  addFiles(droppedFiles)
}

const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    // Check file size
    if (file.size > props.maxSize * 1024 * 1024) {
      console.error(`File ${file.name} exceeds maximum size of ${props.maxSize}MB`)
      return false
    }
    
    // Check file type
    const acceptedTypes = props.accept.split(',').map(type => type.trim())
    const isAccepted = acceptedTypes.some(type => {
      if (type.includes('*')) {
        return file.type.startsWith(type.replace('*', ''))
      }
      return file.type === type
    })
    
    if (!isAccepted) {
      console.error(`File ${file.name} type not accepted`)
      return false
    }
    
    return true
  })
  
  if (props.multiple) {
    files.value.push(...validFiles.map(file => ({
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      uploaded: false,
      uploading: false,
      error: false,
      url: ''
    })))
  } else {
    // Replace existing files if not multiple
    files.value = validFiles.map(file => ({
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      uploaded: false,
      uploading: false,
      error: false,
      url: ''
    }))
  }
  
  emit('files-changed', files.value)
}

const removeFile = (index) => {
  files.value.splice(index, 1)
  emit('files-changed', files.value)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const uploadFiles = async () => {
  if (files.value.length === 0) return []
  
  uploading.value = true
  uploadProgress.value = 0
  
  const uploadedFiles = []
  
  try {
    for (let i = 0; i < files.value.length; i++) {
      const fileData = files.value[i]
      
      if (fileData.uploaded) {
        uploadedFiles.push(fileData)
        continue
      }
      
      fileData.uploading = true
      uploadProgress.value = (i / files.value.length) * 100
      
      const formData = new FormData()
      formData.append('file', fileData.file)
      formData.append('doctype', props.doctype)
      if (props.docname) {
        formData.append('docname', props.docname)
      }
      formData.append('is_private', props.isPrivate ? '1' : '0')
      
      try {
        const response = await call('/api/method/upload_file', formData)
        
        if (response.message === 'OK' && response.file_url) {
          fileData.uploaded = true
          fileData.url = response.file_url
          fileData.uploading = false
          uploadedFiles.push(fileData)
          emit('upload-success', fileData)
        } else {
          throw new Error('Upload failed')
        }
      } catch (error) {
        fileData.error = true
        fileData.uploading = false
        emit('upload-error', { file: fileData, error })
      }
      
      uploadProgress.value = ((i + 1) / files.value.length) * 100
    }
  } catch (error) {
    console.error('Upload error:', error)
  } finally {
    uploading.value = false
    uploadProgress.value = 100
  }
  
  return uploadedFiles
}

// Expose methods for parent component
defineExpose({
  uploadFiles,
  files,
  clearFiles: () => {
    files.value = []
    emit('files-changed', [])
  }
})
</script>
