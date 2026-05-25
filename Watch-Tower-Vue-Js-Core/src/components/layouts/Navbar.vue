<!-- components/Navbar.vue -->
<template>
  <nav class="fixed top-0 left-0 right-0 z-50 transition-all duration-300" :class="scrolled ? 'bg-black/80 backdrop-blur-xl border-b border-cyan-500/20' : 'bg-transparent'">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Logo Section -->
        <div class="flex items-center gap-2 group cursor-pointer" @click="scrollToTop">
          <div class="relative">
            <div class="absolute inset-0 bg-cyan-500/20 blur-lg rounded-full group-hover:bg-cyan-500/30 transition-all duration-300"></div>
            <div class="relative w-8 h-8 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
              </svg>
            </div>
          </div>
          <span class="text-white font-bold tracking-tight">
            WATCH<span class="text-cyan-400">TOWER</span>
          </span>
        </div>

        <!-- Desktop Navigation Links - اینجا منوها مستقیم نوشته شدن -->
        <!-- جایگزین بخش Desktop Navigation Links -->
        <div class="hidden md:flex items-center gap-1">
        <button 
            @click="$emit('navigate', 'dashboard')"
            class="relative px-4 py-2 text-sm font-medium transition-all duration-300 group"
            :class="activeSection === 'dashboard' ? 'text-cyan-400' : 'text-gray-400 hover:text-white'"
        >
            Dashboard
            <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-px bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300 group-hover:w-full"
            :class="activeSection === 'dashboard' ? 'w-full' : ''">
            </span>
        </button>

        <button 
            @click="$emit('navigate', 'apps')"
            class="relative px-4 py-2 text-sm font-medium transition-all duration-300 group"
            :class="activeSection === 'apps' ? 'text-cyan-400' : 'text-gray-400 hover:text-white'"
        >
            Apps
            <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-px bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300 group-hover:w-full"
            :class="activeSection === 'apps' ? 'w-full' : ''">
            </span>
        </button>

        <button 
            @click="$emit('navigate', 'targets')"
            class="relative px-4 py-2 text-sm font-medium transition-all duration-300 group"
            :class="activeSection === 'targets' ? 'text-cyan-400' : 'text-gray-400 hover:text-white'"
        >
            Targets
            <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-px bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300 group-hover:w-full"
            :class="activeSection === 'targets' ? 'w-full' : ''">
            </span>
        </button>

        <button 
            @click="$emit('navigate', 'monitors')"
            class="relative px-4 py-2 text-sm font-medium transition-all duration-300 group"
            :class="activeSection === 'monitors' ? 'text-cyan-400' : 'text-gray-400 hover:text-white'"
        >
            Monitors
            <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-px bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300 group-hover:w-full"
            :class="activeSection === 'monitors' ? 'w-full' : ''">
            </span>
        </button>

        <button 
            @click="$emit('navigate', 'alerts')"
            class="relative px-4 py-2 text-sm font-medium transition-all duration-300 group"
            :class="activeSection === 'alerts' ? 'text-cyan-400' : 'text-gray-400 hover:text-white'"
        >
            Alerts
            <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-px bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300 group-hover:w-full"
            :class="activeSection === 'alerts' ? 'w-full' : ''">
            </span>
        </button>
        </div>

        <!-- Status Indicator -->
        <div class="hidden md:flex items-center gap-2 px-3 py-1.5 border border-cyan-500/20 rounded-full bg-cyan-500/5">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          <span class="text-xs text-green-400/80 font-mono">System Online</span>
        </div>

        <!-- Mobile Menu Button -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden relative w-10 h-10 flex items-center justify-center rounded-lg border border-cyan-500/20 hover:border-cyan-500/40 transition-colors"
        >
          <div class="absolute inset-0 bg-cyan-500/5 rounded-lg"></div>
          <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Mobile Menu Dropdown -->
      <transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 -translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-4"
      >
        <div v-if="mobileMenuOpen" class="md:hidden py-4 border-t border-cyan-500/20 mt-2">
          <div class="flex flex-col gap-2">
            <a href="#dashboard" @click="closeMobileMenu" class="px-4 py-2 text-gray-300 hover:text-cyan-400 transition-colors rounded-lg hover:bg-cyan-500/10">Dashboard</a>
            <a href="#apps" @click="closeMobileMenu" class="px-4 py-2 text-gray-300 hover:text-cyan-400 transition-colors rounded-lg hover:bg-cyan-500/10">Apps</a>
            <a href="#targets" @click="closeMobileMenu" class="px-4 py-2 text-gray-300 hover:text-cyan-400 transition-colors rounded-lg hover:bg-cyan-500/10">Targets</a>
            <a href="#monitors" @click="closeMobileMenu" class="px-4 py-2 text-gray-300 hover:text-cyan-400 transition-colors rounded-lg hover:bg-cyan-500/10">Monitors</a>
            <a href="#alerts" @click="closeMobileMenu" class="px-4 py-2 text-gray-300 hover:text-cyan-400 transition-colors rounded-lg hover:bg-cyan-500/10">Alerts</a>
          </div>
        </div>
      </transition>
    </div>

    <!-- Bottom Glow Effect -->
    <div class="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent"></div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const scrolled = ref(false)
const mobileMenuOpen = ref(false)
const activeSection = ref('dashboard')

const handleScroll = () => {
  scrolled.value = window.scrollY > 20
  
  const sections = ['dashboard', 'apps', 'targets', 'monitors', 'alerts']
  for (const section of sections) {
    const element = document.getElementById(section)
    if (element) {
      const rect = element.getBoundingClientRect()
      if (rect.top <= 100 && rect.bottom >= 100) {
        activeSection.value = section
        break
      }
    }
  }
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>