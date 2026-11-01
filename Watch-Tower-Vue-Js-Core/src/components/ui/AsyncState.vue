<template>
  <div v-if="loading" class="flex items-center justify-center gap-3 py-16 text-gray-500">
    <span class="w-4 h-4 border-2 border-cyan-500/30 border-t-cyan-400 rounded-full animate-spin"></span>
    <span class="text-sm font-mono tracking-wider">LOADING…</span>
  </div>

  <div
    v-else-if="error"
    class="rounded-2xl border border-red-400/25 bg-red-500/5 p-8 text-center backdrop-blur-sm"
  >
    <p class="text-red-400 text-sm font-medium mb-1">Could not load data</p>
    <p class="text-red-400/70 text-xs font-mono mb-4">{{ error }}</p>
    <button
      class="rounded-lg border border-red-400/40 px-4 py-2 text-xs uppercase tracking-wider text-red-300 transition-colors hover:bg-red-500/10"
      @click="$emit('retry')"
    >
      Retry
    </button>
  </div>

  <div
    v-else-if="empty"
    class="rounded-2xl border border-white/[0.07] bg-white/[0.02] p-12 text-center backdrop-blur-sm"
  >
    <div class="mx-auto mb-4 grid h-12 w-12 place-items-center rounded-full border border-cyan-400/20 bg-cyan-400/5">
      <span class="w-2 h-2 rounded-full bg-cyan-500/60"></span>
    </div>
    <p class="text-gray-400 text-sm">{{ emptyText }}</p>
    <p v-if="emptyHint" class="text-gray-600 text-xs mt-2">{{ emptyHint }}</p>
  </div>

  <slot v-else />
</template>

<script setup>
defineProps({
  loading: { type: Boolean, default: false },
  error: { type: [String, null], default: null },
  empty: { type: Boolean, default: false },
  emptyText: { type: String, default: 'Nothing here yet.' },
  emptyHint: { type: String, default: '' },
})

defineEmits(['retry'])
</script>
