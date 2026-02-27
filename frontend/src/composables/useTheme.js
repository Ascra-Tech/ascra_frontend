import { ref, onMounted, watch } from 'vue'

export function useTheme() {
  const isDark = ref(false)
  const systemPreference = ref(false)

  // Check system preference
  const checkSystemPreference = () => {
    if (typeof window !== 'undefined') {
      systemPreference.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      return systemPreference.value
    }
    return false
  }

  // Get saved theme from localStorage
  const getSavedTheme = () => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('theme')
      if (saved) {
        return saved === 'dark'
      }
    }
    return null
  }

  // Apply theme to document
  const applyTheme = (dark) => {
    if (typeof document !== 'undefined') {
      const html = document.documentElement
      if (dark) {
        html.classList.add('dark')
      } else {
        html.classList.remove('dark')
      }
    }
  }

  // Set theme
  const setTheme = (dark) => {
    isDark.value = dark
    applyTheme(dark)
    
    // Save to localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', dark ? 'dark' : 'light')
    }
  }

  // Toggle theme
  const toggleTheme = () => {
    setTheme(!isDark.value)
  }

  // Set system theme
  const setSystemTheme = () => {
    const systemDark = checkSystemPreference()
    setTheme(systemDark)
    if (typeof window !== 'undefined') {
      localStorage.removeItem('theme') // Remove saved preference to use system
    }
  }

  // Initialize theme
  const initTheme = () => {
    const saved = getSavedTheme()
    if (saved !== null) {
      setTheme(saved)
    } else {
      // Use system preference as default
      setSystemTheme()
    }
  }

  // Watch for system preference changes
  const watchSystemPreference = () => {
    if (typeof window !== 'undefined') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      mediaQuery.addEventListener('change', (e) => {
        systemPreference.value = e.matches
        // Only update if user hasn't set a manual preference
        if (getSavedTheme() === null) {
          setTheme(e.matches)
        }
      })
    }
  }

  onMounted(() => {
    watchSystemPreference()
  })

  return {
    isDark,
    systemPreference,
    toggleTheme,
    setTheme,
    setSystemTheme,
    initTheme
  }
}

// Initialize theme immediately to prevent flash
if (typeof window !== 'undefined') {
  const saved = localStorage.getItem('theme')
  let isDark = false
  
  if (saved) {
    isDark = saved === 'dark'
  } else {
    isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  
  // Apply theme immediately
  if (isDark) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}
