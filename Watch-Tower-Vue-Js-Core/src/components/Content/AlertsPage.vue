<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="max-w-7xl mx-auto">
      <PageHeader
        badge="ALERTS"
        title="Alerts"
        subtitle="Every scope change detected by the collector, newest first"
      >
        <template #actions>
          <div class="text-[11px] font-mono text-gray-600">
            updated {{ lastUpdated ? timeAgo(lastUpdated) : '—' }}
          </div>
        </template>
      </PageHeader>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard label="Total Alerts" :value="counts.total" accent="cyan" />
        <StatCard label="Last 24h" :value="counts.last_24h" accent="green" />
        <StatCard label="Last 7 days" :value="counts.last_7d" accent="blue" />
        <StatCard label="Not Notified" :value="counts.unnotified" accent="yellow" hint="pending delivery to Telegram/Discord" />
      </div>

      <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-4 mb-6 flex flex-col lg:flex-row gap-3">
        <div class="relative flex-1">
          <input
            v-model="filters.q"
            type="text"
            placeholder="Search target or program…"
            class="w-full bg-black/40 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-cyan-500/40 font-mono"
          />
        </div>

        <select v-model="filters.type" class="bg-black/40 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-cyan-500/40">
          <option value="">All types</option>
          <option v-for="(label, value) in CHANGE_LABELS" :key="value" :value="value">{{ label }}</option>
        </select>

        <select v-model="filters.source" class="bg-black/40 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-cyan-500/40">
          <option value="">All sources</option>
          <option v-for="source in availableSources" :key="source" :value="source">{{ sourceLabel(source) }}</option>
        </select>
      </div>

      <AsyncState
        :loading="loading"
        :error="error"
        :empty="!loading && !error && changes.length === 0"
        empty-text="No alerts recorded yet."
        empty-hint="Alerts appear as soon as the collector detects a scope change."
        @retry="load"
      >
        <div class="bg-gray-900/40 border border-gray-800 rounded-xl overflow-hidden">
          <div class="divide-y divide-gray-800/70">
            <div
              v-for="change in changes"
              :key="change.id"
              class="px-5 py-4 flex items-start gap-4 hover:bg-cyan-500/[0.02] transition-colors"
            >
              <span class="mt-1 w-1.5 h-1.5 rounded-full shrink-0" :class="dotClass(change.type)"></span>

              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-2 flex-wrap mb-1">
                  <span class="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 border rounded" :class="badgeClass(change.type)">
                    {{ CHANGE_LABELS[change.type] || change.type }}
                  </span>
                  <span class="text-[10px] font-mono text-cyan-400/60">{{ sourceLabel(change.source) }}</span>
                  <span v-if="change.asset_type" class="text-[10px] font-mono text-gray-600">{{ change.asset_type }}</span>
                </div>

                <div class="text-sm text-gray-200 font-mono truncate">
                  {{ change.target || change.program.name }}
                </div>

                <div class="text-[11px] text-gray-600 mt-1">
                  {{ change.program.name }}
                </div>
              </div>

              <div class="text-right shrink-0">
                <div class="text-[11px] text-gray-500">{{ timeAgo(change.detected_at) }}</div>
                <div class="text-[10px] font-mono mt-1" :class="change.notified ? 'text-green-500/70' : 'text-yellow-500/70'">
                  {{ change.notified ? 'notified' : 'pending' }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="(meta.last_page || 1) > 1" class="flex items-center justify-center gap-2 mt-8">
          <button
            class="px-3 py-1.5 text-xs font-mono border border-gray-800 rounded-lg text-gray-400 hover:text-cyan-400 hover:border-cyan-500/40 disabled:opacity-30 transition-colors"
            :disabled="page <= 1"
            @click="page--"
          >
            ← prev
          </button>
          <span class="text-xs font-mono text-gray-500 px-3">{{ meta.current_page }} / {{ meta.last_page }}</span>
          <button
            class="px-3 py-1.5 text-xs font-mono border border-gray-800 rounded-lg text-gray-400 hover:text-cyan-400 hover:border-cyan-500/40 disabled:opacity-30 transition-colors"
            :disabled="page >= (meta.last_page || 1)"
            @click="page++"
          >
            next →
          </button>
        </div>
      </AsyncState>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { api } from '../../services/api'
import { useApi } from '../../composables/useApi'
import { CHANGE_LABELS, sourceLabel, timeAgo } from '../../utils/format'
import PageHeader from '../ui/PageHeader.vue'
import AsyncState from '../ui/AsyncState.vue'
import StatCard from '../ui/StatCard.vue'

const availableSources = ['bugcrowd', 'hackerone', 'yeswehack', 'intigriti', 'local']

const filters = reactive({ q: '', type: '', source: '' })
const page = ref(1)

const { data, error, loading, lastUpdated, load } = useApi(async () => {
  const [changes, counts] = await Promise.all([
    api.changes({
      q: filters.q,
      type: filters.type,
      source: filters.source,
      page: page.value,
      per_page: 20,
    }),
    api.changeCounts(),
  ])
  return { changes, counts: counts.data }
})

const changes = computed(() => data.value?.changes?.data || [])
const meta = computed(() => data.value?.changes?.meta || {})
const counts = computed(() => data.value?.counts || { total: 0, last_24h: 0, last_7d: 0, unnotified: 0 })

let debounce = null
watch(
  () => ({ ...filters }),
  () => {
    clearTimeout(debounce)
    debounce = setTimeout(() => {
      page.value = 1
      load()
    }, 300)
  },
  { deep: true },
)

watch(page, load)

function badgeClass(type) {
  if (type?.endsWith('_removed') || type === 'program_removed') {
    return 'border-red-500/30 text-red-400/90 bg-red-500/5'
  }
  if (type === 'conflict') {
    return 'border-yellow-500/30 text-yellow-400/90 bg-yellow-500/5'
  }
  return 'border-cyan-500/30 text-cyan-400/90 bg-cyan-500/5'
}

function dotClass(type) {
  if (type?.endsWith('_removed') || type === 'program_removed') return 'bg-red-500'
  if (type === 'conflict') return 'bg-yellow-500'
  return 'bg-cyan-500'
}
</script>
