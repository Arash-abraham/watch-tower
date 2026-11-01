<template>
  <div class="pt-24 pb-16 text-white">
    <div class="container-page">
      <PageHeader
        badge="DASHBOARD OVERVIEW"
        title="Dashboard"
        subtitle="Live state of the monitored bounty landscape"
      >
        <template #actions>
          <div class="flex items-center gap-3 font-mono text-[11px] text-gray-600">
            <span class="flex items-center gap-2">
              <span class="relative flex h-1.5 w-1.5">
                <span
                  class="absolute inline-flex h-full w-full rounded-full opacity-70"
                  :class="health.ok ? 'animate-ping bg-emerald-400' : 'bg-red-400'"
                ></span>
                <span class="relative inline-flex h-1.5 w-1.5 rounded-full" :class="health.ok ? 'bg-emerald-400' : 'bg-red-400'"></span>
              </span>
              {{ health.ok ? 'API online' : 'API offline' }}
            </span>
            <span class="text-white/10">·</span>
            <span>updated {{ lastUpdated ? timeAgo(lastUpdated) : '—' }}</span>
            <button class="btn-ghost px-2.5 py-1 text-[10px] uppercase tracking-wider" @click="load">refresh</button>
          </div>
        </template>
      </PageHeader>

      <AsyncState :loading="loading && !stats" :error="error" @retry="load">
        <!-- ══════════ KPIs ══════════ -->
        <div class="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard
            label="Active Programs"
            :value="stats.active_programs"
            accent="cyan"
            :hint="`${formatNumber(stats.programs)} total · ${formatNumber(stats.programs - stats.active_programs)} closed`"
          />
          <StatCard label="Assets In Scope" :value="stats.scopes" accent="blue" hint="unique in-scope assets" />
          <StatCard
            label="Changes · 24h"
            :value="stats.changes_24h"
            accent="green"
            :hint="`${formatNumber(stats.changes_7d)} in the last 7 days`"
          />
          <StatCard label="Scope Conflicts" :value="stats.conflicts" accent="red" hint="assets in both scope lists" />
        </div>

        <!-- ══════════ sources + last run ══════════ -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div class="panel overflow-hidden lg:col-span-2">
            <div class="panel-head">
              <h2 class="panel-title">Sources</h2>
              <span class="font-mono text-[10px] text-gray-600">every {{ formatNumber(scheduleSeconds / 60) }} min</span>
            </div>

            <div class="divide-y divide-white/[0.06]">
              <div
                v-for="source in stats.sources"
                :key="source.source"
                class="row-hover flex items-center justify-between gap-4 px-5 py-3.5"
              >
                <div class="flex min-w-0 items-center gap-3">
                  <div class="relative grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-white/10 bg-white/[0.04] font-mono text-[11px] text-cyan-300/80">
                    {{ source.source.slice(0, 2).toUpperCase() }}
                    <span class="absolute -bottom-0.5 -right-0.5 h-2 w-2 rounded-full border-2 border-[#060b11]" :class="statusDot(source.last_run)"></span>
                  </div>
                  <div class="min-w-0">
                    <div class="truncate text-sm font-medium text-white">{{ sourceLabel(source.source) }}</div>
                    <div class="truncate font-mono text-[11px] text-gray-600">
                      {{ source.last_run ? `last run ${timeAgo(source.last_run.started_at)}` : 'never synced' }}
                    </div>
                  </div>
                </div>

                <div class="flex shrink-0 items-center gap-6 text-right">
                  <div>
                    <div class="text-sm font-semibold text-white tabular-nums">{{ formatNumber(source.active_programs) }}</div>
                    <div class="font-mono text-[9px] uppercase tracking-wider text-gray-600">programs</div>
                  </div>
                  <div class="w-12">
                    <div class="text-sm font-semibold tabular-nums" :class="source.changes_24h ? 'text-cyan-300' : 'text-gray-600'">
                      {{ formatNumber(source.changes_24h) }}
                    </div>
                    <div class="font-mono text-[9px] uppercase tracking-wider text-gray-600">24h</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="panel overflow-hidden">
            <div class="panel-head">
              <h2 class="panel-title">Last collector run</h2>
            </div>

            <div v-if="stats.last_run" class="p-5">
              <div class="mb-5 flex items-center gap-3">
                <span class="relative flex h-2.5 w-2.5">
                  <span
                    class="absolute inline-flex h-full w-full rounded-full opacity-70"
                    :class="stats.last_run.status === 'success' ? 'animate-ping bg-emerald-400' : 'bg-red-400'"
                  ></span>
                  <span
                    class="relative inline-flex h-2.5 w-2.5 rounded-full"
                    :class="stats.last_run.status === 'success' ? 'bg-emerald-400' : 'bg-red-400'"
                  ></span>
                </span>
                <div>
                  <div class="text-sm font-semibold" :class="stats.last_run.status === 'success' ? 'text-emerald-300' : 'text-red-300'">
                    {{ stats.last_run.status }}
                  </div>
                  <div class="font-mono text-[10px] text-gray-600">{{ timeAgo(stats.last_run.started_at) }}</div>
                </div>
              </div>

              <dl class="space-y-2.5 text-[13px]">
                <div class="flex items-center justify-between">
                  <dt class="text-gray-500">Source</dt>
                  <dd class="text-gray-200">{{ sourceLabel(stats.last_run.source) }}</dd>
                </div>
                <div class="flex items-center justify-between">
                  <dt class="text-gray-500">Duration</dt>
                  <dd class="font-mono text-gray-200 tabular-nums">{{ formatNumber(stats.last_run.duration_ms) }} ms</dd>
                </div>
                <div class="flex items-center justify-between">
                  <dt class="text-gray-500">Changes</dt>
                  <dd class="font-mono font-semibold text-cyan-300 tabular-nums">{{ formatNumber(stats.last_run.stats?.changes) }}</dd>
                </div>
                <div class="flex items-center justify-between">
                  <dt class="text-gray-500">New programs</dt>
                  <dd class="font-mono text-gray-200 tabular-nums">{{ formatNumber(stats.last_run.stats?.inserted) }}</dd>
                </div>
              </dl>

              <div class="mt-5 border-t border-white/[0.06] pt-4">
                <RouterLink to="/monitors" class="group flex items-center justify-between text-[12px] font-medium text-cyan-300/90 hover:text-cyan-200">
                  Inspect monitors
                  <svg class="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6" />
                  </svg>
                </RouterLink>
              </div>
            </div>

            <p v-else class="p-5 text-sm text-gray-500">
              The collector has not run yet. Start it with
              <code class="rounded bg-white/5 px-1.5 py-0.5 font-mono text-xs text-cyan-300/80">python monitor.py --once</code>.
            </p>
          </div>
        </div>

        <!-- ══════════ activity + latest changes ══════════ -->
        <div class="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div class="panel overflow-hidden">
            <div class="panel-head">
              <h2 class="panel-title">7-day activity</h2>
              <span class="font-mono text-[10px] text-gray-600">{{ formatNumber(stats.changes_7d) }} total</span>
            </div>

            <div v-if="perDay.length" class="px-5 pb-5 pt-6">
              <div class="flex h-36 items-end justify-between gap-2">
                <div v-for="day in perDay" :key="day.label" class="group flex h-full flex-1 flex-col items-center justify-end gap-2">
                  <span class="font-mono text-[10px] text-gray-600 opacity-0 transition-opacity group-hover:opacity-100">{{ day.value }}</span>
                  <div class="relative w-full max-w-8 overflow-hidden rounded-md bg-white/[0.04]" :style="{ height: `${day.pct}%` }">
                    <div class="absolute inset-0 bg-gradient-to-t from-blue-500/70 via-cyan-400/70 to-cyan-300/90 transition-opacity duration-300 group-hover:opacity-100 opacity-80"></div>
                  </div>
                  <span class="font-mono text-[9px] uppercase tracking-wider text-gray-600">{{ day.label }}</span>
                </div>
              </div>
            </div>
            <p v-else class="p-5 text-sm text-gray-600">No activity recorded yet.</p>
          </div>

          <div class="panel overflow-hidden lg:col-span-2">
            <div class="panel-head">
              <h2 class="panel-title">Latest changes</h2>
              <RouterLink to="/alerts" class="group flex items-center gap-1 font-mono text-[11px] text-cyan-300/70 hover:text-cyan-300">
                view all
                <svg class="h-3 w-3 transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6" />
                </svg>
              </RouterLink>
            </div>

            <div v-if="changes.length" class="divide-y divide-white/[0.06]">
              <div v-for="change in changes" :key="change.id" class="row-hover flex items-center gap-3 px-5 py-2.5">
                <span class="shrink-0 rounded border px-2 py-0.5 font-mono text-[10px]" :class="badgeClass(change.type)">
                  {{ CHANGE_LABELS[change.type] || change.type }}
                </span>
                <span class="flex-1 truncate font-mono text-[12px] text-gray-300">{{ change.target || change.program.name }}</span>
                <span class="hidden shrink-0 font-mono text-[10px] text-gray-500 sm:inline">{{ sourceLabel(change.source) }}</span>
                <span class="w-20 shrink-0 text-right font-mono text-[10px] text-gray-600">{{ timeAgo(change.detected_at) }}</span>
              </div>
            </div>
            <div v-else class="px-5 py-10 text-center text-sm text-gray-600">No changes recorded yet.</div>
          </div>
        </div>
      </AsyncState>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '../../services/api'
