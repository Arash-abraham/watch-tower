<template>
  <header class="mb-10">
    <div class="mb-6 flex items-center gap-3">
      <span class="chip">
        <span class="relative flex h-1.5 w-1.5">
          <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-cyan-400 opacity-70"></span>
          <span class="relative inline-flex h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
        </span>
        {{ badge }}
      </span>
      <span class="hidden h-px flex-1 bg-gradient-to-r from-cyan-400/25 to-transparent sm:block"></span>
    </div>

    <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
      <div class="min-w-0">
        <h1 class="text-3xl font-bold tracking-tight text-white sm:text-4xl md:text-5xl">
          {{ title }}
        </h1>
        <p v-if="subtitle" class="mt-2 max-w-2xl text-sm text-gray-400">{{ subtitle }}</p>
      </div>

      <div class="flex shrink-0 flex-wrap items-center gap-2">
        <slot name="actions" />
      </div>
    </div>

    <div class="mt-6 divider"></div>
  </header>
</template>

<script setup>
defineProps({
  badge: { type: String, required: true },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>
