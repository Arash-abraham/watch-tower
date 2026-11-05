<template>
  <div class="pt-24 pb-16 text-white">
    <div class="container-page">
      <PageHeader
        badge="PROGRAM DOSSIER"
        :title="program ? program.name : 'Program'"
        :subtitle="program
          ? `Complete scope inventory for ${program.name} — every asset listed in full, nothing truncated.`
          : 'Complete scope inventory for this program'"
      >
        <template #actions>
          <RouterLink to="/targets" class="btn-ghost text-xs">← all programs</RouterLink>
          <a
            v-if="program?.url"
            :href="program.url"
            target="_blank"
            rel="noopener noreferrer"
            class="btn-primary text-xs"
          >
            open program page ↗
          </a>
        </template>
      </PageHeader>

      <AsyncState :loading="loading" :error="error" @retry="load">
        <template v-if="program">
          <!-- status strip -->
          <div class="mb-6 flex flex-wrap items-center gap-2">
            <span class="chip">{{ sourceLabel(program.source) }}</span>
            <span
              class="inline-flex items-center gap-2 rounded-full border px-3 py-1 font-mono text-[10px] uppercase tracking-[0.18em]"
              :class="program.active
                ? 'border-emerald-400/25 bg-emerald-400/[0.06] text-emerald-300/80'
                : 'border-white/10 text-gray-500'"
            >
              <span class="h-1.5 w-1.5 rounded-full" :class="program.active ? 'bg-emerald-400' : 'bg-gray-600'"></span>
              {{ program.active ? 'active' : 'closed' }}
            </span>
            <span v-if="program.meta?.offers_bounties" class="chip">bounty program</span>
            <span
              v-if="program.conflicts?.length"
              class="inline-flex items-center gap-2 rounded-full border border-yellow-400/25 bg-yellow-400/[0.06] px-3 py-1 font-mono text-[10px] uppercase tracking-[0.18em] text-yellow-300/80"
            >
              {{ program.conflicts.length }} conflict(s)
            </span>
            <span class="ml-auto font-mono text-[11px] text-gray-600">
              synced {{ program.last_synced_at ? timeAgo(program.last_synced_at) : 'never' }}
            </span>
          </div>

          <!-- counters -->
          <div class="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
            <StatCard label="In-scope assets" :value="program.scopes.length" accent="cyan" hint="listed in full below" />
            <StatCard label="Out-of-scope assets" :value="program.out_of_scope.length" accent="yellow" hint="listed in full below" />
            <StatCard label="Max payout" :value="payout || '—'" accent="green" :hint="program.meta?.offers_bounties ? 'bounties offered' : 'no bounty info'" />
            <StatCard label="First seen" :value="firstSeen" accent="blue" hint="in Watch Tower" />
          </div>

          <!-- overview -->
          <section class="panel mb-6 p-6">
            <h2 class="panel-title mb-4">OVERVIEW</h2>
            <dl class="grid grid-cols-1 gap-x-10 gap-y-3 text-sm md:grid-cols-2">
              <div v-if="program.url" class="md:col-span-2">
                <dt class="mb-1 font-mono text-[10px] uppercase tracking-wider text-gray-600">Program URL</dt>
                <dd>
                  <a
                    :href="program.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="font-mono text-[13px] text-cyan-300/90 break-all transition-colors hover:text-cyan-300"
                  >{{ program.url }}</a>
                </dd>
              </div>
              <div>
                <dt class="mb-1 font-mono text-[10px] uppercase tracking-wider text-gray-600">Slug</dt>
                <dd class="font-mono text-[13px] text-gray-300 break-all">{{ program.slug }}</dd>
              </div>
              <div>
                <dt class="mb-1 font-mono text-[10px] uppercase tracking-wider text-gray-600">Source</dt>
                <dd class="text-gray-300">{{ sourceLabel(program.source) }}</dd>
              </div>
              <div>
                <dt class="mb-1 font-mono text-[10px] uppercase tracking-wider text-gray-600">First seen</dt>
                <dd class="text-gray-300">{{ formatDateTime(program.first_seen_at) }}</dd>
              </div>
              <div>
                <dt class="mb-1 font-mono text-[10px] uppercase tracking-wider text-gray-600">Last synced</dt>
                <dd class="text-gray-300">{{ formatDateTime(program.last_synced_at) }}</dd>
              </div>
            </dl>
          </section>

          <!-- conflicts -->
          <section v-if="program.conflicts?.length" class="mb-6 rounded-2xl border border-yellow-400/25 bg-yellow-400/[0.04] p-6">
            <h2 class="mb-2 flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.18em] text-yellow-300/90">
              ⚠ SCOPE CONFLICTS
            </h2>
            <p class="mb-3 text-xs text-yellow-200/60">
              These targets appear in both the in-scope and out-of-scope lists. Verify with the program before testing.
            </p>
            <ul class="space-y-1.5">
              <li v-for="target in program.conflicts" :key="target" class="font-mono text-xs text-yellow-200/90 break-all">
                › {{ target }}
              </li>
            </ul>
          </section>

          <!-- ══════════ IN SCOPE — full paginated list ══════════ -->
          <section id="in-scope" ref="inScopeEl" class="panel mb-6 scroll-mt-24 overflow-hidden">
            <div class="panel-head flex-wrap">
              <h2 class="panel-title">IN SCOPE · {{ formatNumber(inScope.filtered.length) }} asset(s)</h2>
              <span class="font-mono text-[10px] text-gray-600">full identifiers · no truncation</span>
            </div>

            <div class="flex flex-col gap-3 border-b border-white/[0.06] p-4 sm:flex-row sm:items-center">
              <input
                v-model="inScope.q"
                type="text"
                placeholder="Filter in-scope assets…"
                class="field flex-1 font-mono text-xs"
              />
              <label class="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-gray-600">
                per page
                <select v-model.number="inScope.perPage" class="field w-auto cursor-pointer py-1.5 text-xs">
                  <option :value="10">10</option>
                  <option :value="25">25</option>
                  <option :value="50">50</option>
                  <option :value="100">100</option>
                </select>
              </label>
            </div>

            <p v-if="!inScope.filtered.length" class="p-8 text-center text-sm text-gray-600">
              {{ inScope.q ? 'No in-scope asset matches this filter.' : 'No in-scope assets.' }}
            </p>
            <ol v-else class="divide-y divide-white/[0.05]">
              <li v-for="(asset, index) in inScope.paged" :key="asset.target" class="row-hover px-5 py-3">
                <div class="flex items-start gap-3">
                  <span class="mt-0.5 w-9 shrink-0 text-right font-mono text-[10px] tabular-nums text-gray-700">
                    {{ inScope.start + index + 1 }}
                  </span>
                  <div class="min-w-0 flex-1">
                    <div class="flex flex-wrap items-center gap-x-2 gap-y-1">
                      <span class="font-mono text-[13px] text-gray-200 break-all">{{ asset.target }}</span>
                      <span v-if="asset.type" class="rounded border border-cyan-400/20 bg-cyan-400/[0.06] px-1.5 py-px font-mono text-[9px] uppercase tracking-wider text-cyan-300/70">
                        {{ asset.type }}
                      </span>
                    </div>
                    <div v-if="asset.chips.length" class="mt-1.5 flex flex-wrap gap-1.5">
                      <span v-for="chip in asset.chips" :key="chip" class="rounded border border-white/[0.08] bg-white/[0.02] px-1.5 py-px font-mono text-[10px] text-gray-500 break-all">
                        {{ chip }}
                      </span>
                    </div>
                    <p v-for="note in asset.notes" :key="note.key" class="mt-1.5 text-xs leading-relaxed text-gray-500 break-words">
                      <span class="font-mono text-gray-600">{{ note.key }}:</span> {{ note.value }}
                    </p>
                  </div>
                  <a
                    v-if="asset.href"
                    :href="asset.href"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="shrink-0 font-mono text-xs text-gray-600 transition-colors hover:text-cyan-300"
                    aria-label="Open asset in a new tab"
                  >↗</a>
                </div>
              </li>
            </ol>

            <div class="px-5 pb-5">
              <Pagination
                :page="inScope.page"
                :last-page="inScope.lastPage"
                :total="inScope.filtered.length"
                @update:page="(value) => goPage(inScope, value, inScopeEl)"
              />
            </div>
          </section>

          <!-- ══════════ OUT OF SCOPE — full paginated list ══════════ -->
          <section id="out-of-scope" ref="outScopeEl" class="panel mb-6 scroll-mt-24 overflow-hidden">
            <div class="panel-head flex-wrap">
              <h2 class="panel-title">OUT OF SCOPE · {{ formatNumber(outScope.filtered.length) }} asset(s)</h2>
              <span class="font-mono text-[10px] text-gray-600">always visible · no dropdown</span>
            </div>

            <div class="flex flex-col gap-3 border-b border-white/[0.06] p-4 sm:flex-row sm:items-center">
              <input
                v-model="outScope.q"
                type="text"
                placeholder="Filter out-of-scope assets…"
                class="field flex-1 font-mono text-xs"
              />
              <label class="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-gray-600">
                per page
                <select v-model.number="outScope.perPage" class="field w-auto cursor-pointer py-1.5 text-xs">
                  <option :value="10">10</option>
                  <option :value="25">25</option>
                  <option :value="50">50</option>
                  <option :value="100">100</option>
                </select>
              </label>
            </div>

            <p v-if="!outScope.filtered.length" class="p-8 text-center text-sm text-gray-600">
              {{ outScope.q ? 'No out-of-scope asset matches this filter.' : 'No out-of-scope assets.' }}
            </p>
            <ol v-else class="divide-y divide-white/[0.05]">
              <li v-for="(asset, index) in outScope.paged" :key="asset.target" class="row-hover px-5 py-3">
                <div class="flex items-start gap-3">
                  <span class="mt-0.5 w-9 shrink-0 text-right font-mono text-[10px] tabular-nums text-gray-700">
                    {{ outScope.start + index + 1 }}
                  </span>
                  <div class="min-w-0 flex-1">
                    <div class="flex flex-wrap items-center gap-x-2 gap-y-1">
                      <span class="font-mono text-[13px] text-gray-400 break-all">{{ asset.target }}</span>
                      <span v-if="asset.type" class="rounded border border-white/10 px-1.5 py-px font-mono text-[9px] uppercase tracking-wider text-gray-500">
                        {{ asset.type }}
                      </span>
                    </div>
                    <div v-if="asset.chips.length" class="mt-1.5 flex flex-wrap gap-1.5">
                      <span v-for="chip in asset.chips" :key="chip" class="rounded border border-white/[0.08] bg-white/[0.02] px-1.5 py-px font-mono text-[10px] text-gray-500 break-all">
                        {{ chip }}
                      </span>
                    </div>
                    <p v-for="note in asset.notes" :key="note.key" class="mt-1.5 text-xs leading-relaxed text-gray-500 break-words">
                      <span class="font-mono text-gray-600">{{ note.key }}:</span> {{ note.value }}
                    </p>
                  </div>
                  <a
                    v-if="asset.href"
                    :href="asset.href"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="shrink-0 font-mono text-xs text-gray-600 transition-colors hover:text-cyan-300"
                    aria-label="Open asset in a new tab"
                  >↗</a>
                </div>
              </li>
            </ol>

            <div class="px-5 pb-5">
              <Pagination
                :page="outScope.page"
                :last-page="outScope.lastPage"
                :total="outScope.filtered.length"
                @update:page="(value) => goPage(outScope, value, outScopeEl)"
              />
            </div>
          </section>

          <!-- program metadata -->
          <section v-if="metaEntries.length" class="panel p-6">
            <h2 class="panel-title mb-4">PROGRAM METADATA</h2>
            <dl class="grid grid-cols-1 gap-x-10 gap-y-3 text-sm md:grid-cols-2">
              <div v-for="entry in metaEntries" :key="entry.key">
                <dt class="mb-1 font-mono text-[10px] uppercase tracking-wider text-gray-600">{{ entry.key }}</dt>
                <dd class="text-[13px] text-gray-300 break-words">{{ entry.value }}</dd>
              </div>
            </dl>
          </section>
        </template>
      </AsyncState>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onUnmounted, reactive, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { api } from '../../services/api'
