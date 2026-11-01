<template>
  <div class="mb-10">
    <div class="mb-8">
      <div class="inline-flex items-center gap-3 px-4 py-2 border border-cyan-500/20 bg-cyan-500/5 backdrop-blur-sm rounded-full">
        <span class="relative flex h-2 w-2">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
        </span>
        <span class="text-cyan-400/70 text-[10px] tracking-[0.2em] font-mono">{{ badge }}</span>
      </div>
    </div>

    <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-2">
      <span class="text-white">{{ title }}</span>
    </h1>

    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
      <p class="text-gray-500 text-sm">{{ subtitle }}</p>
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  badge: { type: String, required: true },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>
