<template>
  <div class="pt-24 pb-16 text-white">
    <div class="container-page">
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
            class="panel panel-hover p-6"
          >
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center gap-3">
                <div class="tile font-mono text-[13px]">
                  {{ initials(source.source) }}
                </div>
                <div>
                  <h3 class="text-base font-semibold text-white">{{ sourceLabel(source.source) }}</h3>
                  <p class="text-[11px] font-mono text-gray-600">{{ source.source }}</p>
                </div>
              </div>
              <span
                class="rounded border px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider"
                :class="source.last_run ? 'border-emerald-400/25 bg-emerald-400/[0.06] text-emerald-300/80' : 'border-white/10 text-gray-500'"
              >
                {{ source.last_run ? 'SYNCED' : 'IDLE' }}
              </span>
            </div>

            <div class="grid grid-cols-3 gap-3 mb-5">
              <div>
                <div class="text-2xl font-bold tracking-tight text-white tabular-nums">{{ formatNumber(source.active_programs) }}</div>
                <div class="text-[10px] font-mono text-gray-600">ACTIVE</div>
              </div>
              <div>
                <div class="text-2xl font-bold tracking-tight text-white tabular-nums">{{ formatNumber(source.programs) }}</div>
                <div class="text-[10px] font-mono text-gray-600">TOTAL</div>
              </div>
              <div>
                <div class="text-2xl font-bold tracking-tight tabular-nums" :class="source.changes_24h ? 'text-cyan-300' : 'text-gray-600'">
                  {{ formatNumber(source.changes_24h) }}
                </div>
                <div class="text-[10px] font-mono text-gray-600">24H</div>
              </div>
            </div>

            <div class="flex items-center justify-between border-t border-white/[0.06] pt-4 font-mono text-[11px] text-gray-600">
              <span>{{ source.last_run ? timeAgo(source.last_run.started_at) : 'never synced' }}</span>
              <RouterLink to="/targets" class="text-cyan-300/70 transition-colors hover:text-cyan-300">browse →</RouterLink>
            </div>
          </article>
        </div>

        <div class="panel p-6">
          <h2 class="panel-title mb-2">How sources work</h2>
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
