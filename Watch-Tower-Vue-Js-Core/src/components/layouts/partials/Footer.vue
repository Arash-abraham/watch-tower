<template>
  <footer class="relative mt-24 overflow-hidden border-t border-white/10 bg-[#04070a]/70">
    <!-- decorative top glow -->
    <div class="pointer-events-none absolute inset-x-0 top-0 h-px glass-line"></div>
    <div class="pointer-events-none absolute -top-24 left-1/2 h-48 w-[42rem] -translate-x-1/2 rounded-full bg-cyan-500/10 blur-[100px]"></div>
    <div class="pointer-events-none absolute inset-0 bg-grid opacity-30"></div>

    <div class="container-page relative">
      <!-- ══════════ main grid ══════════ -->
      <div class="grid gap-12 py-14 lg:grid-cols-12 lg:gap-8">
        <!-- brand -->
        <div class="lg:col-span-4">
          <RouterLink to="/" class="group inline-flex items-center gap-2.5">
            <span class="relative grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 shadow-glow-sm">
              <svg class="h-5 w-5 text-slate-950" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </span>
            <span class="text-[15px] font-extrabold tracking-tight text-white">
              WATCH<span class="text-cyan-300">TOWER</span>
            </span>
          </RouterLink>

          <p class="mt-5 max-w-sm text-sm leading-relaxed text-gray-400">
            Continuous asset monitoring for bug bounty programs. Watch Tower tracks scope changes across the
            major platforms and tells you the moment something moves.
          </p>

          <div class="mt-6 flex flex-wrap gap-2">
            <span v-for="tech in stack" :key="tech" class="rounded-md border border-white/10 bg-white/[0.03] px-2 py-1 font-mono text-[10px] uppercase tracking-wider text-gray-500">
              {{ tech }}
            </span>
          </div>

          <div class="mt-6 flex items-center gap-2">
            <a
              v-for="social in socials"
              :key="social.label"
              :href="social.href"
              target="_blank"
              rel="noopener"
              class="grid h-9 w-9 place-items-center rounded-lg border border-white/10 text-gray-400 transition-all duration-300 hover:-translate-y-0.5 hover:border-cyan-400/40 hover:text-cyan-300"
              :aria-label="social.label"
            >
              <svg v-if="social.icon === 'github'" class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                />
              </svg>
              <svg v-else-if="social.icon === 'docs'" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.5a5.5 5.5 0 00-5.5-2A20 20 0 003 5v13a20 20 0 013.5-.5 5.5 5.5 0 015.5 2m0-13a5.5 5.5 0 015.5-2A20 20 0 0121 5v13a20 20 0 00-3.5-.5 5.5 5.5 0 00-5.5 2m0-13v13" />
              </svg>
              <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2m0 14v2M4.2 4.2l1.4 1.4m12.8 12.8l1.4 1.4M3 12h2m14 0h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
                <circle cx="12" cy="12" r="3.5" />
              </svg>
            </a>
          </div>
        </div>

        <!-- link columns -->
        <div class="grid grid-cols-2 gap-8 sm:grid-cols-3 lg:col-span-5">
          <div v-for="column in columns" :key="column.title">
            <h3 class="mb-4 font-mono text-[10px] uppercase tracking-[0.2em] text-cyan-300/70">{{ column.title }}</h3>
            <ul class="space-y-2.5">
              <li v-for="link in column.links" :key="link.label">
                <RouterLink
                  v-if="link.to"
                  :to="link.to"
                  class="group inline-flex items-center gap-1.5 text-[13px] text-gray-400 transition-colors hover:text-cyan-300"
                >
                  <span class="h-px w-0 bg-cyan-400 transition-all duration-300 group-hover:w-3"></span>
                  {{ link.label }}
                </RouterLink>
                <button
                  v-else-if="link.action === 'docs'"
                  class="group inline-flex items-center gap-1.5 text-[13px] text-gray-400 transition-colors hover:text-cyan-300"
                  @click="openDocs"
                >
                  <span class="h-px w-0 bg-cyan-400 transition-all duration-300 group-hover:w-3"></span>
                  {{ link.label }}
                </button>
                <a
                  v-else
                  :href="link.href"
                  target="_blank"
                  rel="noopener"
                  class="group inline-flex items-center gap-1.5 text-[13px] text-gray-400 transition-colors hover:text-cyan-300"
                >
                  <span class="h-px w-0 bg-cyan-400 transition-all duration-300 group-hover:w-3"></span>
                  {{ link.label }}
                  <svg class="h-3 w-3 opacity-0 transition-opacity group-hover:opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7 17L17 7M17 7H9m8 0v8" />
                  </svg>
                </a>
              </li>
            </ul>
          </div>
        </div>

        <!-- status card -->
        <div class="lg:col-span-3">
          <div class="panel p-5">
            <div class="mb-3 flex items-center justify-between">
              <h3 class="font-mono text-[10px] uppercase tracking-[0.2em] text-gray-500">Platform status</h3>
              <span class="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]"></span>
            </div>

            <div class="space-y-3">
              <div v-for="row in status" :key="row.label" class="flex items-center justify-between gap-3">
                <span class="text-[12px] text-gray-500">{{ row.label }}</span>
                <span class="font-mono text-[11px]" :class="row.ok ? 'text-emerald-300/90' : 'text-gray-500'">
                  {{ row.value }}
                </span>
              </div>
            </div>

            <div class="divider my-4"></div>

            <RouterLink to="/monitors" class="group flex items-center justify-between text-[12px] font-medium text-cyan-300/90 hover:text-cyan-200">
              View monitors
              <svg class="h-3.5 w-3.5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6" />
              </svg>
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- ══════════ bottom bar ══════════ -->
      <div class="flex flex-col items-center justify-between gap-4 border-t border-white/10 py-6 sm:flex-row">
        <p class="text-center text-[12px] text-gray-500 sm:text-left">
          © {{ year }} <span class="text-gray-400">Watch Tower</span> · Released under the
          <a
            href="https://github.com/Arash-abraham/watch-tower/blob/main/LICENSE"
            target="_blank"
            rel="noopener"
            class="text-cyan-300/80 underline decoration-cyan-400/30 underline-offset-2 hover:text-cyan-200"
          >
            MIT License
          </a>
        </p>

        <div class="flex items-center gap-5">
          <span class="hidden font-mono text-[10px] uppercase tracking-[0.18em] text-gray-600 sm:inline"> Self-hosted · v2.0.1 </span>
          <button
            class="group inline-flex items-center gap-2 rounded-lg border border-white/10 px-3 py-1.5 text-[11px] font-mono uppercase tracking-wider text-gray-400 transition-colors hover:border-cyan-400/40 hover:text-cyan-300"
            @click="scrollToTop"
          >
            Back to top
            <svg class="h-3 w-3 transition-transform duration-300 group-hover:-translate-y-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 19V5M6 11l6-6 6 6" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()

