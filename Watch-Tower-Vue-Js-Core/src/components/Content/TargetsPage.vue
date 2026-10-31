<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="max-w-7xl mx-auto">
      <PageHeader
        badge="TARGET INTELLIGENCE"
        title="Attack Surface"
        subtitle="In-scope and out-of-scope assets for every monitored program"
      >
        <template #actions>
          <div class="flex items-center gap-2">
            <button
              v-for="mode in ['grid', 'list']"
              :key="mode"
              class="px-3 py-1.5 text-[11px] font-mono uppercase tracking-wider border rounded-lg transition-colors"
              :class="viewMode === mode ? 'border-cyan-500/50 text-cyan-400 bg-cyan-500/10' : 'border-gray-800 text-gray-500 hover:text-gray-300'"
              @click="viewMode = mode"
            >
              {{ mode }}
            </button>
          </div>
        </template>
      </PageHeader>

      <!-- filters -->
      <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-4 mb-6 flex flex-col lg:flex-row gap-3">
        <div class="relative flex-1">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="filters.q"
            type="text"
            placeholder="Search program name, URL or asset…"
            class="w-full bg-black/40 border border-gray-800 rounded-lg pl-10 pr-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-cyan-500/40 font-mono"
          />
        </div>

        <select v-model="filters.source" class="bg-black/40 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-cyan-500/40">
          <option value="">All sources</option>
          <option v-for="source in availableSources" :key="source" :value="source">{{ sourceLabel(source) }}</option>
        </select>

        <select v-model="filters.active" class="bg-black/40 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-cyan-500/40">
          <option value="">Any status</option>
          <option value="1">Active only</option>
          <option value="0">Closed only</option>
        </select>

        <select v-model="filters.sort" class="bg-black/40 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-cyan-500/40">
          <option value="name">Sort: name</option>
          <option value="updated">Sort: last update</option>
          <option value="source">Sort: source</option>
        </select>
      </div>

      <!-- summary -->
      <div class="flex items-center justify-between mb-4 text-[11px] font-mono text-gray-600">
        <span>
          {{ formatNumber(meta.total || 0) }} program(s) ·
          page {{ meta.current_page || 1 }} / {{ meta.last_page || 1 }}
        </span>
        <span v-if="filters.q || filters.source || filters.active">filtered</span>
      </div>

      <AsyncState
        :loading="loading"
        :error="error"
        :empty="!loading && !error && programs.length === 0"
        empty-text="No programs match these filters."
        empty-hint="Run the collector (python monitor.py --once) to populate the database."
        @retry="load"
      >
        <!-- grid -->
        <div v-if="viewMode === 'grid'" class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <article
            v-for="program in programs"
            :key="program.id"
            class="bg-gray-900/40 border border-gray-800 rounded-xl p-5 hover:border-cyan-500/30 transition-colors"
          >
            <div class="flex items-start justify-between gap-3 mb-3">
              <div class="min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <span class="w-1.5 h-1.5 rounded-full" :class="program.active ? 'bg-green-500' : 'bg-gray-600'"></span>
                  <span class="text-[10px] font-mono uppercase tracking-wider text-cyan-400/70">{{ sourceLabel(program.source) }}</span>
                  <span v-if="program.conflicts?.length" class="text-[10px] font-mono text-yellow-500/80">conflict</span>
                </div>
                <h3 class="text-base font-semibold text-white truncate">{{ program.name }}</h3>
              </div>
              <a
                v-if="program.url"
                :href="program.url"
                target="_blank"
                rel="noopener noreferrer"
                class="text-[11px] font-mono text-gray-500 hover:text-cyan-400 transition-colors shrink-0"
              >
                open ↗
              </a>
            </div>

            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-2 py-0.5 text-[10px] font-mono border border-cyan-500/20 text-cyan-400/80 rounded">
                {{ program.scopes.length }} in scope
              </span>
              <span class="px-2 py-0.5 text-[10px] font-mono border border-gray-700 text-gray-500 rounded">
                {{ program.out_of_scope.length }} out
              </span>
              <span v-if="payout(program)" class="px-2 py-0.5 text-[10px] font-mono border border-green-500/20 text-green-400/80 rounded">
                max {{ payout(program) }}
              </span>
              <span v-if="program.meta?.offers_bounties" class="px-2 py-0.5 text-[10px] font-mono border border-blue-500/20 text-blue-400/80 rounded">
                bounty
              </span>
            </div>

            <ul class="space-y-1 mb-3">
              <li
                v-for="asset in visibleScopes(program)"
                :key="asset.target || asset"
                class="text-xs font-mono text-gray-400 truncate flex items-center gap-2"
              >
                <span class="text-cyan-500/50">›</span>
                <span class="truncate">{{ asset.target || asset }}</span>
                <span v-if="asset.type" class="text-[10px] text-gray-600 shrink-0">{{ asset.type }}</span>
              </li>
              <li v-if="program.scopes.length === 0" class="text-xs text-gray-600">no in-scope assets</li>
            </ul>

            <button
              v-if="program.out_of_scope.length"
              class="text-[11px] font-mono text-gray-500 hover:text-gray-300 transition-colors"
              @click="toggle(program.id)"
            >
              {{ expanded[program.id] ? '− hide' : '+' }} out-of-scope ({{ program.out_of_scope.length }})
            </button>

            <ul v-if="expanded[program.id]" class="mt-2 space-y-1 pl-4 border-l border-gray-800">
              <li v-for="asset in program.out_of_scope" :key="asset" class="text-[11px] font-mono text-gray-600 truncate">
                {{ typeof asset === 'string' ? asset : asset.target }}
              </li>
            </ul>

            <div class="mt-4 pt-3 border-t border-gray-800/70 flex items-center justify-between text-[10px] font-mono text-gray-600">
              <span>{{ program.slug }}</span>
              <span>{{ program.last_synced_at ? timeAgo(program.last_synced_at) : 'never synced' }}</span>
            </div>
          </article>
        </div>

        <!-- list -->
        <div v-else class="bg-gray-900/40 border border-gray-800 rounded-xl overflow-hidden">
          <table class="w-full text-sm">
            <thead class="text-[10px] font-mono uppercase tracking-wider text-gray-600 border-b border-gray-800">
              <tr>
                <th class="text-left px-4 py-3 font-normal">Program</th>
                <th class="text-left px-4 py-3 font-normal">Source</th>
                <th class="text-right px-4 py-3 font-normal">In scope</th>
                <th class="text-right px-4 py-3 font-normal">Out</th>
                <th class="text-right px-4 py-3 font-normal">Updated</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-800/70">
              <tr v-for="program in programs" :key="program.id" class="hover:bg-cyan-500/[0.02]">
                <td class="px-4 py-3 text-gray-200 truncate max-w-[220px]">{{ program.name }}</td>
                <td class="px-4 py-3 text-[11px] font-mono text-cyan-400/70">{{ sourceLabel(program.source) }}</td>
                <td class="px-4 py-3 text-right tabular-nums text-gray-300">{{ program.scopes.length }}</td>
                <td class="px-4 py-3 text-right tabular-nums text-gray-500">{{ program.out_of_scope.length }}</td>
                <td class="px-4 py-3 text-right text-[11px] text-gray-600">{{ timeAgo(program.last_synced_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- pagination -->
        <div v-if="(meta.last_page || 1) > 1" class="flex items-center justify-center gap-2 mt-8">
          <button
            class="px-3 py-1.5 text-xs font-mono border border-gray-800 rounded-lg text-gray-400 hover:text-cyan-400 hover:border-cyan-500/40 disabled:opacity-30 disabled:hover:text-gray-400 transition-colors"
            :disabled="page <= 1"
            @click="page--"
          >
            ← prev
          </button>
          <span class="text-xs font-mono text-gray-500 px-3">{{ meta.current_page }} / {{ meta.last_page }}</span>
          <button
            class="px-3 py-1.5 text-xs font-mono border border-gray-800 rounded-lg text-gray-400 hover:text-cyan-400 hover:border-cyan-500/40 disabled:opacity-30 disabled:hover:text-gray-400 transition-colors"
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
import { formatMoney, formatNumber, sourceLabel, timeAgo } from '../../utils/format'
import PageHeader from '../ui/PageHeader.vue'
import AsyncState from '../ui/AsyncState.vue'

const availableSources = ['bugcrowd', 'hackerone', 'yeswehack', 'intigriti', 'local']

const filters = reactive({ q: '', source: '', active: '', sort: 'name' })
const page = ref(1)
const viewMode = ref('grid')
const expanded = reactive({})

const { data, error, loading, load } = useApi(() =>
  api.programs({
    q: filters.q,
    source: filters.source,
    active: filters.active,
    sort: filters.sort,
    page: page.value,
    per_page: 12,
  }),
)

const programs = computed(() => data.value?.data || [])
const meta = computed(() => data.value?.meta || {})

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

function toggle(id) {
  expanded[id] = !expanded[id]
}

function visibleScopes(program) {
  const details = program.scope_details?.in
  if (Array.isArray(details) && details.length) return details.slice(0, 4)
  return program.scopes.slice(0, 4)
}

function payout(program) {
  return formatMoney(program.meta?.max_payout ?? program.meta?.max_bounty, program.meta?.currency)
}
</script>
