<template>
  <div class="pt-24 pb-16 text-white">
    <div class="container-narrow">
      <PageHeader
        badge="SETTINGS"
        title="Settings"
        subtitle="Runtime configuration of this dashboard"
      />

      <div class="space-y-6">
        <!-- connection -->
        <section class="bg-gray-900/40 border border-gray-800 rounded-xl overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-800 flex items-center justify-between">
            <h2 class="text-sm font-semibold tracking-wide text-gray-300">API CONNECTION</h2>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded border" :class="health.ok ? 'border-green-500/30 text-green-400/80 bg-green-500/5' : 'border-red-500/30 text-red-400/80 bg-red-500/5'">
              {{ health.ok ? 'ONLINE' : 'OFFLINE' }}
            </span>
          </div>
          <div class="p-6 space-y-4 text-sm">
            <div class="flex items-center justify-between gap-4">
              <span class="text-gray-500">Base URL</span>
              <code class="text-cyan-400/90 font-mono text-xs">{{ api.baseUrl }}</code>
            </div>
            <div class="flex items-center justify-between gap-4">
              <span class="text-gray-500">Service</span>
              <span class="text-gray-300 text-xs font-mono">{{ health.service || '—' }} · v{{ health.version || '—' }}</span>
            </div>
            <div class="flex items-center justify-between gap-4">
              <span class="text-gray-500">MongoDB</span>
              <span class="text-xs font-mono" :class="health.mongo ? 'text-green-400' : 'text-red-400'">
                {{ health.mongo ? 'connected' : health.error || 'unavailable' }}
              </span>
            </div>
            <button
              class="mt-2 px-4 py-2 text-[11px] font-mono uppercase tracking-wider border border-cyan-500/40 text-cyan-400 rounded-lg hover:bg-cyan-500/10 transition-colors"
              @click="check"
            >
              test connection
            </button>
          </div>
        </section>

        <!-- notifications -->
        <section class="bg-gray-900/40 border border-gray-800 rounded-xl overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-800">
            <h2 class="text-sm font-semibold tracking-wide text-gray-300">NOTIFICATION CHANNELS</h2>
          </div>
          <div class="divide-y divide-gray-800/70">
            <div v-for="channel in channels" :key="channel.key" class="px-6 py-4 flex items-center justify-between">
              <div>
                <div class="text-sm text-white">{{ channel.label }}</div>
                <div class="text-[11px] font-mono text-gray-600">{{ channel.env }}</div>
              </div>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded border" :class="channel.enabled ? 'border-green-500/30 text-green-400/80 bg-green-500/5' : 'border-gray-700 text-gray-500'">
                {{ channel.enabled ? 'ENABLED' : 'DISABLED' }}
              </span>
            </div>
          </div>
          <div class="px-6 py-4 border-t border-gray-800/70">
            <p class="text-[11px] text-gray-600">
              Channels are configured in the collector's environment
              (<code class="text-gray-400">Watch-Tower-Python-Core/.env</code>). The API only reports their state.
            </p>
          </div>
        </section>

        <!-- env -->
        <section class="bg-gray-900/40 border border-gray-800 rounded-xl overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-800">
            <h2 class="text-sm font-semibold tracking-wide text-gray-300">FRONTEND ENVIRONMENT</h2>
          </div>
          <div class="p-6 space-y-3 text-sm">
            <div class="flex items-center justify-between gap-4">
              <span class="text-gray-500">Refresh interval</span>
              <span class="text-gray-300 text-xs font-mono">60s (dashboard polling)</span>
            </div>
            <div class="flex items-center justify-between gap-4">
              <span class="text-gray-500">API base override</span>
              <code class="text-gray-400 font-mono text-xs">VITE_API_BASE_URL</code>
            </div>
            <div class="flex items-center justify-between gap-4">
              <span class="text-gray-500">Dev proxy target</span>
              <code class="text-gray-400 font-mono text-xs">VITE_PROXY_TARGET</code>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from '../../services/api'
import PageHeader from '../ui/PageHeader.vue'

const health = ref({ ok: false })
const stats = ref(null)

const channels = computed(() => {
  const notifications = stats.value?.notifications || {}
  return [
    { key: 'telegram', label: 'Telegram', env: 'TELEGRAM_BOT_TOKEN · TELEGRAM_CHAT_ID', enabled: Boolean(notifications.telegram) },
    { key: 'discord', label: 'Discord', env: 'DISCORD_WEBHOOK_URL', enabled: Boolean(notifications.discord) },
  ]
})

async function check() {
  health.value = await api.health().catch(() => ({ ok: false }))
}

onMounted(async () => {
  await check()
  const response = await api.stats().catch(() => null)
  stats.value = response?.data || null
})
</script>
