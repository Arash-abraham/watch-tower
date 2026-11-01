# Watch Tower API reference

Base URL: `http://localhost:8000/api`

All endpoints return JSON. Collections are paginated with Laravel's standard
envelope:

```json
{
  "data": [ /* items */ ],
  "links": { "first": "...", "last": "...", "prev": null, "next": "..." },
  "meta": { "current_page": 1, "last_page": 5, "per_page": 15, "total": 67 }
}
```

Rate limit: 120 requests per minute per IP (`429` when exceeded).

---

## Health

### `GET /api/health`

```json
{
  "status": "ok",
  "service": "watch-tower-api",
  "version": "2.1",
  "mongo": true,
  "error": null,
  "time": "2026-10-31T08:12:44+00:00"
}
```

Returns `503` with `"status": "degraded"` when MongoDB is unreachable.

---

## Stats

### `GET /api/v2.1/stats`

```json
{
  "data": {
    "programs": 947,
    "active_programs": 946,
    "scopes": 48400,
    "changes": 951,
    "changes_24h": 4,
    "changes_7d": 951,
    "conflicts": 12,
    "last_run": {
      "id": "6712...",
      "source": "intigriti",
      "status": "success",
      "started_at": "2026-10-31T08:00:00+00:00",
      "finished_at": "2026-10-31T08:00:02+00:00",
      "duration_ms": 1980,
      "stats": { "inserted": 0, "updated": 2, "changes": 2 }
    },
    "sources": [
      {
        "source": "bugcrowd",
        "programs": 297,
        "active_programs": 297,
        "changes_24h": 2,
        "last_run": { "...": "same shape as last_run above" }
      }
    ],
    "schedule_interval": 1800,
    "notifications": { "telegram": false, "discord": false },
    "generated_at": "2026-10-31T08:12:44+00:00"
  }
}
```

### `GET /api/v2.1/sources`

Same `sources` array as above, without the surrounding counters.

---

## Programs

### `GET /api/v2.1/programs`

Query parameters:

| Name | Type | Default | Notes |
|---|---|---|---|
| `q` | string | — | Case-insensitive match on name, URL, in-scope and out-of-scope assets |
| `source` | enum | — | `bugcrowd`, `hackerone`, `yeswehack`, `intigriti`, `local` |
| `active` | `1` / `0` | — | Filter on the program state |
| `bounty_only` | bool | `false` | Only programs that offer bounties |
| `conflicts_only` | bool | `false` | Only programs with in/out-scope overlaps |
| `sort` | enum | `name` | `name`, `updated`, `source` |
| `direction` | enum | `asc` | `asc`, `desc` |
| `page` | int | `1` | |
| `per_page` | int | `15` | Max 100 |

Item shape:

```json
{
  "id": "6712f0c1a1b2c3d4e5f60718",
  "source": "bugcrowd",
  "slug": "tesla",
  "name": "Tesla",
  "url": "https://bugcrowd.com/engagements/tesla",
  "active": true,
  "scopes": ["*.tesla.com", "*.teslamotors.com"],
  "out_of_scope": ["https://shop.tesla.com/"],
  "scope_details": {
    "in": [{ "target": "*.tesla.com", "type": "wildcard" }],
    "out": [{ "target": "https://shop.tesla.com/", "type": "website" }]
  },
  "conflicts": [],
  "meta": { "allows_disclosure": true, "managed": false, "max_payout": 15000 },
  "first_seen_at": "2026-10-30T21:31:00+00:00",
  "last_synced_at": "2026-10-31T08:00:00+00:00"
}
```

### `GET /api/v2.1/programs/{id}`

Returns `{ "data": { ...program } }` or `404`.

### `POST /api/v2.1/programs`

Creates a program with `source = "local"` (the collector never touches these).

```json
{
  "program_name": "Acme Internal",
  "program_url": "https://example.com/security",
  "scopes": ["*.acme.test", "api.acme.test"],
  "out_of_scope": ["status.acme.test"],
  "meta": { "owner": "security-team" }
}
```

Validation: `program_name` required (max 200), `program_url` must be a URL,
scope arrays max 5000 entries. `409` when a local program with the same slug
exists.

### `PUT /api/v2.1/programs/{id}`

Same fields, all optional. The slug is regenerated when `program_name` changes
and `conflicts` is recalculated.

### `DELETE /api/v2.1/programs/{id}`

`204 No Content`.

---

## Changes (alerts)

### `GET /api/v2.1/changes`

| Name | Type | Default | Notes |
|---|---|---|---|
| `q` | string | — | Match on target or program name |
| `source` | enum | — | Source filter |
| `type` | enum | — | `program_added`, `program_removed`, `scope_added`, `scope_removed`, `out_scope_added`, `out_scope_removed`, `conflict` |
| `program` | string | — | Program slug |
| `since` | ISO date | — | `detected_at >= since` |
| `notified` | `1` / `0` | — | Delivery state |
| `page`, `per_page` | int | `1`, `25` | |

```json
{
  "id": "6712f0c1a1b2c3d4e5f60719",
  "source": "bugcrowd",
  "program": { "slug": "tesla", "name": "Tesla" },
  "type": "scope_added",
  "scope": "in",
  "target": "api.tesla.com",
  "asset_type": "api",
  "detected_at": "2026-10-31T08:00:00+00:00",
  "notified": true
}
```

### `GET /api/v2.1/changes/count`

```json
{ "data": { "total": 951, "last_24h": 4, "last_7d": 951, "unnotified": 0 } }
```

---

## Subdomains

Reserved for the asset-discovery monitors. The collection exists and the API is
read-only; the collector does not populate it yet.

### `GET /api/v2.1/subdomains`

Filters: `source`, `program`, `q`, `page`, `per_page`.

### `GET /api/v2.1/subdomains/{id}`

Returns `{ "data": { ... } }` or `404`.

---

## Errors

| Status | Meaning |
|---|---|
| `404` | Unknown id (invalid ObjectId or missing document) |
| `409` | Duplicate local program |
| `422` | Validation failed — `{ "message": ..., "errors": { field: [..] } }` |
| `429` | Rate limit exceeded |
| `503` | MongoDB unavailable (health endpoint) |
