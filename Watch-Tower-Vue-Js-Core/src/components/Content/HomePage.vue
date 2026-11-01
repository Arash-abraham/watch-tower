<template>
  <section class="relative overflow-hidden">
    <!-- local ambience -->
    <div class="pointer-events-none absolute left-1/2 top-0 -z-0 h-[32rem] w-[52rem] -translate-x-1/2 rounded-full bg-cyan-500/[0.07] blur-[130px]"></div>

    <div class="container-page relative py-16 lg:py-24">
      <div class="grid items-center gap-14 lg:grid-cols-[1.05fr_0.95fr] lg:gap-10">
        <!-- ══════════════ copy ══════════════ -->
        <div class="animate-fade-up">
          <div class="flex flex-wrap items-center gap-3">
            <span class="chip">
              <span class="relative flex h-1.5 w-1.5">
                <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-cyan-400 opacity-70"></span>
                <span class="relative inline-flex h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
              </span>
              System active
            </span>
            <span class="font-mono text-[10px] uppercase tracking-[0.18em] text-gray-600">v2.0.1 · self-hosted</span>
          </div>

          <h1 class="mt-7 text-[2.6rem] font-extrabold leading-[1.05] tracking-tight sm:text-6xl lg:text-[4.2rem]">
            <span class="block text-white/90">Welcome to</span>
            <span class="relative mt-1 inline-block">
              <span
                class="absolute -inset-x-2 bottom-1 top-2 -z-10 bg-gradient-to-r from-cyan-400/20 via-blue-500/20 to-transparent blur-2xl"
                aria-hidden="true"
              ></span>
              <span class="text-gradient animate-gradient bg-[length:200%_auto] text-shadow-glow">Watch Tower</span>
            </span>
          </h1>

          <p class="mt-6 max-w-xl text-[15px] leading-relaxed text-gray-400">
            Continuous asset monitoring for bug bounty programs. Watch Tower keeps an eye on
            <span class="text-gray-200">every scope change</span> across the major platforms and tells you the
            moment something moves — before anyone else notices.
          </p>

          <div class="mt-9 flex flex-col gap-3 sm:flex-row">
            <RouterLink to="/dashboard" class="btn-primary group px-7 py-3 text-[13px] uppercase tracking-wider">
              Open dashboard
              <svg
                class="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                stroke-width="2.2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6" />
              </svg>
            </RouterLink>

            <a
              href="https://github.com/Arash-abraham/watch-tower"
              target="_blank"
              rel="noopener"
              class="btn-ghost group px-7 py-3 text-[13px] uppercase tracking-wider"
            >
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                />
              </svg>
              Source code
            </a>
          </div>

          <div class="mt-10 flex flex-wrap items-center gap-x-6 gap-y-2">
            <div v-for="item in highlights" :key="item" class="flex items-center gap-2 text-[12px] text-gray-500">
              <svg class="h-3.5 w-3.5 text-cyan-400/60" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              {{ item }}
            </div>
          </div>
        </div>

        <!-- ══════════════ live telemetry panel ══════════════ -->
        <div class="animate-fade-up [animation-delay:120ms]">
          <div class="card-gradient-border relative rounded-3xl p-[1px]">
            <div class="relative overflow-hidden rounded-3xl bg-[#060b11]/90 p-1 shadow-[0_40px_120px_-40px_rgba(34,211,238,0.35)] backdrop-blur-xl">
              <!-- header -->
              <div class="flex items-center justify-between gap-3 rounded-t-2xl border-b border-white/[0.06] px-4 py-3">
                <div class="flex items-center gap-2.5">
                  <span class="flex gap-1.5">
                    <span class="h-2 w-2 rounded-full bg-red-400/70"></span>
                    <span class="h-2 w-2 rounded-full bg-amber-400/70"></span>
                    <span class="h-2 w-2 rounded-full bg-emerald-400/70"></span>
                  </span>
                  <span class="font-mono text-[10px] tracking-wider text-gray-500">watchtower://telemetry</span>
                </div>
                <span class="flex items-center gap-1.5 rounded-full border border-emerald-400/25 bg-emerald-400/10 px-2 py-0.5 font-mono text-[9px] uppercase tracking-[0.16em] text-emerald-300">
                  <span class="h-1 w-1 animate-pulse rounded-full bg-emerald-400"></span> live
                </span>
              </div>

              <!-- radar -->
              <div class="relative flex justify-center px-4 pb-2 pt-6">
                <div class="relative aspect-square w-full max-w-[15rem]">
                  <div class="absolute inset-0 rounded-full border border-cyan-400/15"></div>
                  <div class="absolute inset-[14%] rounded-full border border-cyan-400/12"></div>
                  <div class="absolute inset-[28%] rounded-full border border-cyan-400/10"></div>
                  <div class="absolute inset-[42%] rounded-full border border-cyan-400/10"></div>
                  <div class="absolute inset-0 rounded-full bg-cyan-400/[0.03]"></div>

                  <!-- crosshairs -->
                  <div class="absolute inset-x-0 top-1/2 h-px bg-gradient-to-r from-transparent via-cyan-400/15 to-transparent"></div>
                  <div class="absolute inset-y-0 left-1/2 w-px bg-gradient-to-b from-transparent via-cyan-400/15 to-transparent"></div>

                  <!-- sweep -->
                  <div
                    class="absolute inset-0 animate-radar rounded-full [background:conic-gradient(from_0deg,rgba(34,211,238,0.35),rgba(34,211,238,0.06)_55deg,transparent_110deg)]"
                  ></div>

                  <!-- blips -->
                  <span class="absolute left-[30%] top-[34%] h-1.5 w-1.5 animate-blip rounded-full bg-cyan-300 shadow-[0_0_10px_2px_rgba(34,211,238,0.7)]"></span>
                  <span class="absolute left-[68%] top-[46%] h-1.5 w-1.5 animate-blip rounded-full bg-emerald-300 shadow-[0_0_10px_2px_rgba(52,211,153,0.6)] [animation-delay:1.1s]"></span>
                  <span class="absolute left-[46%] top-[70%] h-1 w-1 animate-blip rounded-full bg-blue-300 shadow-[0_0_10px_2px_rgba(96,165,250,0.6)] [animation-delay:2.2s]"></span>

                  <!-- center -->
                  <div class="absolute left-1/2 top-1/2 grid h-8 w-8 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full border border-cyan-400/40 bg-[#04121a]">
                    <span class="h-1.5 w-1.5 rounded-full bg-cyan-300 shadow-[0_0_10px_2px_rgba(34,211,238,0.8)]"></span>
                  </div>
                </div>
              </div>

              <!-- stats -->
              <div class="grid grid-cols-3 divide-x divide-white/[0.06] border-y border-white/[0.06]">
                <div v-for="stat in stats" :key="stat.label" class="px-3 py-4 text-center">
                  <div class="font-mono text-[9px] uppercase tracking-[0.14em] text-gray-600">{{ stat.label }}</div>
                  <div class="mt-1 text-xl font-bold text-white tabular-nums">{{ stat.value }}</div>
                </div>
              </div>

              <!-- ticker -->
              <div class="px-4 py-3">
                <div class="mb-2 flex items-center justify-between">
                  <span class="font-mono text-[9px] uppercase tracking-[0.16em] text-cyan-400/60">live feed</span>
                  <span class="flex items-center gap-1 font-mono text-[9px] text-gray-600">
                    <span class="h-1 w-1 animate-pulse rounded-full bg-cyan-400"></span> updating
                  </span>
                </div>

                <ul class="space-y-1.5">
                  <li
                    v-for="(change, index) in ticker"
                    :key="index"
                    class="flex items-center gap-2 rounded-md px-2 py-1 font-mono text-[10px] text-gray-500"
                    :class="index === 0 ? 'bg-white/[0.03] text-gray-400' : ''"
                  >
                    <span class="h-1 w-1 shrink-0 rounded-full" :class="index === 0 ? 'bg-cyan-400' : 'bg-gray-600'"></span>
                    <span class="truncate">{{ change }}</span>
                  </li>
                  <li v-if="!ticker.length" class="flex items-center gap-2 px-2 py-1 font-mono text-[10px] text-gray-600">
                    <span class="h-1 w-1 rounded-full bg-gray-600"></span>
                    waiting for the collector…
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ══════════════ feature cards ══════════════ -->
      <div class="mt-20 grid gap-5 md:grid-cols-3">
        <article
          v-for="(feature, index) in features"
          :key="feature.title"
          class="panel panel-hover group animate-fade-up p-6"
          :style="{ animationDelay: `${180 + index * 90}ms` }"
        >
          <div class="tile transition-colors duration-300 group-hover:border-cyan-400/30 group-hover:text-cyan-200">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.6">
              <path stroke-linecap="round" stroke-linejoin="round" :d="feature.icon" />
            </svg>
          </div>

          <h3 class="mt-5 text-base font-semibold text-white">{{ feature.title }}</h3>
          <p class="mt-2 text-[13px] leading-relaxed text-gray-500">{{ feature.description }}</p>

          <div class="mt-5 flex flex-wrap gap-1.5">
            <span
              v-for="tag in feature.tags"
              :key="tag"
              class="rounded-md border border-white/10 bg-white/[0.03] px-2 py-0.5 font-mono text-[10px] text-gray-500"
            >
              {{ tag }}
            </span>
          </div>
        </article>
      </div>

      <!-- ══════════════ tech strip ══════════════ -->
      <div class="mt-14 flex flex-col items-center gap-4 border-t border-white/[0.06] pt-8 sm:flex-row sm:justify-between">
        <p class="font-mono text-[10px] uppercase tracking-[0.2em] text-gray-600">Built with</p>
        <div class="flex flex-wrap justify-center gap-2">
          <span
            v-for="tech in stack"
            :key="tech"
            class="rounded-lg border border-white/10 bg-white/[0.03] px-2.5 py-1 font-mono text-[10px] uppercase tracking-wider text-gray-500 transition-colors hover:border-cyan-400/30 hover:text-cyan-300/80"
          >
            {{ tech }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from '../../services/api'

const live = ref({ programs: '—', changes: '—', sources: '—' })
const feed = ref([])

const stats = computed(() => [
  { label: 'Programs', value: live.value.programs },
  { label: 'Changes 24h', value: live.value.changes },
  { label: 'Sources', value: live.value.sources },
])

const ticker = computed(() => feed.value.slice(0, 2))

const highlights = ['Multi-channel alerts', 'MongoDB + Laravel API', 'Self-hosted']

const features = [
  {
    title: 'Scope change detection',
    description:
      'Every program snapshot is diffed against the previous run. Assets added or removed from scope are recorded with a timestamp and notified instantly.',
    tags: ['diff engine', 'history'],
    icon: 'M4 7V5a1 1 0 011-1h3M20 7V5a1 1 0 00-1-1h-3M4 17v2a1 1 0 001 1h3m9 0h3a1 1 0 001-1v-2M8 12h8',
  },
  {
    title: 'Four platforms, one schema',
    description:
      'HackerOne, Bugcrowd, YesWeHack and Intigriti datasets are normalised into a single model so you can search the whole landscape at once.',
    tags: ['hackerone', 'bugcrowd', 'yeswehack', 'intigriti'],
    icon: 'M12 3v18M3 12h18M5.6 5.6l12.8 12.8M18.4 5.6L5.6 18.4',
  },
  {
    title: 'Signal, not noise',
    description:
      'Conflicts, out-of-scope moves and closed programs are flagged separately, so the alert feed stays short enough to actually read.',
    tags: ['conflicts', 'telegram', 'discord'],
    icon: 'M12 9v4m0 4h.01M10.3 3.9L2.6 17a2 2 0 001.7 3h15.4a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z',
  },
]

const stack = ['Vue 3', 'Laravel', 'Python 3', 'MongoDB', 'Tailwind', 'Docker']

onMounted(async () => {
  const [statsResponse, changesResponse] = await Promise.all([
    api.stats().catch(() => null),
    api.changes({ per_page: 6 }).catch(() => null),
  ])

  const data = statsResponse?.data
  if (data) {
    live.value = {
      programs: data.active_programs ?? 0,
      changes: data.changes_24h ?? 0,
      sources: (data.sources || []).filter((source) => source.active_programs > 0).length,
    }
  }

  const items = changesResponse?.data
  if (Array.isArray(items)) {
    feed.value = items.slice(0, 3).map((change) => `${change.type.replace(/_/g, ' ')} · ${change.target || change.program?.name || 'unknown'}`)
  }
})
</script>
