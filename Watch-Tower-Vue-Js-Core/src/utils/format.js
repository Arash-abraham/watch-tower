const dateFormatter = new Intl.DateTimeFormat(undefined, {
  year: 'numeric',
  month: 'short',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
})

export function formatDateTime(value) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return dateFormatter.format(date)
}

export function timeAgo(value) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'

  const seconds = Math.round((date.getTime() - Date.now()) / 1000)
  const units = [
    { limit: 60, divisor: 1, unit: 'second' },
    { limit: 3600, divisor: 60, unit: 'minute' },
    { limit: 86400, divisor: 3600, unit: 'hour' },
    { limit: 604800, divisor: 86400, unit: 'day' },
    { limit: 2629800, divisor: 604800, unit: 'week' },
    { limit: Infinity, divisor: 2629800, unit: 'month' },
  ]

  const formatter = new Intl.RelativeTimeFormat(undefined, { numeric: 'auto' })

  for (const { limit, divisor, unit } of units) {
    if (Math.abs(seconds) < limit) {
      return formatter.format(Math.round(seconds / divisor), unit)
    }
  }

  return formatDateTime(value)
}

export function formatNumber(value) {
  if (value === null || value === undefined) return '—'
  return new Intl.NumberFormat().format(value)
}

export function formatMoney(value, currency) {
  if (value === null || value === undefined || value === 0) return null
  try {
    return new Intl.NumberFormat(undefined, {
      style: 'currency',
      currency: currency || 'USD',
      maximumFractionDigits: 0,
    }).format(value)
  } catch {
    return `${value}`
  }
}

export const SOURCE_LABELS = {
  bugcrowd: 'Bugcrowd',
  hackerone: 'HackerOne',
  yeswehack: 'YesWeHack',
  intigriti: 'Intigriti',
  local: 'Local',
}

export const CHANGE_LABELS = {
  program_added: 'New program',
  program_removed: 'Program closed',
  scope_added: 'Scope added',
  scope_removed: 'Scope removed',
  out_scope_added: 'Out-of-scope added',
  out_scope_removed: 'Out-of-scope removed',
  conflict: 'Conflict',
}

export function sourceLabel(source) {
  return SOURCE_LABELS[source] || source
}