const stack = ['Vue 3', 'Laravel', 'Python 3', 'MongoDB', 'Tailwind']

const socials = [
  { label: 'GitHub', href: 'https://github.com/Arash-abraham/watch-tower', icon: 'github' },
  { label: 'Documentation', action: 'docs', icon: 'docs' },
  { label: 'Repository insights', href: 'https://github.com/Arash-abraham/watch-tower', icon: 'pulse' },
]

const columns = [
  {
    title: 'Platform',
    links: [
      { label: 'Dashboard', to: '/dashboard' },
      { label: 'Applications', to: '/apps' },
      { label: 'Targets', to: '/targets' },
      { label: 'Monitors', to: '/monitors' },
    ],
  },
  {
    title: 'Insights',
    links: [
      { label: 'Alerts feed', to: '/alerts' },
      { label: 'Settings', to: '/setting' },
      { label: 'Overview', to: '/' },
    ],
  },
  {
    title: 'Resources',
    links: [
      { label: 'Documentation', action: 'docs' },
      { label: 'Source code', href: 'https://github.com/Arash-abraham/watch-tower' },
      { label: 'Report an issue', href: 'https://github.com/Arash-abraham/watch-tower/issues' },
      { label: 'License', href: 'https://github.com/Arash-abraham/watch-tower/blob/main/LICENSE' },
    ],
  },
]

const status = [
  { label: 'Collector', value: 'scheduled', ok: true },
  { label: 'API', value: 'v2.1', ok: true },
  { label: 'Storage', value: 'MongoDB', ok: true },
  { label: 'Notifiers', value: 'Telegram · Discord', ok: true },
]

function openDocs() {
  window.dispatchEvent(new CustomEvent('show-modal'))
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>
