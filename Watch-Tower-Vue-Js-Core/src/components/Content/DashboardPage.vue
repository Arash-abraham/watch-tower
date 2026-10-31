<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="max-w-7xl mx-auto">
      <PageHeader
        badge="DASHBOARD OVERVIEW"
        title="Dashboard"
        subtitle="Live state of the monitored bounty landscape"
      >
        <template #actions>
          <div class="flex items-center gap-3 text-[11px] font-mono text-gray-600">
            <span class="flex items-center gap-2">
              <span class="w-1.5 h-1.5 rounded-full" :class="health.ok ? 'bg-green-500' : 'bg-red-500'"></span>
              {{ health.ok ? 'API ONLINE' : 'API OFFLINE' }}
            </span>
            <span>·</span>
            <span>updated {{ lastUpdated ? timeAgo(lastUpdated) : '—' }}</span>
            <button
              class="px-2 py-1 border border-gray-800 rounded hover:border-cyan-500/40 hover:text-cyan-400 transition-colors"
              @click="load"
            >
              refresh
            </button>
          </div>
        </template>
      </PageHeader>

      <AsyncState :loading="loading && !stats" :error="error" @retry="load">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <StatCard label="Active Programs" :value="stats.active_programs" accent="cyan" :hint="`${formatNumber(stats.programs)} total · ${formatNumber(stats.programs - stats.active_programs)} closed`" />
          <StatCard label="Assets In Scope" :value="stats.scopes" accent="blue" hint="unique in-scope assets" />
          <StatCard label="Changes · 24h" :value="stats.changes_24h" accent="green" :hint="`${formatNumber(stats.changes_7d)} in the last 7 days`" />
          <StatCard label="Scope Conflicts" :value="stats.conflicts" accent="red" hint="assets in both scope lists" />
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- sources -->
          <div class="lg:col-span-2 bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-800 flex items-center justify-between">
              <h2 class="text-sm font-semibold tracking-wide text-gray-300">SOURCES</h2>
              <span class="text-[10px] font-mono text-gray-600">
                every {{ formatNumber(scheduleSeconds / 60) }} min
              </span>
            </div>

            <div class="divide-y divide-gray-800/70">
              <div
                v-for="source in stats.sources"
                :key="source.source"
                class="px-6 py-4 flex items-center justify-between gap-4 hover:bg-cyan-500/[0.02] transition-colors"
              >
                <div class="flex items-center gap-3 min-w-0">
                  <span
                    class="w-1.5 h-1.5 rounded-full shrink-0"
                    :class="statusDot(source.last_run)"
                  ></span>
                  <div class="min-w-0">
                    <div class="text-sm text-white truncate">{{ sourceLabel(source.source) }}</div>
                    <div class="text-[11px] font-mono text-gray-600">
                      {{ source.last_run ? `last run ${timeAgo(source.last_run.started_at)}` : 'never synced' }}
                    </div>
                  </div>
                </div>
                <div class="flex items-center gap-6 text-right shrink-0">
                  <div>
                    <div class="text-sm text-white tabular-nums">{{ formatNumber(source.active_programs) }}</div>
                    <div class="text-[10px] text-gray-600 font-mono">PROGRAMS</div>
                  </div>
                  <div>
                    <div class="text-sm tabular-nums" :class="source.changes_24h ? 'text-cyan-400' : 'text-gray-500'">
                      {{ formatNumber(source.changes_24h) }}
                    </div>
                    <div class="text-[10px] text-gray-600 font-mono">24H</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- last run -->
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
            <h2 class="text-sm font-semibold tracking-wide text-gray-300 mb-4">LAST COLLECTOR RUN</h2>

            <template v-if="stats.last_run">
              <div class="flex items-center gap-2 mb-4">
                <span class="w-2 h-2 rounded-full" :class="stats.last_run.status === 'success' ? 'bg-green-500' : 'bg-red-500'"></span>
                <span class="text-sm" :class="stats.last_run.status === 'success' ? 'text-green-400' : 'text-red-400'">
                  {{ stats.last_run.status }}
                </span>
                <span class="text-[11px] font-mono text-gray-600">· {{ timeAgo(stats.last_run.started_at) }}</span>
              </div>

              <dl class="space-y-2 text-sm">
                <div class="flex justify-between"><dt class="text-gray-500">Source</dt><dd class="text-gray-300">{{ sourceLabel(stats.last_run.source) }}</dd></div>
                <div class="flex justify-between"><dt class="text-gray-500">Duration</dt><dd class="text-gray-300 tabular-nums">{{ formatNumber(stats.last_run.duration_ms) }} ms</dd></div>
                <div class="flex justify-between"><dt class="text-gray-500">Changes</dt><dd class="text-cyan-400 tabular-nums">{{ formatNumber(stats.last_run.stats?.changes) }}</dd></div>
                <div class="flex justify-between"><dt class="text-gray-500">New programs</dt><dd class="text-gray-300 tabular-nums">{{ formatNumber(stats.last_run.stats?.inserted) }}</dd></div>
              </dl>
            </template>

            <p v-else class="text-sm text-gray-500">
              The collector has not run yet. Start it with
              <code class="text-cyan-400/80 text-xs">python monitor.py --once</code>.
            </p>
          </div>
        </div>

        <!-- recent changes -->
        <div class="mt-6 bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-800 flex items-center justify-between">
            <h2 class="text-sm font-semibold tracking-wide text-gray-300">LATEST CHANGES</h2>
            <RouterLink to="/alerts" class="text-[11px] font-mono text-cyan-400/70 hover:text-cyan-400">
              view all →
            </RouterLink>
          </div>

          <div v-if="changes.length" class="divide-y divide-gray-800/70">
            <div v-for="change in changes" :key="change.id" class="px-6 py-3 flex items-center gap-4">
              <span class="text-[10px] font-mono px-2 py-1 rounded border shrink-0" :class="badgeClass(change.type)">
                {{ CHANGE_LABELS[change.type] || change.type }}
              </span>
              <span class="text-sm text-gray-300 truncate flex-1 font-mono">{{ change.target || change.program.name }}</span>
              <span class="text-[11px] text-gray-600 shrink-0">{{ sourceLabel(change.source) }}</span>
              <span class="text-[11px] text-gray-600 shrink-0 w-20 text-right">{{ timeAgo(change.detected_at) }}</span>
            </div>
          </div>
          <div v-else class="px-6 py-8 text-center text-sm text-gray-600">
            No changes recorded yet.
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

function statusDot(run) {
  if (!run) return 'bg-gray-600'
  return run.status === 'success' ? 'bg-green-500' : 'bg-red-500'
}

function badgeClass(type) {
  if (type.endsWith('_removed') || type === 'program_removed') return 'border-red-500/30 text-red-400/90 bg-red-500/5'
  if (type === 'conflict') return 'border-yellow-500/30 text-yellow-400/90 bg-yellow-500/5'
  return 'border-cyan-500/30 text-cyan-400/90 bg-cyan-500/5'
}
</script>
