<template>
  <div v-if="loading" class="flex items-center justify-center gap-3 py-16 text-gray-500">
    <span class="w-4 h-4 border-2 border-cyan-500/30 border-t-cyan-400 rounded-full animate-spin"></span>
    <span class="text-sm font-mono tracking-wider">LOADING…</span>
  </div>

  <div
    v-else-if="error"
    class="border border-red-500/30 bg-red-500/5 rounded-xl p-6 text-center"
  >
    <p class="text-red-400 text-sm font-medium mb-1">Could not load data</p>
    <p class="text-red-400/70 text-xs font-mono mb-4">{{ error }}</p>
    <button
      class="px-4 py-2 text-xs uppercase tracking-wider border border-red-500/40 text-red-300 rounded-lg hover:bg-red-500/10 transition-colors"
      @click="$emit('retry')"
    >
      Retry
    </button>
  </div>

  <div
    v-else-if="empty"
    class="border border-gray-800 bg-gray-900/30 rounded-xl p-12 text-center"
  >
    <div class="w-12 h-12 mx-auto mb-4 rounded-full border border-cyan-500/20 bg-cyan-500/5 flex items-center justify-center">
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
