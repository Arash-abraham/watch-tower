<template>
  <header class="mb-9">
    <div class="mb-6 flex items-center gap-3">
      <span class="chip">
        <span class="relative flex h-1.5 w-1.5">
          <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-cyan-400 opacity-70"></span>
          <span class="relative inline-flex h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
        </span>
        {{ badge }}
      </span>
      <span class="hidden h-px flex-1 bg-gradient-to-r from-cyan-400/25 via-white/5 to-transparent sm:block"></span>
      <span class="hidden font-mono text-[10px] uppercase tracking-[0.16em] text-gray-700 sm:block">
        {{ stamp }}
      </span>
    </div>

    <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
      <div class="min-w-0">
        <h1 class="text-[2rem] font-extrabold leading-[1.1] tracking-tight text-white sm:text-4xl md:text-[2.75rem]">
          {{ title }}
        </h1>
        <p v-if="subtitle" class="mt-2 max-w-2xl text-[13px] leading-relaxed text-gray-400 sm:text-sm">{{ subtitle }}</p>
      </div>

      <div class="flex shrink-0 flex-wrap items-center gap-2">
        <slot name="actions" />
      </div>
    </div>

    <div class="mt-6 divider"></div>
  </header>
</template>

<script setup>
import { computed } from 'vue'

defineProps({
  badge: { type: String, required: true },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})

const stamp = computed(() =>
  new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase(),
)
</script>
