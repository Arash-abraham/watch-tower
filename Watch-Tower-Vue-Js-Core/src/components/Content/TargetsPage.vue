<template>
  <div class="pt-24 pb-16 text-white">
    <div class="container-page">
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
              :class="viewMode === mode ? 'border-cyan-400/50 bg-cyan-400/10 text-cyan-300' : 'border-white/10 text-gray-500 hover:border-white/20 hover:text-gray-300'"
              @click="viewMode = mode"
            >
              {{ mode }}
            </button>
          </div>
        </template>
      </PageHeader>

      <!-- filters -->
      <div class="panel mb-6 flex flex-col gap-3 p-3 lg:flex-row">
        <div class="relative flex-1">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="filters.q"
            type="text"
            placeholder="Search program name, URL or asset…"
            class="field pl-10 font-mono"
          />
        </div>

        <select v-model="filters.source" class="field w-auto min-w-[9rem] cursor-pointer">
          <option value="">All sources</option>
          <option v-for="source in availableSources" :key="source" :value="source">{{ sourceLabel(source) }}</option>
        </select>

        <select v-model="filters.active" class="field w-auto min-w-[9rem] cursor-pointer">
          <option value="">Any status</option>
          <option value="1">Active only</option>
          <option value="0">Closed only</option>
        </select>

        <select v-model="filters.sort" class="field w-auto min-w-[9rem] cursor-pointer">
          <option value="name">Sort: name</option>
          <option value="updated">Sort: last update</option>
          <option value="source">Sort: source</option>
        </select>
      </div>

      <!-- summary -->
      <div class="mb-4 flex items-center justify-between font-mono text-[11px] text-gray-600">
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
            class="panel p-5 hover:border-cyan-500/30 transition-colors"
          >
            <div class="flex items-start justify-between gap-3 mb-3">
              <div class="min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <span class="h-1.5 w-1.5 rounded-full" :class="program.active ? 'bg-emerald-400' : 'bg-gray-600'"></span>
                  <span class="text-[10px] font-mono uppercase tracking-wider text-cyan-400/70">{{ sourceLabel(program.source) }}</span>
                  <span v-if="program.conflicts?.length" class="text-[10px] font-mono text-yellow-500/80">conflict</span>
                </div>
                <h3 class="text-base font-semibold text-white break-words">
                  <RouterLink
                    :to="{ name: 'program-detail', params: { id: program.id } }"
                    class="transition-colors hover:text-cyan-300"
                    title="View the full program dossier"
                  >
                    {{ program.name }}
                  </RouterLink>
                </h3>
              </div>
              <a
                v-if="program.url"
                :href="program.url"
                target="_blank"
                rel="noopener noreferrer"
                class="shrink-0 rounded-md border border-white/10 px-2 py-0.5 font-mono text-[10px] text-gray-500 transition-colors hover:border-cyan-400/40 hover:text-cyan-300"
              >
                open ↗
              </a>
            </div>

            <div class="flex flex-wrap gap-2 mb-4">
              <RouterLink
                :to="{ name: 'program-detail', params: { id: program.id }, hash: '#in-scope' }"
                class="rounded border border-cyan-400/20 bg-cyan-400/[0.06] px-2 py-0.5 font-mono text-[10px] text-cyan-300/80 transition-colors hover:border-cyan-400/50 hover:text-cyan-300"
                title="View every in-scope asset"
              >
                {{ program.scopes.length }} in scope
              </RouterLink>
              <RouterLink
                :to="{ name: 'program-detail', params: { id: program.id }, hash: '#out-of-scope' }"
                class="rounded border border-white/10 px-2 py-0.5 font-mono text-[10px] text-gray-500 transition-colors hover:border-cyan-400/40 hover:text-cyan-300"
                title="View every out-of-scope asset"
              >
                {{ program.out_of_scope.length }} out
              </RouterLink>
              <span v-if="payout(program)" class="rounded border border-emerald-400/20 bg-emerald-400/[0.06] px-2 py-0.5 font-mono text-[10px] text-emerald-300/80">
                max {{ payout(program) }}
              </span>
              <span v-if="program.meta?.offers_bounties" class="rounded border border-blue-400/20 bg-blue-400/[0.06] px-2 py-0.5 font-mono text-[10px] text-blue-300/80">
                bounty
              </span>
            </div>

            <!-- short preview only — the complete lists live on the detail page -->
            <ul class="space-y-1 mb-3">
              <li
                v-for="asset in visibleScopes(program)"
                :key="asset.target || asset"
                class="text-xs font-mono text-gray-400 flex items-start gap-2"
              >
                <span class="text-cyan-500/50">›</span>
                <span class="min-w-0 break-all">{{ asset.target || asset }}</span>
                <span v-if="asset.type" class="text-[10px] text-gray-600 shrink-0">{{ asset.type }}</span>
              </li>
              <li v-if="program.scopes.length === 0" class="text-xs text-gray-600">no in-scope assets</li>
              <li v-if="program.scopes.length > 4">
                <RouterLink
                  :to="{ name: 'program-detail', params: { id: program.id }, hash: '#in-scope' }"
                  class="text-[11px] font-mono text-cyan-300/70 transition-colors hover:text-cyan-300"
                >
                  + {{ program.scopes.length - 4 }} more in scope →
                </RouterLink>
              </li>
            </ul>

            <div class="mt-4 pt-3 border-t border-white/[0.06] flex items-center justify-between gap-3 text-[10px] font-mono text-gray-600">
              <span class="min-w-0 break-all">{{ program.slug }}</span>
              <span class="shrink-0">{{ program.last_synced_at ? timeAgo(program.last_synced_at) : 'never synced' }}</span>
            </div>

            <!-- opens the full dossier (all scopes, paginated) in a new tab -->
            <RouterLink
              :to="{ name: 'program-detail', params: { id: program.id } }"
              target="_blank"
              class="mt-3 flex items-center justify-center gap-2 rounded-lg border border-cyan-400/20 bg-cyan-400/[0.05] px-3 py-2 font-mono text-[11px] uppercase tracking-wider text-cyan-300/80 transition-colors hover:border-cyan-400/50 hover:bg-cyan-400/10 hover:text-cyan-300"
            >
              view full program ↗
            </RouterLink>
          </article>
        </div>

        <!-- list -->
        <div v-else class="panel overflow-hidden">
          <table class="w-full text-sm">
            <thead class="text-[10px] font-mono uppercase tracking-wider text-gray-600 border-b border-white/[0.06]">
              <tr>
                <th class="text-left px-4 py-3 font-normal">Program</th>
                <th class="text-left px-4 py-3 font-normal">Source</th>
                <th class="text-right px-4 py-3 font-normal">In scope</th>
                <th class="text-right px-4 py-3 font-normal">Out</th>
                <th class="text-right px-4 py-3 font-normal">Updated</th>
                <th class="text-right px-4 py-3 font-normal">Details</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/[0.06]">
              <tr v-for="program in programs" :key="program.id" class="row-hover">
                <td class="px-4 py-3 text-gray-200 break-words">
                  <RouterLink
                    :to="{ name: 'program-detail', params: { id: program.id } }"
                    class="transition-colors hover:text-cyan-300"
                    title="View the full program dossier"
                  >
                    {{ program.name }}
                  </RouterLink>
                </td>
                <td class="px-4 py-3 text-[11px] font-mono text-cyan-400/70">{{ sourceLabel(program.source) }}</td>
                <td class="px-4 py-3 text-right tabular-nums text-gray-300">{{ program.scopes.length }}</td>
                <td class="px-4 py-3 text-right tabular-nums text-gray-500">{{ program.out_of_scope.length }}</td>
                <td class="px-4 py-3 text-right text-[11px] text-gray-600">{{ timeAgo(program.last_synced_at) }}</td>
                <td class="px-4 py-3 text-right">
                  <RouterLink
                    :to="{ name: 'program-detail', params: { id: program.id } }"
                    target="_blank"
                    class="font-mono text-[11px] text-cyan-300/70 transition-colors hover:text-cyan-300"
                    title="Open the full dossier in a new tab"
                  >
                    open ↗
                  </RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- pagination -->
        <Pagination v-model:page="page" :last-page="meta.last_page || 1" :total="meta.total ?? null" />
      </AsyncState>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '../../services/api'
import { useApi } from '../../composables/useApi'
import { formatMoney, formatNumber, sourceLabel, timeAgo } from '../../utils/format'
import PageHeader from '../ui/PageHeader.vue'
import AsyncState from '../ui/AsyncState.vue'
import Pagination from '../ui/Pagination.vue'

const availableSources = ['bugcrowd', 'hackerone', 'yeswehack', 'intigriti', 'local']

const filters = reactive({ q: '', source: '', active: '', sort: 'name' })
const page = ref(1)
const viewMode = ref('grid')

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

function visibleScopes(program) {
  const details = program.scope_details?.in
  if (Array.isArray(details) && details.length) return details.slice(0, 4)
  return program.scopes.slice(0, 4)
}

function payout(program) {
  return formatMoney(program.meta?.max_payout ?? program.meta?.max_bounty, program.meta?.currency)
}
</script>
