<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="max-w-7xl mx-auto">
      <PageHeader
        badge="SOURCES"
        title="Applications"
        subtitle="Where the monitored data comes from and how fresh it is"
      />

      <AsyncState :loading="loading" :error="error" @retry="load">
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <article
            v-for="source in sources"
            :key="source.source"
            class="bg-gray-900/40 border border-gray-800 rounded-xl p-6 hover:border-cyan-500/30 transition-colors"
          >
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center font-mono text-cyan-400 text-sm">
                  {{ initials(source.source) }}
                </div>
                <div>
                  <h3 class="text-base font-semibold text-white">{{ sourceLabel(source.source) }}</h3>
                  <p class="text-[11px] font-mono text-gray-600">{{ source.source }}</p>
                </div>
              </div>
              <span
                class="text-[10px] font-mono px-2 py-0.5 rounded border"
                :class="source.last_run ? 'border-green-500/30 text-green-400/80 bg-green-500/5' : 'border-gray-700 text-gray-500'"
              >
                {{ source.last_run ? 'SYNCED' : 'IDLE' }}
              </span>
            </div>

            <div class="grid grid-cols-3 gap-3 mb-5">
              <div>
                <div class="text-xl font-bold text-white tabular-nums">{{ formatNumber(source.active_programs) }}</div>
                <div class="text-[10px] font-mono text-gray-600">ACTIVE</div>
              </div>
              <div>
                <div class="text-xl font-bold text-white tabular-nums">{{ formatNumber(source.programs) }}</div>
                <div class="text-[10px] font-mono text-gray-600">TOTAL</div>
              </div>
              <div>
                <div class="text-xl font-bold tabular-nums" :class="source.changes_24h ? 'text-cyan-400' : 'text-gray-500'">
                  {{ formatNumber(source.changes_24h) }}
                </div>
                <div class="text-[10px] font-mono text-gray-600">24H</div>
              </div>
            </div>

            <div class="pt-4 border-t border-gray-800/70 text-[11px] font-mono text-gray-600 flex items-center justify-between">
              <span>{{ source.last_run ? timeAgo(source.last_run.started_at) : 'never synced' }}</span>
              <RouterLink to="/targets" class="text-cyan-400/60 hover:text-cyan-400">browse →</RouterLink>
            </div>
          </article>
        </div>

        <div class="mt-8 bg-gray-900/30 border border-gray-800 rounded-xl p-6">
          <h2 class="text-sm font-semibold tracking-wide text-gray-300 mb-2">HOW SOURCES WORK</h2>
          <p class="text-sm text-gray-500 leading-relaxed">
            The Python collector downloads the public datasets published by
            <span class="text-gray-300">arkadiyt/bounty-targets-data</span> — Bugcrowd, HackerOne, YesWeHack and Intigriti —
            normalises them into a single schema and stores them in MongoDB. The
            <span class="text-gray-300"> local</span> source contains programs you maintain yourself
            (either through the API or as JSON files in the collector's <code class="text-cyan-400/80">programs/</code> directory).
          </p>
        </div>
      </AsyncState>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '../../services/api'
import { useApi } from '../../composables/useApi'
import { formatNumber, sourceLabel, timeAgo } from '../../utils/format'
import PageHeader from '../ui/PageHeader.vue'
import AsyncState from '../ui/AsyncState.vue'

const { data, error, loading, load } = useApi(() => api.sources())
const sources = computed(() => data.value?.data || [])

function initials(source) {
  return (source || '?').slice(0, 2).toUpperCase()
}
</script>
