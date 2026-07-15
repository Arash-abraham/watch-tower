<template>
  <nav class="fixed top-0 left-0 right-0 z-50 transition-all duration-300" :class="scrolled ? 'bg-black/80 backdrop-blur-xl border-b border-cyan-500/20' : 'bg-transparent'">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Logo Section -->
        <div class="flex items-center gap-2 group cursor-pointer" @click="goHome">
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

        <!-- Desktop Navigation Links -->
        <div class="hidden md:flex items-center gap-1">
          <button 
            v-for="item in navItems"
            :key="item.route"
            @click="navigateTo(item.route)"
            class="relative px-4 py-2 text-sm font-medium transition-all duration-300 group"
            :class="isActive(item.route) ? 'text-cyan-400' : 'text-gray-400 hover:text-white'"
          >
            {{ item.label }}
            <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-px bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300 group-hover:w-full"
              :class="isActive(item.route) ? 'w-full' : ''">
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
          @click="toggleMobileMenu"
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
      <div v-if="mobileMenuOpen" class="md:hidden py-4 border-t border-cyan-500/20 mt-2">
        <div class="flex flex-col gap-2">
          <button 
            v-for="item in navItems"
            :key="item.route"
            @click="navigateTo(item.route)"
            class="px-4 py-2 text-gray-300 hover:text-cyan-400 transition-colors rounded-lg hover:bg-cyan-500/10 text-left"
          >
            {{ item.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Bottom Glow Effect -->
    <div class="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent"></div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const scrolled = ref(false)
const mobileMenuOpen = ref(false)

// آیتم‌های منو
const navItems = [
  { label: 'Dashboard', route: '/dashboard' },
  { label: 'Apps', route: '/apps' },
  { label: 'Targets', route: '/targets' },
  { label: 'Monitors', route: '/monitors' },
  { label: 'Alerts', route: '/alerts' }
]

// بررسی فعال بودن مسیر - استفاده از computed به جای تابع
const isActive = (path) => {
  if (!route || !route.path) return false
  return route.path === path
}

// نویگیشن به مسیر
const navigateTo = (path) => {
  if (router) {
    router.push(path)
    mobileMenuOpen.value = false
  }
}

// رفتن به صفحه اصلی
const goHome = () => {
  if (router) {
    router.push('/')
    mobileMenuOpen.value = false
  }
}

// مدیریت اسکرول
const handleScroll = () => {
  scrolled.value = window.scrollY > 20
}

// توگل منو موبایل
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

// بستن منو موبایل
const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>