/**
 * Thin API client for the Watch Tower Laravel API.
 *
 * In development Vite proxies `/api` to Laravel (see vite.config.js), so the
 * default relative base works both behind nginx and behind the dev server.
 */

const BASE_URL = (import.meta.env.VITE_API_BASE_URL || '/api/v2.1').replace(/\/+$/, '')
const API_ROOT = BASE_URL.replace(/\/v2\.1$/, '')

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

function buildQuery(params = {}) {
  const search = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return
    search.append(key, value)
  })

  const query = search.toString()
  return query ? `?${query}` : ''
}

async function request(path, params) {
  const url = `${BASE_URL}${path}${buildQuery(params)}`

  let response
  try {
    response = await fetch(url, { headers: { Accept: 'application/json' } })
  } catch (error) {
    throw new ApiError('Cannot reach the API. Is the backend running?', 0)
  }

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`
    try {
      const body = await response.json()
      message = body.message || message
    } catch {
      /* the body was not JSON */
    }
    throw new ApiError(message, response.status)
  }

  return response.json()
}

export const api = {
  baseUrl: BASE_URL,

  programs: (params = {}) => request('/programs', params),
  program: (id) => request(`/programs/${encodeURIComponent(id)}`),
  changes: (params = {}) => request('/changes', params),
  changeCounts: () => request('/changes/count'),
  stats: () => request('/stats'),
  sources: () => request('/sources'),

  async health() {
    const response = await fetch(`${API_ROOT}/health`, { headers: { Accept: 'application/json' } })
    const body = await response.json().catch(() => ({}))
    return { ok: response.ok, status: response.status, ...body }
  },
}
