/**
 * DEV-ONLY demo API for working on the Vue frontend without the backend.
 *
 * The real API is the Laravel core (Watch-Tower-Laravel-Core). This script
 * mimics its documented endpoints (docs/API.md) with deterministic fake data
 * so `npm run dev` has something to talk to in environments where PHP/MongoDB
 * are not available (e.g. UI sandboxes). It is NEVER used in production:
 * Vite proxies /api to VITE_PROXY_TARGET (default http://127.0.0.1:8000), and
 * this script simply listens on that port when you start it manually:
 *
 *   npm run mock-api      # terminal 1  (demo data on :8000)
 *   npm run dev           # terminal 2  (Vite on :5173, proxies /api)
 *
 * No Laravel or Python code is touched by this file.
 */

import http from 'node:http'

const PORT = Number(process.env.MOCK_API_PORT || 8000)
const HOST = '0.0.0.0'
const API = '/api/v2.1'

/* ── deterministic PRNG so the dataset is stable between restarts ── */
function mulberry32(seed) {
  return function () {
    seed |= 0
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}
const rand = mulberry32(20261105)
const pick = (list) => list[Math.floor(rand() * list.length)]
const hexId = (n) => (BigInt('0x6712f0c1a1b2c3d4e5f60718') + BigInt(n)).toString(16).padStart(24, '0')

const NOW = Date.now()
const HOUR = 3600_000
const DAY = 24 * HOUR
const iso = (ms) => new Date(ms).toISOString()

/* ── dataset ─────────────────────────────────────────────────────── */
const NAMES = [
  'Tesla', 'Shopify', 'GitLab', 'Nextcloud', 'Automattic', 'Slack', 'Uber', 'Airbnb',
  'Dropbox', 'GitHub', 'Mozilla', 'Cloudflare', 'Discord', 'Spotify', 'Netflix', 'Adobe',
  'Intel', 'Sony', 'PlayStation', 'Nintendo', 'Valve', 'Steam', 'Epic Games', 'Riot Games',
  'Roblox', 'TikTok', 'ByteDance', 'Snapchat', 'Reddit', 'Pinterest', 'LinkedIn', 'Microsoft',
  'Google', 'Amazon', 'AWS', 'Oracle', 'SAP', 'Salesforce', 'Atlassian', 'Trello',
  'Bitbucket', 'Zoom', 'Twilio', 'Stripe', 'PayPal', 'Coinbase', 'Binance', 'Kraken',
]
const SOURCES = ['bugcrowd', 'hackerone', 'yeswehack', 'intigriti', 'local']
const SEVERITIES = ['critical', 'high', 'medium', 'low']
const PAYOUTS = [500, 1000, 2500, 5000, 10000, 15000, 25000, 50000, 100000]
const CHANGE_TYPES = [
  'program_added', 'program_removed', 'scope_added', 'scope_removed',
  'out_scope_added', 'out_scope_removed', 'conflict',
]

const slugify = (name) => name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')

function programUrl(source, slug) {
  switch (source) {
    case 'bugcrowd': return `https://bugcrowd.com/engagements/${slug}`
    case 'hackerone': return `https://hackerone.com/${slug}`
    case 'yeswehack': return `https://yeswehack.com/programs/${slug}`
    case 'intigriti': return `https://app.intigriti.com/programs/${slug}-org/${slug}/detail`
    default: return `https://security.${slug.replace(/-/g, '')}.example.com/vulnerability-disclosure`
  }
}

function buildAssets(domain, slug, count, kind) {
  const clean = slug.replace(/-/g, '')
  const longPath = '/en-US/enterprise/account-management/self-service/v3/dashboard/overview/settings/notifications'
  const patterns = kind === 'in'
    ? [
        (i) => ({ target: i === 0 ? `*.${domain}` : `*.${['api', 'staging', 'dev', 'cloud', 'app', 'cdn', 'edge'][i % 7]}${i > 7 ? Math.floor(i / 7) : ''}.${domain}`, type: 'wildcard' }),
        (i) => ({ target: `https://${['app', 'api', 'www', 'go', 'my', 'portal'][i % 6]}${i > 6 ? i : ''}.${domain}/`, type: 'url' }),
        (i) => ({ target: `https://partner-portal.staging.${domain}${longPath}?tenant=${slug}-${i}`, type: 'url' }),
        (i) => ({ target: `https://checkout.${domain}/payments/callback/oauth2/authorize/step-${i}`, type: 'url' }),
        (i) => ({ target: `com.${clean}${i > 0 ? `.module${i}` : ''}.android`, type: 'android' }),
        (i) => ({ target: `com.${clean}${i > 0 ? `.module${i}` : ''}.ios`, type: 'ios' }),
        (i) => ({ target: `https://github.com/${slug}/${['core', 'api', 'web', 'mobile', 'sdk'][i % 5]}${i > 5 ? `-${i}` : ''}`, type: 'source_code' }),
        (i) => ({ target: `203.0.${113 + (i % 10)}.${(i * 17) % 256}/32`, type: 'ip_address' }),
      ]
    : [
        (i) => ({ target: `https://${['status', 'blog', 'careers', 'shop', 'community', 'docs'][i % 6]}${i > 6 ? i : ''}.${domain}/`, type: 'url' }),
        (i) => ({ target: `https://shop.${domain}/checkout/billing/subscription-management${longPath}?ref=${slug}-${i}`, type: 'url' }),
        (i) => ({ target: `*.${['thirdparty', 'sandbox', 'legacy', 'corp'][i % 4]}${i > 4 ? i : ''}.${domain}`, type: 'wildcard' }),
        (i) => ({ target: `https://mail.${domain}/owa/auth/logon.aspx?replaceCurrent=${i}&url=https%3A%2F%2Fmail.${domain}%2Fowa%2F`, type: 'url' }),
        (i) => ({ target: `198.51.100.${(i * 23) % 256}/28`, type: 'ip_address' }),
      ]

  const assets = []
  const seen = new Set()
  let i = 0
  while (assets.length < count) {
    const pattern = patterns[i % patterns.length]
    const round = Math.floor(i / patterns.length)
    const asset = pattern(round)
    i += 1
    if (seen.has(asset.target)) continue
    seen.add(asset.target)

    if (kind === 'in') {
      asset.max_severity = pick(SEVERITIES)
      asset.eligible_for_bounty = rand() > 0.25
      asset.eligible_for_submission = true
      if (assets.length % 9 === 4) {
        asset.instruction = `Only test against your own tenant. Accounts can be provisioned at https://signup.${domain}/researcher — attacks that degrade production services, physical attacks and social engineering are excluded.`
      }
    } else if (assets.length % 7 === 3) {
      asset.instruction = 'Owned by a third-party vendor; report issues to the vendor directly.'
    }
    assets.push(asset)
  }
  return assets
}

const programs = NAMES.map((name, index) => {
  const slug = slugify(name)
  const domain = `${slug.replace(/-/g, '')}.com`
  const source = SOURCES[index % SOURCES.length]
  const active = index % 11 !== 10

  // A couple of programs deliberately have very large scopes so the
  // detail page pagination is easy to exercise in the demo.
  const inCount = name === 'Shopify' ? 68 : name === 'GitLab' ? 44 : 5 + ((index * 13) % 46)
  const outCount = name === 'Shopify' ? 47 : 2 + ((index * 7) % 34)

  const inDetails = buildAssets(domain, slug, inCount, 'in')
  const outDetails = buildAssets(domain, slug, outCount, 'out')

  const conflicts = []
  if (index % 17 === 3) {
    const target = outDetails[0].target
    inDetails.push({ target, type: outDetails[0].type, max_severity: 'low', eligible_for_bounty: false })
    conflicts.push(target)
  }

  const offersBounties = index % 3 !== 2
  const meta = {
    offers_bounties: offersBounties,
    max_payout: offersBounties ? PAYOUTS[index % PAYOUTS.length] : null,
    min_bounty: offersBounties ? 100 : null,
    currency: index % 5 === 4 ? 'EUR' : 'USD',
    allows_disclosure: index % 4 !== 1,
    managed: index % 6 === 0,
    status: active ? 'open' : 'closed',
  }

  return {
    id: hexId(index + 1),
    source,
    slug,
    name: name === 'AWS'
      ? 'Amazon Web Services — International Vulnerability Disclosure & Bug Bounty Programme'
      : name,
    url: programUrl(source, slug),
    active,
    scopes: inDetails.map((a) => a.target),
    out_of_scope: outDetails.map((a) => a.target),
    scope_details: { in: inDetails, out: outDetails },
    conflicts,
    meta,
    first_seen_at: iso(NOW - (30 + index * 3) * DAY),
    last_synced_at: iso(NOW - (index % 24) * HOUR - (index * 7 % 60) * 60_000),
  }
})

const changes = Array.from({ length: 90 }, (_, j) => {
  const program = programs[(j * 5) % programs.length]
  const type = CHANGE_TYPES[j % CHANGE_TYPES.length]
  const pool = type.startsWith('out_scope') ? program.out_of_scope : program.scopes
  return {
    id: hexId(1000 + j),
    source: program.source,
    program: { slug: program.slug, name: program.name },
    type,
    scope: type.startsWith('out_scope') ? 'out' : 'in',
    target: type.startsWith('program_') ? null : pool[j % pool.length],
    asset_type: type.startsWith('program_') ? null : 'url',
    detected_at: iso(NOW - Math.round(j * 2.2 * HOUR)),
    notified: j % 4 !== 0,
  }
})

const syncRuns = SOURCES.map((source, i) => ({
  id: hexId(2000 + i),
  source,
  status: 'success',
  started_at: iso(NOW - 25 * 60_000 - i * 60_000),
  finished_at: iso(NOW - 25 * 60_000 - i * 60_000 + 45_000),
  duration_ms: 45_000 + i * 1200,
  stats: { inserted: i, updated: 8 + i * 3, changes: changes.filter((c) => c.source === source && NOW - Date.parse(c.detected_at) < DAY).length },
  error: null,
}))

/* ── helpers ─────────────────────────────────────────────────────── */
function paginate(items, url, defaultPerPage = 15) {
  const perPage = Math.min(Math.max(parseInt(url.searchParams.get('per_page') || defaultPerPage, 10) || defaultPerPage, 1), 100)
  const lastPage = Math.max(1, Math.ceil(items.length / perPage))
  const page = Math.min(Math.max(parseInt(url.searchParams.get('page') || '1', 10) || 1, 1), lastPage)
  const slice = items.slice((page - 1) * perPage, page * perPage)
  const pageUrl = (p) => `${url.pathname}?page=${p}&per_page=${perPage}`

  return {
    data: slice,
    links: {
      first: pageUrl(1),
      last: pageUrl(lastPage),
      prev: page > 1 ? pageUrl(page - 1) : null,
      next: page < lastPage ? pageUrl(page + 1) : null,
    },
    meta: {
      current_page: page,
      from: items.length ? (page - 1) * perPage + 1 : null,
      last_page: lastPage,
      path: url.pathname,
      per_page: perPage,
      to: items.length ? (page - 1) * perPage + slice.length : null,
      total: items.length,
    },
  }
}

function sourceBreakdown() {
  return SOURCES.map((source, i) => {
    const own = programs.filter((p) => p.source === source)
    return {
      source,
      programs: own.length,
      active_programs: own.filter((p) => p.active).length,
      changes_24h: changes.filter((c) => c.source === source && NOW - Date.parse(c.detected_at) < DAY).length,
      last_run: syncRuns[i],
    }
  })
}

function stats() {
  return {
    programs: programs.length,
    active_programs: programs.filter((p) => p.active).length,
    scopes: programs.filter((p) => p.active).reduce((sum, p) => sum + p.scopes.length, 0),
    changes: changes.length,
    changes_24h: changes.filter((c) => NOW - Date.parse(c.detected_at) < DAY).length,
    changes_7d: changes.filter((c) => NOW - Date.parse(c.detected_at) < 7 * DAY).length,
    conflicts: programs.filter((p) => p.conflicts.length).length,
    last_run: syncRuns[0],
    sources: sourceBreakdown(),
    schedule_interval: 1800,
    notifications: { telegram: false, discord: false },
    generated_at: iso(Date.now()),
  }
}

function listPrograms(url) {
  let items = [...programs]
  const q = (url.searchParams.get('q') || '').trim().toLowerCase()
  const source = url.searchParams.get('source')
  const active = url.searchParams.get('active')
  const sort = url.searchParams.get('sort') || 'name'
  const direction = url.searchParams.get('direction') === 'desc' ? -1 : 1

  if (q) items = items.filter((p) => `${p.name} ${p.slug} ${p.url}`.toLowerCase().includes(q))
  if (source) items = items.filter((p) => p.source === source)
  if (active === '1' || active === '0') items = items.filter((p) => p.active === (active === '1'))

  const key = sort === 'updated' ? 'last_synced_at' : sort === 'source' ? 'source' : 'name'
  items.sort((a, b) => direction * String(a[key]).localeCompare(String(b[key])))
  return paginate(items, url, 15)
}

function listChanges(url) {
  let items = [...changes]
  const source = url.searchParams.get('source')
  const type = url.searchParams.get('type')
  const program = url.searchParams.get('program')
  const q = (url.searchParams.get('q') || '').trim().toLowerCase()

  if (source) items = items.filter((c) => c.source === source)
  if (type) items = items.filter((c) => c.type === type)
  if (program) items = items.filter((c) => c.program.slug === program)
  if (q) items = items.filter((c) => `${c.target || ''} ${c.program.name}`.toLowerCase().includes(q))
  return paginate(items, url, 25)
}

/* ── server ──────────────────────────────────────────────────────── */
const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`)
  const path = url.pathname.replace(/\/+$/, '')

  const send = (status, body) => {
    const json = JSON.stringify(body)
    res.writeHead(status, {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
      'X-Watch-Tower-Demo': 'true',
    })
    res.end(json)
  }

  // Small delay so loading states are visible, like a real network.
  setTimeout(() => {
    if (req.method !== 'GET') return send(405, { message: 'The demo API is read-only.' })

    if (path === '/api/health') {
      return send(200, { ok: true, service: 'watch-tower-api (demo data)', version: '2.1.0-demo', mongo: true })
    }
    if (path === `${API}/stats`) return send(200, { data: stats() })
    if (path === `${API}/sources`) return send(200, { data: sourceBreakdown() })
    if (path === `${API}/changes/count`) {
      return send(200, {
        data: {
          total: changes.length,
          last_24h: changes.filter((c) => NOW - Date.parse(c.detected_at) < DAY).length,
          last_7d: changes.filter((c) => NOW - Date.parse(c.detected_at) < 7 * DAY).length,
          unnotified: changes.filter((c) => !c.notified).length,
        },
      })
    }
    if (path === `${API}/changes`) return send(200, listChanges(url))
    if (path === `${API}/programs`) return send(200, listPrograms(url))

    const match = path.match(new RegExp(`^${API}/programs/([^/]+)$`))
    if (match) {
      const id = decodeURIComponent(match[1])
      const program = programs.find((p) => p.id === id || p.slug === id)
      return program ? send(200, { data: program }) : send(404, { message: 'Program not found.' })
    }

    return send(404, { message: `No demo route for ${path}` })
  }, 120)
})

server.listen(PORT, HOST, () => {
  console.log(`[watch-tower] DEV-ONLY demo API listening on http://${HOST}:${PORT}`)
  console.log(`[watch-tower] ${programs.length} fake programs, ${changes.length} fake changes — deterministic demo data`)
  console.log('[watch-tower] The real backend is the Laravel core; this script is only for frontend development.')
})
