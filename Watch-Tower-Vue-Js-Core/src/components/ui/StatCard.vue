<template>
  <div class="panel panel-hover group overflow-hidden p-5">
    <!-- accent wash -->
    <div
      class="pointer-events-none absolute -right-8 -top-10 h-24 w-24 rounded-full opacity-0 blur-2xl transition-opacity duration-500 group-hover:opacity-100"
      :class="glowClass"
    ></div>
    <div class="pointer-events-none absolute inset-x-0 top-0 h-px" :class="topLineClass"></div>

    <div class="relative flex items-start justify-between gap-3">
      <span class="font-mono text-[10px] uppercase leading-tight tracking-[0.14em] text-gray-500">{{ label }}</span>
      <span class="relative mt-1 flex h-1.5 w-1.5 shrink-0">
        <span class="absolute inline-flex h-full w-full rounded-full opacity-60" :class="[dotClass, 'animate-ping']"></span>
        <span class="relative inline-flex h-1.5 w-1.5 rounded-full" :class="dotClass"></span>
      </span>
    </div>

    <div class="relative mt-3 flex items-end gap-2">
      <span class="kpi">{{ displayValue }}</span>
    </div>

    <div class="relative mt-1 text-[11px] leading-snug" :class="hintClass">
      <slot name="hint">{{ hint }}</slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatNumber } from '../../utils/format'

const props = defineProps({
  label: { type: String, required: true },
  value: { type: [Number, String], default: null },
  hint: { type: String, default: '' },
  accent: { type: String, default: 'cyan' }, // cyan | green | red | yellow | blue
  loading: { type: Boolean, default: false },
})

const displayValue = computed(() => {
  if (props.loading) return '···'
  if (props.value === null || props.value === undefined) return '—'
  return typeof props.value === 'number' ? formatNumber(props.value) : props.value
})

const accents = {
  cyan: { dot: 'bg-cyan-400', hint: 'text-gray-600', glow: 'bg-cyan-400/20', line: 'bg-gradient-to-r from-cyan-400/70 to-transparent' },
  green: { dot: 'bg-emerald-400', hint: 'text-emerald-400/80', glow: 'bg-emerald-400/20', line: 'bg-gradient-to-r from-emerald-400/70 to-transparent' },
  red: { dot: 'bg-red-400', hint: 'text-red-400/80', glow: 'bg-red-400/20', line: 'bg-gradient-to-r from-red-400/70 to-transparent' },
  yellow: { dot: 'bg-amber-400', hint: 'text-amber-400/80', glow: 'bg-amber-400/20', line: 'bg-gradient-to-r from-amber-400/70 to-transparent' },
  blue: { dot: 'bg-blue-400', hint: 'text-gray-600', glow: 'bg-blue-400/20', line: 'bg-gradient-to-r from-blue-400/70 to-transparent' },
}

const current = computed(() => accents[props.accent] || accents.cyan)
const dotClass = computed(() => current.value.dot)
const hintClass = computed(() => current.value.hint)
const glowClass = computed(() => current.value.glow)
const topLineClass = computed(() => current.value.line)
</script>

<style scoped>
.kpi {
  font-variant-numeric: tabular-nums;
}
</style>
