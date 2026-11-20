<template>
  <section id="discovered-subdomains" class="panel mb-6 scroll-mt-24 overflow-hidden" aria-labelledby="discovery-title">
    <header class="border-b border-white/[0.06] p-5 sm:p-6">
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p class="mb-2 font-mono text-[10px] uppercase tracking-widest text-cyan-400/80">Passive inventory</p>
          <h2 id="discovery-title" class="text-lg font-semibold text-white">Discovered subdomains</h2>
          <p class="mt-2 max-w-3xl text-sm text-gray-400">
            Subdomains collected for this program. These are historical observations, not a check that a name is online or currently in scope.
          </p>
        </div>
        <button type="button" class="btn-ghost text-xs disabled:opacity-50" :disabled="loading || loadingRun" @click="refresh">
          {{ loadingRun ? 'Refreshing…' : 'Refresh discovery' }}
        </button>
      </div>

      <div v-if="run" class="mt-5 rounded-xl border border-white/10 bg-black/25 p-4">
        <div class="flex flex-wrap items-center gap-x-3 gap-y-2">
          <span class="font-mono text-[10px] uppercase tracking-widest text-gray-400">Latest run</span>
          <span class="rounded border px-2 py-0.5 font-mono text-[10px] uppercase tracking-wide" :class="statusClass">
            {{ statusLabel }}
          </span>
          <span class="text-xs text-gray-400">{{ formatDateTime(run.finished_at) }}</span>
        </div>
        <p class="mt-2 text-sm text-gray-300">
          {{ formatNumber(run.hosts) }} distinct {{ run.hosts === 1 ? 'name' : 'names' }} across
          {{ formatNumber(run.roots) }} wildcard {{ run.roots === 1 ? 'root' : 'roots' }}.
        </p>
        <p v-if="run.status === 'blocked_scope'" class="mt-1 text-xs text-yellow-200/80">
          Collection was skipped because an exclusion could not be interpreted. Review the program rules before running it again.
        </p>
        <p v-else-if="run.failures" class="mt-1 text-xs text-yellow-200/80">
          Some provider requests failed. Previously collected results remain available.
        </p>
        <p v-if="run.limited" class="mt-1 text-xs text-yellow-200/80">
          Some sources reached a page or result limit. The names already collected are shown below.
        </p>
        <div v-if="run.roots" class="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          <div v-for="(summary, provider) in run.providers" :key="provider" class="rounded-lg border border-white/[0.08] px-3 py-2">
            <p class="text-xs font-medium text-gray-200">{{ providerLabel(provider) }}</p>
            <p class="mt-1 font-mono text-[11px] text-gray-400">
              {{ formatNumber(summary.hosts) }} matched · {{ formatNumber(summary.exclusive_hosts) }} only from this collector
            </p>
            <p class="mt-1 font-mono text-[11px] text-gray-400">
              {{ formatNumber(summary.succeeded) }} responded · {{ formatNumber(summary.failures) }} failed
              <span v-if="summary.limited"> · {{ formatNumber(summary.limited) }} limited</span>
            </p>
          </div>
        </div>
      </div>
      <p v-else class="mt-4 text-xs text-gray-400">No run summary yet. Collection is started manually from the collector CLI.</p>
      <p v-if="runError" role="status" class="mt-2 text-xs text-red-300">Could not refresh the latest run: {{ runError }}</p>
    </header>

    <div role="search" aria-label="Filter discovered subdomains" class="flex flex-wrap items-center gap-3 border-b border-white/[0.06] p-4 sm:px-6">
      <input v-model="query" type="search" class="field min-w-[12rem] flex-1 font-mono text-xs" maxlength="253"
        placeholder="Search subdomains…" aria-label="Search subdomains by hostname" />
      <button v-if="providerFilter" type="button" class="chip transition-colors hover:text-cyan-300" @click="setProvider('')">
        {{ providerLabel(providerFilter) }} <span aria-hidden="true">×</span><span class="sr-only"> (clear source filter)</span>
      </button>
      <span v-if="!loading && !error && data" aria-live="polite" class="font-mono text-xs text-gray-400">
        {{ formatNumber(meta.total ?? 0) }} {{ query.trim() || providerFilter ? 'matches' : meta.total === 1 ? 'subdomain' : 'subdomains' }}
      </span>
    </div>

    <div class="p-4 sm:p-6" :aria-busy="loading">
      <AsyncState :loading="loading" :error="error" :empty="!rows.length"
        :empty-text="query.trim() || providerFilter ? 'No matching subdomains.' : 'No subdomains recorded for this program.'"
        :empty-hint="query.trim() || providerFilter ? 'Try a different search or clear the source filter.' : 'Results appear after a manual passive collection run.'"
        @retry="load">
        <ul class="divide-y divide-white/[0.07]" aria-label="Historical subdomain observations">
          <li v-for="asset in rows" :key="asset.id" class="grid gap-3 py-3 first:pt-0 md:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)_auto] md:items-start">
            <span class="break-all font-mono text-sm text-cyan-100">{{ asset.host }}</span>
            <div class="flex flex-wrap items-center gap-2">
              <span v-if="!Object.keys(asset.observations || {}).length" class="text-xs text-gray-400">Source not recorded</span>
              <div v-for="(seen, source) in asset.observations" :key="source"
                class="flex flex-col gap-1 rounded-lg border border-cyan-500/20 bg-cyan-400/[0.04] px-2 py-1.5">
                <button type="button" class="text-left font-mono text-[11px] text-cyan-200 hover:underline"
                  :aria-label="`Filter by ${providerLabel(source)}`" @click="setProvider(source)">{{ providerLabel(source) }}</button>
                <time :datetime="seen" class="text-[10px] text-gray-400">{{ formatDateTime(seen) }}</time>
              </div>
            </div>
            <div class="text-xs text-gray-400 md:text-right">
              <span>Last collected</span>
              <time :datetime="asset.last_seen_at" class="ml-1 text-gray-300 md:ml-0 md:block">{{ formatDateTime(asset.last_seen_at) }}</time>
            </div>
          </li>
        </ul>
        <Pagination :page="page" :last-page="meta.last_page ?? 1" :total="meta.total ?? null" @update:page="go" />
      </AsyncState>
    </div>
  </section>
