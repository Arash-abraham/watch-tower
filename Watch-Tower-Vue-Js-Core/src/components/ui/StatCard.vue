<template>
  <div
    class="group relative overflow-hidden rounded-2xl border border-white/[0.07] bg-white/[0.02] p-5 backdrop-blur-sm transition-all duration-300 hover:bg-white/[0.035]"
    :class="borderClass"
  >
    <div class="flex items-center justify-between mb-2">
      <span class="text-[11px] font-mono uppercase tracking-[0.14em] text-gray-500">{{ label }}</span>
      <span class="h-1.5 w-1.5 rounded-full" :class="dotClass"></span>
    </div>
    <div class="mt-3 text-3xl font-bold text-white tabular-nums">
      {{ displayValue }}
    </div>
    <div class="mt-1 text-[11px] leading-snug" :class="hintClass">
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
  cyan: { border: 'hover:border-cyan-400/30', dot: 'bg-cyan-400', hint: 'text-gray-600' },
  green: { border: 'hover:border-emerald-400/30', dot: 'bg-emerald-400', hint: 'text-emerald-400/80' },
  red: { border: 'hover:border-red-400/30', dot: 'bg-red-400', hint: 'text-red-400/80' },
  yellow: { border: 'hover:border-amber-400/30', dot: 'bg-amber-400', hint: 'text-amber-400/80' },
  blue: { border: 'hover:border-blue-400/30', dot: 'bg-blue-400', hint: 'text-gray-600' },
}

const borderClass = computed(() => (accents[props.accent] || accents.cyan).border)
const dotClass = computed(() => (accents[props.accent] || accents.cyan).dot)
const hintClass = computed(() => (accents[props.accent] || accents.cyan).hint)
</script>
