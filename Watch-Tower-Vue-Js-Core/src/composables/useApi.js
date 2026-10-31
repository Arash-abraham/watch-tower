import { onMounted, onUnmounted, ref } from 'vue'
import { ApiError } from '../services/api'

/**
 * Small fetch wrapper with loading/error state and optional polling.
 *
 * @param {() => Promise<any>} loader
 * @param {{ immediate?: boolean, refreshInterval?: number }} options
 */
export function useApi(loader, options = {}) {
  const { immediate = true, refreshInterval = 0 } = options

  const data = ref(null)
  const error = ref(null)
  const loading = ref(false)
  const lastUpdated = ref(null)

  let timer = null
  let requestId = 0

  async function load() {
    const current = ++requestId
    loading.value = true
    error.value = null

    try {
      const result = await loader()
      if (current !== requestId) return
      data.value = result
      lastUpdated.value = new Date()
    } catch (exception) {
      if (current !== requestId) return
      error.value =
        exception instanceof ApiError
          ? exception.message
          : exception?.message || 'Unexpected error while loading data'
    } finally {
      if (current === requestId) loading.value = false
    }
  }

  function startPolling() {
    stopPolling()
    if (!refreshInterval) return
    timer = setInterval(load, refreshInterval)
  }

  function stopPolling() {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  if (immediate) onMounted(load)
  if (refreshInterval) {
    onMounted(startPolling)
    onUnmounted(stopPolling)
  }

  return { data, error, loading, lastUpdated, load, stopPolling }
}