import { useApi } from '../../composables/useApi'
import { CHANGE_LABELS, formatNumber, sourceLabel, timeAgo } from '../../utils/format'
import PageHeader from '../ui/PageHeader.vue'
import AsyncState from '../ui/AsyncState.vue'
import StatCard from '../ui/StatCard.vue'

const health = ref({ ok: false })

const { data, error, loading, lastUpdated, load } = useApi(
  async () => {
    const [stats, changes, healthResult] = await Promise.all([
      api.stats(),
      api.changes({ per_page: 8 }),
      api.health(),
    ])
    health.value = healthResult
    return { stats: stats.data, changes: changes.data }
  },
  { refreshInterval: 60000 },
)

const stats = computed(() => data.value?.stats || {
  programs: 0, active_programs: 0, scopes: 0, changes_24h: 0, changes_7d: 0,
  conflicts: 0, sources: [], last_run: null,
})
const changes = computed(() => data.value?.changes || [])

const scheduleSeconds = computed(() => {
  const value = Number(stats.value.schedule_interval || 1800)
  return Number.isFinite(value) ? value : 1800
})

const perDay = computed(() => {
  const values = stats.value.changes_per_day
  if (!Array.isArray(values) || !values.length) return []
  const max = Math.max(...values, 1)
  return values.map((value, i) => ({
    value,
    pct: Math.max(6, Math.round((value / max) * 100)),
    label: new Date(Date.now() - (values.length - 1 - i) * 86400000)
      .toLocaleDateString('en-US', { weekday: 'short' }),
  }))
})

function statusDot(run) {
  if (!run) return 'bg-gray-600'
  return run.status === 'success' ? 'bg-emerald-400' : 'bg-red-400'
}

function badgeClass(type) {
  if (type.endsWith('_removed') || type === 'program_removed') return 'border-red-400/30 bg-red-500/5 text-red-300/90'
  if (type === 'conflict') return 'border-amber-400/30 bg-amber-500/5 text-amber-300/90'
  return 'border-cyan-400/30 bg-cyan-500/5 text-cyan-300/90'
}
</script>
