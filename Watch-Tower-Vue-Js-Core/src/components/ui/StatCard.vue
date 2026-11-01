<template>
  <div
    class="bg-gray-900/50 border rounded-xl p-6 transition-colors"
    :class="borderClass"
  >
    <div class="flex items-center justify-between mb-2">
      <span class="text-gray-500 text-sm font-medium">{{ label }}</span>
      <span class="w-2 h-2 rounded-full" :class="dotClass"></span>
    </div>
    <div class="text-3xl font-bold text-white tabular-nums">
      {{ displayValue }}
    </div>
    <div class="text-xs mt-1" :class="hintClass">
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
  cyan: { border: 'border-gray-800 hover:border-cyan-500/30', dot: 'bg-cyan-500', hint: 'text-gray-600' },
  green: { border: 'border-gray-800 hover:border-green-500/30', dot: 'bg-green-500', hint: 'text-green-500/80' },
  red: { border: 'border-gray-800 hover:border-red-500/30', dot: 'bg-red-500', hint: 'text-red-500/80' },
  yellow: { border: 'border-gray-800 hover:border-yellow-500/30', dot: 'bg-yellow-500', hint: 'text-yellow-500/80' },
  blue: { border: 'border-gray-800 hover:border-blue-500/30', dot: 'bg-blue-500', hint: 'text-gray-600' },
}

const borderClass = computed(() => (accents[props.accent] || accents.cyan).border)
const dotClass = computed(() => (accents[props.accent] || accents.cyan).dot)
const hintClass = computed(() => (accents[props.accent] || accents.cyan).hint)
</script>