</template>

<script setup>
import { computed, onUnmounted, ref, watch } from 'vue'
import { useApi } from '../../composables/useApi'
import { api } from '../../services/api'
import { formatDateTime, formatNumber } from '../../utils/format'
import AsyncState from '../ui/AsyncState.vue'
import Pagination from '../ui/Pagination.vue'

const props = defineProps({ program: { type: Object, required: true } })

const query = ref('')
const providerFilter = ref('')
const page = ref(1)
const { data, error, loading, load } = useApi(() => api.subdomains({
  source: props.program.source,
  program: props.program.slug,
  q: query.value.trim(),
  provider: providerFilter.value,
  page: page.value,
}))
const rows = computed(() => data.value?.data ?? [])
const meta = computed(() => data.value?.meta ?? {})
const { data: refreshedProgram, loading: loadingRun, error: runError, load: loadRun } = useApi(
  () => api.program(props.program.id), { immediate: false },
)
const run = computed(() => refreshedProgram.value ? refreshedProgram.value.data?.discovery : props.program.discovery)
const labels = { complete: 'Complete', partial: 'Partial', failed: 'Failed', no_scope: 'No eligible wildcard roots', blocked_scope: 'Blocked by scope rules' }
const statusLabel = computed(() => labels[run.value?.status] ?? 'Unknown')
const statusClass = computed(() => ({
  complete: 'border-emerald-400/30 text-emerald-200',
  partial: 'border-yellow-400/30 text-yellow-200',
  blocked_scope: 'border-yellow-400/30 text-yellow-200',
  failed: 'border-red-400/30 text-red-200',
}[run.value?.status] ?? 'border-white/10 text-gray-300'))

function providerLabel(source) {
  const names = {
    crtsh: 'crt.sh', subfinder: 'Subfinder', commoncrawl: 'Common Crawl', securitytrails: 'SecurityTrails',
    dnsdb: 'Farsight DNSDB', urlscan: 'urlscan.io', chaos: 'Chaos', certspotter: 'Cert Spotter', virustotal: 'VirusTotal',
  }
  return Object.hasOwn(names, source) ? names[source] : source
}

let debounce
watch(query, () => {
  clearTimeout(debounce)
  debounce = setTimeout(() => go(1), 250)
})
onUnmounted(() => clearTimeout(debounce))

function go(next) {
  clearTimeout(debounce)
  page.value = next
  load()
}

function refresh() {
  go(1)
  loadRun()
}

function setProvider(provider) {
  if (providerFilter.value === provider) return
  providerFilter.value = provider
  go(1)
}
</script>