import { useApi } from '../../composables/useApi'
import { formatDateTime, formatMoney, formatNumber, sourceLabel, timeAgo } from '../../utils/format'
import PageHeader from '../ui/PageHeader.vue'
import AsyncState from '../ui/AsyncState.vue'
import Pagination from '../ui/Pagination.vue'
import StatCard from '../ui/StatCard.vue'

const route = useRoute()

const { data, error, loading, load } = useApi(() => api.program(route.params.id))
const program = computed(() => data.value?.data || null)

const payout = computed(() =>
  program.value ? formatMoney(program.value.meta?.max_payout ?? program.value.meta?.max_bounty, program.value.meta?.currency) : null,
)

const firstSeen = computed(() => {
  if (!program.value?.first_seen_at) return '—'
  return new Date(program.value.first_seen_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: '2-digit' })
})

const metaEntries = computed(() =>
  Object.entries(program.value?.meta || {})
    .filter(([, value]) => value !== null && value !== undefined && value !== '')
    .map(([key, value]) => ({ key, value: formatValue(value) })),
)

/* ── asset lists ────────────────────────────────────────────────
 * Prefer scope_details (rich objects); fall back to the plain
 * identifier arrays. Every asset is rendered in full — long URLs
 * wrap instead of being cut off with an ellipsis.
 */
