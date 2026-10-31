<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="max-w-7xl mx-auto">
      <PageHeader
        badge="MONITORS"
        title="Monitors"
        subtitle="Collector health, schedule and what is being watched"
      >
        <template #actions>
          <button
            class="px-3 py-1.5 text-[11px] font-mono uppercase tracking-wider border border-gray-800 rounded-lg text-gray-400 hover:text-cyan-400 hover:border-cyan-500/40 transition-colors"
            @click="refresh"
          >
            re-check
          </button>
        </template>
      </PageHeader>

      <AsyncState :loading="loading && !stats" :error="error" @retry="refresh">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <!-- collector -->
          <div class="bg-gray-900/40 border border-gray-800 rounded-xl p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-semibold tracking-wide text-gray-300">COLLECTOR</h3>
              <span class="w-2 h-2 rounded-full" :class="health.ok ? 'bg-green-500' : 'bg-red-500'"></span>
            </div>
            <div class="text-2xl font-bold mb-1" :class="health.ok ? 'text-green-400' : 'text-red-400'">
              {{ health.ok ? 'Healthy' : 'Unreachable' }}
            </div>
            <p class="text-[11px] font-mono text-gray-600">
              {{ health.service || 'watch-tower-api' }} · v{{ health.version || '—' }}
            </p>
            <p v-if="health.mongo !== undefined" class="text-[11px] font-mono mt-3" :class="health.mongo ? 'text-gray-500' : 'text-red-400'">
              mongo: {{ health.mongo ? 'connected' : 'unavailable' }}
            </p>
          </div>

          <!-- schedule -->
          <div class="bg-gray-900/40 border border-gray-800 rounded-xl p-6">
            <h3 class="text-sm font-semibold tracking-wide text-gray-300 mb-4">SCHEDULE</h3>
            <div class="text-2xl font-bold text-white mb-1 tabular-nums">
              {{ scheduleLabel }}
            </div>
            <p class="text-[11px] font-mono text-gray-600">between collector runs</p>

            <div class="mt-4 pt-4 border-t border-gray-800/70 space-y-2 text-xs">
              <div class="flex justify-between"><span class="text-gray-500">Last run</span><span class="text-gray-300">{{ stats.last_run ? timeAgo(stats.last_run.started_at) : 'never' }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Duration</span><span class="text-gray-300 tabular-nums">{{ stats.last_run ? `${formatNumber(stats.last_run.duration_ms)} ms` : '—' }}</span></div>
            </div>
          </div>

          <!-- volume -->
          <div class="bg-gray-900/40 border border-gray-800 rounded-xl p-6">
            <h3 class="text-sm font-semibold tracking-wide text-gray-300 mb-4">VOLUME</h3>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between"><span class="text-gray-500">Programs</span><span class="text-white tabular-nums">{{ formatNumber(stats.programs) }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">In-scope assets</span><span class="text-white tabular-nums">{{ formatNumber(stats.scopes) }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Changes (24h)</span><span class="text-cyan-400 tabular-nums">{{ formatNumber(stats.changes_24h) }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Conflicts</span><span :class="stats.conflicts ? 'text-yellow-400 tabular-nums' : 'text-gray-400 tabular-nums'">{{ formatNumber(stats.conflicts) }}</span></div>
            </div>
          </div>
        </div>

        <!-- what is monitored -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-gray-900/40 border border-gray-800 rounded-xl overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-800">
              <h3 class="text-sm font-semibold tracking-wide text-gray-300">ACTIVE MONITORS</h3>
            </div>
            <div class="divide-y divide-gray-800/70">
              <div v-for="monitor in monitors" :key="monitor.name" class="px-6 py-4">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-sm text-white">{{ monitor.name }}</span>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded border" :class="monitor.enabled ? 'border-green-500/30 text-green-400/80 bg-green-500/5' : 'border-gray-700 text-gray-500'">
                    {{ monitor.enabled ? 'ACTIVE' : 'PLANNED' }}
                  </span>
                </div>
                <p class="text-[11px] text-gray-500">{{ monitor.description }}</p>
              </div>
            </div>
          </div>

          <div class="bg-gray-900/40 border border-gray-800 rounded-xl overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-800">
              <h3 class="text-sm font-semibold tracking-wide text-gray-300">SOURCE FRESHNESS</h3>
            </div>
            <div class="divide-y divide-gray-800/70">
              <div v-for="source in stats.sources" :key="source.source" class="px-6 py-3 flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span class="w-1.5 h-1.5 rounded-full" :class="source.last_run?.status === 'success' ? 'bg-green-500' : source.last_run ? 'bg-red-500' : 'bg-gray-600'"></span>
                  <span class="text-sm text-gray-300">{{ sourceLabel(source.source) }}</span>
                </div>
                <span class="text-[11px] font-mono text-gray-600">
                  {{ source.last_run ? timeAgo(source.last_run.started_at) : 'never synced' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </AsyncState>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { api } from '../../services/api'
import { useApi } from '../../composables/useApi'
import { formatNumber, sourceLabel, timeAgo } from '../../utils/format'
import PageHeader from '../ui/PageHeader.vue'
import AsyncState from '../ui/AsyncState.vue'

const health = ref({ ok: false })

const { data, error, loading, load } = useApi(async () => {
  const [stats, healthResult] = await Promise.all([api.stats(), api.health()])
  health.value = healthResult
  return stats.data
})

const stats = computed(() => data.value || {
  programs: 0, scopes: 0, changes_24h: 0, conflicts: 0, sources: [], last_run: null,
})

const scheduleLabel = computed(() => {
  const seconds = Number(data.value?.schedule_interval || 1800)
  if (!Number.isFinite(seconds) || seconds <= 0) return '—'
  if (seconds < 3600) return `${Math.round(seconds / 60)} min`
  return `${(seconds / 3600).toFixed(1)} h`
})

const monitors = computed(() => [
  {
    name: 'Scope change monitor',
    description: 'Compares every program snapshot with the previous one and records added/removed assets.',
    enabled: true,
  },
  {
    name: 'New program monitor',
    description: 'Flags programs that appear in a source for the first time.',
    enabled: true,
  },
  {
    name: 'Out-of-scope monitor',
    description: 'Tracks changes in out-of-scope lists, including conflicts with in-scope assets.',
    enabled: true,
  },
  {
    name: 'Asset discovery (subdomains)',
    description: 'Reserved collection; enumeration is not implemented yet.',
    enabled: false,
  },
])

function refresh() {
  load()
}
</script>
