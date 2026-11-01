<template>
  <header
    class="fixed inset-x-0 top-0 z-50 transition-all duration-300"
    :class="scrolled || mobileOpen ? 'border-b border-white/10 bg-[#04070a]/85 backdrop-blur-xl' : 'border-b border-transparent bg-transparent'"
  >
    <!-- top glow line -->
    <div class="pointer-events-none absolute inset-x-0 top-0 h-px glass-line"></div>

    <nav class="container-page" aria-label="Main navigation">
      <div class="flex h-16 items-center justify-between gap-4">
        <!-- Brand -->
        <RouterLink to="/" class="group flex shrink-0 items-center gap-2.5" @click="closeMobile">
          <span class="relative grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 shadow-glow-sm">
            <span class="absolute inset-0 rounded-xl bg-cyan-400/30 blur-md transition-opacity duration-300 group-hover:opacity-100 opacity-60"></span>
            <svg class="relative h-5 w-5 text-slate-950" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </span>
          <span class="text-[15px] font-extrabold tracking-tight text-white">
            WATCH<span class="text-cyan-300">TOWER</span>
          </span>
        </RouterLink>

        <!-- Desktop links -->
        <ul class="hidden items-center gap-1 md:flex">
          <li v-for="item in navItems" :key="item.route">
            <RouterLink
              :to="item.route"
              class="group relative flex items-center rounded-lg px-3 py-2 text-[13px] font-medium transition-colors duration-200"
              :class="isActive(item.route) ? 'text-cyan-300' : 'text-gray-400 hover:text-white'"
            >
              <span
                v-if="isActive(item.route)"
                class="absolute inset-0 rounded-lg border border-cyan-400/20 bg-cyan-400/[0.07]"
                aria-hidden="true"
              ></span>
              <span class="relative">{{ item.label }}</span>
              <span
                class="absolute inset-x-3 -bottom-px h-px origin-center scale-x-0 bg-gradient-to-r from-transparent via-cyan-400 to-transparent transition-transform duration-300 group-hover:scale-x-100"
                aria-hidden="true"
              ></span>
            </RouterLink>
          </li>
        </ul>

        <!-- Right cluster -->
        <div class="flex items-center gap-2.5">
          <div class="hidden items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/[0.06] px-3 py-1.5 lg:flex">
            <span class="relative flex h-1.5 w-1.5">
              <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-70"></span>
              <span class="relative inline-flex h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
            </span>
            <span class="font-mono text-[10px] uppercase tracking-[0.14em] text-emerald-300/80">System online</span>
          </div>

          <a
            href="https://github.com/Arash-abraham/watch-tower"
            target="_blank"
            rel="noopener"
            class="hidden h-9 w-9 place-items-center rounded-lg border border-white/10 text-gray-400 transition-colors hover:border-cyan-400/40 hover:text-cyan-300 sm:grid"
            aria-label="GitHub repository"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
              />
            </svg>
          </a>

          <!-- Mobile toggle -->
          <button
            class="grid h-9 w-9 place-items-center rounded-lg border border-white/10 text-cyan-300 transition-colors hover:border-cyan-400/40 md:hidden"
            :aria-expanded="mobileOpen"
            aria-controls="mobile-menu"
            aria-label="Toggle navigation menu"
            @click="mobileOpen = !mobileOpen"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" d="M4 7h16M4 12h16M4 17h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </nav>

    <!-- Mobile drawer -->
    <transition name="drawer">
      <div v-if="mobileOpen" id="mobile-menu" class="border-t border-white/10 bg-[#04070a]/95 backdrop-blur-xl md:hidden">
        <ul class="container-page flex flex-col gap-1 py-4">
          <li v-for="item in navItems" :key="item.route">
            <RouterLink
              :to="item.route"
              class="flex items-center justify-between rounded-xl px-4 py-3 text-sm transition-colors"
              :class="isActive(item.route) ? 'bg-cyan-400/10 text-cyan-300' : 'text-gray-300 hover:bg-white/5 hover:text-white'"
              @click="closeMobile"
            >
              {{ item.label }}
              <svg class="h-4 w-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            </RouterLink>
          </li>
          <li class="mt-2 flex items-center gap-2 px-4">
            <span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
            <span class="font-mono text-[10px] uppercase tracking-[0.14em] text-emerald-300/80">System online</span>
          </li>
        </ul>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const scrolled = ref(false)
const mobileOpen = ref(false)

const navItems = [
  { label: 'Dashboard', route: '/dashboard' },
  { label: 'Apps', route: '/apps' },
  { label: 'Targets', route: '/targets' },
  { label: 'Monitors', route: '/monitors' },
  { label: 'Alerts', route: '/alerts' },
  { label: 'Setting', route: '/setting' },
]

const isActive = (path) => route.path === path

function closeMobile() {
  mobileOpen.value = false
}

function handleScroll() {
  scrolled.value = window.scrollY > 12
}

watch(() => route.fullPath, closeMobile)

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<style scoped>
.drawer-enter-active,
.drawer-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
