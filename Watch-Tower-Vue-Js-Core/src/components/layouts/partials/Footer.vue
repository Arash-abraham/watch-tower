<template>
  <footer class="relative mt-20 border-t border-white/[0.07] bg-[#04070a]/70">
    <!-- top glow -->
    <div class="pointer-events-none absolute inset-x-0 top-0 h-px glass-line"></div>
    <div class="pointer-events-none absolute -top-16 left-1/2 h-32 w-[32rem] -translate-x-1/2 rounded-full bg-cyan-500/[0.07] blur-[80px]"></div>

    <div class="container-page relative">
      <!-- ══════════ single elegant row ══════════ -->
      <div class="flex flex-col items-center gap-6 py-7 lg:flex-row lg:justify-between">
        <!-- brand -->
        <RouterLink to="/" class="group flex items-center gap-2.5">
          <span class="relative grid h-8 w-8 place-items-center rounded-lg bg-gradient-to-br from-cyan-400 to-blue-600 shadow-glow-sm transition-transform duration-300 group-hover:-translate-y-0.5">
            <svg class="h-4 w-4 text-slate-950" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </span>
          <span class="text-[14px] font-extrabold tracking-tight text-white">
            WATCH<span class="text-cyan-300">TOWER</span>
          </span>
          <span class="hidden h-3.5 w-px bg-white/10 sm:block"></span>
          <span class="hidden text-[11px] text-gray-500 sm:block">Continuous asset monitoring</span>
        </RouterLink>

        <!-- links -->
        <nav class="flex flex-wrap items-center justify-center gap-x-6 gap-y-2" aria-label="Footer navigation">
          <RouterLink
            v-for="link in links"
            :key="link.to"
            :to="link.to"
            class="text-[12px] text-gray-500 transition-colors hover:text-cyan-300"
          >
            {{ link.label }}
          </RouterLink>
          <a
            href="https://github.com/Arash-abraham/watch-tower"
            target="_blank"
            rel="noopener"
            class="text-[12px] text-gray-500 transition-colors hover:text-cyan-300"
          >
            GitHub
          </a>
        </nav>

        <!-- actions -->
        <div class="flex items-center gap-2">
          <span class="flex items-center gap-1.5 rounded-full border border-emerald-400/20 bg-emerald-400/[0.06] px-2.5 py-1">
            <span class="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]"></span>
            <span class="font-mono text-[9px] uppercase tracking-[0.14em] text-emerald-300/80">All systems normal</span>
          </span>

          <button
            class="group grid h-8 w-8 place-items-center rounded-lg border border-white/10 text-gray-500 transition-all duration-300 hover:-translate-y-0.5 hover:border-cyan-400/40 hover:text-cyan-300"
            aria-label="Back to top"
            @click="scrollToTop"
          >
            <svg class="h-3.5 w-3.5 transition-transform group-hover:-translate-y-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 19V5M6 11l6-6 6 6" />
            </svg>
          </button>
        </div>
      </div>

      <!-- ══════════ thin bottom bar ══════════ -->
      <div class="flex flex-col items-center justify-between gap-2 border-t border-white/[0.06] py-4 sm:flex-row">
        <p class="text-[11px] text-gray-600">
          © {{ year }} <span class="text-gray-400">Watch Tower</span> · MIT License
        </p>
        <p class="font-mono text-[10px] uppercase tracking-[0.16em] text-gray-700">
          Vue · Laravel · Python · MongoDB
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()

const links = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Targets', to: '/targets' },
  { label: 'Alerts', to: '/alerts' },
  { label: 'Monitors', to: '/monitors' },
]

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>
