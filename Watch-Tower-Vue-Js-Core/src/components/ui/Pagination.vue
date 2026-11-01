<template>
  <nav
    v-if="lastPage > 1"
    class="mt-8 flex flex-col items-center justify-between gap-3 sm:flex-row"
    aria-label="Pagination"
  >
    <p class="font-mono text-[11px] text-gray-600">
      page <span class="text-gray-400">{{ page }}</span> of {{ lastPage }}
      <span v-if="total !== null"> · {{ total }} records</span>
    </p>

    <div class="flex items-center gap-1.5">
      <button
        class="grid h-8 w-8 place-items-center rounded-lg border border-white/10 text-gray-400 transition-colors hover:border-cyan-400/40 hover:text-cyan-300 disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-white/10 disabled:hover:text-gray-400"
        :disabled="page <= 1"
        aria-label="Previous page"
        @click="go(page - 1)"
      >
        <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <template v-for="(item, index) in pages" :key="`${item}-${index}`">
        <span v-if="item === '…'" class="px-1.5 font-mono text-xs text-gray-600">…</span>
        <button
          v-else
          class="h-8 min-w-8 rounded-lg border px-2 font-mono text-xs transition-colors"
          :class="
            item === page
              ? 'border-cyan-400/50 bg-cyan-400/10 text-cyan-300'
              : 'border-white/10 text-gray-400 hover:border-cyan-400/40 hover:text-cyan-300'
          "
          :aria-current="item === page ? 'page' : undefined"
          @click="go(item)"
        >
          {{ item }}
        </button>
      </template>

      <button
        class="grid h-8 w-8 place-items-center rounded-lg border border-white/10 text-gray-400 transition-colors hover:border-cyan-400/40 hover:text-cyan-300 disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-white/10 disabled:hover:text-gray-400"
        :disabled="page >= lastPage"
        aria-label="Next page"
        @click="go(page + 1)"
      >
        <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  page: { type: Number, default: 1 },
  lastPage: { type: Number, default: 1 },
  total: { type: Number, default: null },
})

const emit = defineEmits(['update:page'])

const pages = computed(() => {
  const last = Math.max(1, props.lastPage)
  const current = Math.min(Math.max(1, props.page), last)

  if (last <= 7) return Array.from({ length: last }, (_, index) => index + 1)

  const result = [1]
  const start = Math.max(2, current - 1)
  const end = Math.min(last - 1, current + 1)

  if (start > 2) result.push('…')
  for (let index = start; index <= end; index += 1) result.push(index)
  if (end < last - 1) result.push('…')
  result.push(last)

  return result
})

function go(target) {
  if (target < 1 || target > props.lastPage || target === props.page) return
  emit('update:page', target)
}
</script>