function normalizeAssets(details, plain) {
  const source = Array.isArray(details) && details.length ? details : plain || []

  return source.map((item) => {
    const raw = typeof item === 'string' ? { target: item } : item || {}
    const target = String(raw.target ?? '')
    const type = raw.type && raw.type !== 'unknown' ? String(raw.type) : ''
    const chips = []
    const notes = []

    for (const [key, value] of Object.entries(raw)) {
      if (key === 'target' || key === 'type') continue
      if (value === null || value === undefined || value === '') continue
      const text = formatValue(value)
      if (text.length > 90) notes.push({ key, value: text })
      else chips.push(`${key}: ${text}`)
    }

    return {
      target,
      type,
      chips,
      notes,
      href: /^https?:\/\//i.test(target) ? target : null,
    }
  })
}

function formatValue(value) {
  if (typeof value === 'boolean') return value ? 'yes' : 'no'
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

const inScopeAssets = computed(() =>
  normalizeAssets(program.value?.scope_details?.in, program.value?.scopes),
)
const outScopeAssets = computed(() =>
  normalizeAssets(program.value?.scope_details?.out, program.value?.out_of_scope),
)

/* Client-side pagination so huge scopes stay readable and nothing
 * is ever hidden: every asset is reachable page by page. */
function useAssetSection(assets) {
  const section = reactive({
    q: '',
    page: 1,
    perPage: 25,
    filtered: computed(() => {
      const needle = section.q.trim().toLowerCase()
      if (!needle) return assets.value
      return assets.value.filter((asset) =>
        asset.target.toLowerCase().includes(needle) ||
        asset.type.toLowerCase().includes(needle) ||
        asset.chips.some((chip) => chip.toLowerCase().includes(needle)) ||
        asset.notes.some((note) => `${note.key} ${note.value}`.toLowerCase().includes(needle)),
      )
    }),
    lastPage: computed(() => Math.max(1, Math.ceil(section.filtered.length / section.perPage))),
    start: computed(() => (section.page - 1) * section.perPage),
    paged: computed(() => section.filtered.slice(section.start, section.start + section.perPage)),
  })

  watch(() => [section.q, section.perPage], () => { section.page = 1 })
  watch(() => section.lastPage, (last) => { if (section.page > last) section.page = last })

  return section
}

const inScope = useAssetSection(inScopeAssets)
const outScope = useAssetSection(outScopeAssets)

const inScopeEl = ref(null)
const outScopeEl = ref(null)

function goPage(section, value, element) {
  section.page = value
  nextTick(() => element?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
}

/* Deep links like /programs/:id#out-of-scope land on the right
 * section once the data has rendered. */
watch(loading, async (isLoading) => {
  if (isLoading || !program.value || !route.hash) return
  await nextTick()
  document.querySelector(route.hash)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
})

/* Reload when navigating between two program detail pages. */
watch(() => route.params.id, (id) => { if (id && route.name === 'program-detail') load() })

/* Meaningful tab title — handy when the page opens in a new tab. */
const originalTitle = document.title
watch(program, (value) => {
  document.title = value ? `${value.name} · Watch Tower` : originalTitle
})
onUnmounted(() => { document.title = originalTitle })
</script>
