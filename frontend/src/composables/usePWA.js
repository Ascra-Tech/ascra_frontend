import { ref, onMounted } from 'vue'

export function usePWA() {
  const isInstallable = ref(false)
  const isInstalled = ref(false)
  const deferredPrompt = ref(null)

  const install = async () => {
    if (!deferredPrompt.value) return
    
    deferredPrompt.value.prompt()
    const { outcome } = await deferredPrompt.value.userChoice
    
    if (outcome === 'accepted') {
      console.log('PWA installation accepted')
      isInstallable.value = false
    }
    
    deferredPrompt.value = null
  }

  const checkInstalled = () => {
    if (window.matchMedia('(display-mode: standalone)').matches) {
      isInstalled.value = true
    }
  }

  onMounted(() => {
    // Listen for beforeinstallprompt
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault()
      deferredPrompt.value = e
      isInstallable.value = true
    })

    // Listen for app installed
    window.addEventListener('appinstalled', () => {
      console.log('PWA was installed')
      isInstalled.value = true
      isInstallable.value = false
    })

    checkInstalled()
  })

  return {
    isInstallable,
    isInstalled,
    install
  }
}