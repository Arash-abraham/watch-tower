# Watch Tower

<p align="center">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" height="42" />
  &nbsp;&nbsp;
  <img src="https://laravel.com/img/logomark.min.svg" height="42" />
  &nbsp;&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vuejs/vuejs-original.svg" height="42" />
</p>

<h1 align="center">Watch Tower</h1>

<p align="center">
  Continuous bounty scope monitoring
  <br>
  Python collector · Laravel API · Vue dashboard
</p>

Watch Tower continuously watches the public bug-bounty datasets (Bugcrowd, HackerOne, YesWeHack,
Intigriti), stores every program's in-scope and out-of-scope assets, detects what
changed since the previous run and tells you about it — on a dashboard and on
Telegram/Discord.

The scope collector only reads public scope definitions. Optional asset discovery uses subfinder passive sources and is run explicitly by the operator.

<p align="center">
  <img src="img/Neon Watch Tower Monitoring Cycle.png" alt="Watch Tower architecture — datasets → Python collector → MongoDB → Laravel API → Vue dashboard, with Telegram/Discord notifications" width="860" />
</p>

---

## What it actually does

| Capability | Status |
|---|---|
| Fetch + normalise Bugcrowd / HackerOne / YesWeHack / Intigriti | ✅ |
| Store programs, in-scope and out-of-scope assets in MongoDB | ✅ |
| Diff against the previous snapshot, one alert per change | ✅ |
| Telegram + Discord notifications (per-run summary, chunked) | ✅ |
| Scheduler (`--watch`) and one-shot runs (`--once`) | ✅ |
| REST API: programs, changes, stats, sources, subdomains, health | ✅ |
| Dashboard: live stats, program browser, alert feed, sources, monitors | ✅ |
| Subdomain / asset discovery | ✅ opt-in, passive subfinder discovery for wildcard scopes |
| Authentication / multi-tenant workspaces | 🚧 planned |

---

## Screenshots

The screenshots below show the running Vue dashboard using the project's **demo API**;
the programs, assets, alerts and health status shown are sample data, not live results.

### Home
![Home page](img/screenshots/home.jpg)

### Dashboard
![Dashboard overview](img/screenshots/dashboard.jpg)

### Applications and sources
![Applications and sources](img/screenshots/sources.jpg)

### Targets and assets
![Targets and assets](img/screenshots/programs.jpg)

### Program details
![Program details and scope inventory](img/screenshots/program-detail.jpg)

### Monitors
![Monitors](img/screenshots/monitors.jpg)

### Alerts
![Alerts](img/screenshots/alerts.jpg)

### Settings
![Settings](img/screenshots/settings.jpg)

---

## Quick start (Docker)

Requirements: Docker with the Compose plugin.

```bash
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower
cp .env.example .env          # edit MONGO_ROOT_PASSWORD / notification tokens if you want
docker compose up --build
```

| Service | URL |
|---|---|
| Dashboard | http://localhost:5173 |
| API | http://localhost:8000/api/v2.1/stats |
| API health | http://localhost:8000/api/health |
| Collector health | http://localhost:8080/health |
| MongoDB | `mongodb://root:secret@localhost:27017/?authSource=admin` |

The collector starts syncing immediately and then every 30 minutes
(`WATCHTOWER_SCAN_INTERVAL`). The first run only records `program_added`
events, so the alert feed is not flooded on a fresh install.

Stop with `docker compose down` (add `-v` to drop the database volume).

### Opt-in subdomain discovery

After syncing programs, review the program rules and authorization before running discovery.
Discovery is manual and only enumerates explicit `*.example.com` in-scope entries of
one active program; exact hostnames are not treated as permission to enumerate their
subdomains. Subfinder queries third-party passive sources, which may receive the domain.
Results are filtered against machine-readable out-of-scope hostnames and wildcards;
a program with an unparseable exclusion is skipped rather than guessed. This filtering
cannot interpret all program policies, so validate results against the original rules.
No DNS resolution or target probing is performed, and results are historical (not removed
when a later run does not return them). API `/api/v2.1/subdomains` exposes the results.

```bash
# Docker: sync first, then use the source and slug shown in the program API
docker compose --profile manual run --rm collector python monitor.py --once --sources hackerone
docker compose --profile manual run --rm collector python discover.py --source hackerone --program PROGRAM_SLUG

# Local: install ProjectDiscovery subfinder separately and ensure it is on PATH
cd Watch-Tower-Python-Core
python discover.py --source hackerone --program PROGRAM_SLUG
```

Use `--subfinder /path/to/subfinder` to choose the binary and `--timeout 300` to
change the per-domain timeout. A failed enumeration returns a nonzero exit code;
successful domains are still saved. The Docker collector image includes subfinder.
Discovery is not scheduled automatically and does not generate change alerts.

### Enabling notifications

Put either of these in `.env` and restart the collector:

```dotenv
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=-1001234567890
# and/or
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

Every detected change is sent once; the `notified` flag is then set in
MongoDB, and the dashboard shows which alerts are still pending.

---

## Local development (no Docker)

You need: PHP 8.3 with the `mongodb` extension, Composer, Node 22, Python 3.12
and a running MongoDB (the compose file's `mongo` service is enough:
`docker compose up -d mongo`).

### 1. Collector

```bash
cd Watch-Tower-Python-Core
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # DB_PORT defaults to 27017

python monitor.py --once                  # sync everything once
python monitor.py --watch --interval 900  # keep running
python monitor.py --once --sources bugcrowd --no-notify
python monitor.py --once --dry-run        # fetch + normalise, no DB writes
```

### 2. API

```bash
cd Watch-Tower-Laravel-Core
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan serve --host=0.0.0.0 --port=8000
```

`DB_URI` must point at the same MongoDB the collector writes to. The API has no
SQL dependency: migrations only create Mongo collections and indexes.

### 3. Dashboard

```bash
cd Watch-Tower-Vue-Js-Core
npm ci
npm run dev        # http://localhost:5173, /api is proxied to :8000
```

Set `VITE_PROXY_TARGET` if the API is not on `http://127.0.0.1:8000`.

---

## API

Base path: `/api/v2.1` (throttled to 120 requests/minute).

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/stats` | Counters, per-source breakdown, last collector run, schedule |
| `GET` | `/sources` | Programs and 24h changes per source |
| `GET` | `/programs` | Paginated programs — filters: `q`, `source`, `active`, `bounty_only`, `conflicts_only`, `sort`, `direction`, `page`, `per_page` |
| `GET` | `/programs/{id}` | One program |
| `POST` | `/programs` | Create a `local` program |
| `PUT` | `/programs/{id}` | Update a program |
| `DELETE` | `/programs/{id}` | Delete a program |
| `GET` | `/changes` | Alert feed — filters: `q`, `source`, `type`, `program`, `since`, `notified`, `page`, `per_page` |
| `GET` | `/changes/count` | Totals (all / 24h / 7d / unnotified) |
| `GET` | `/subdomains` | Reserved for asset discovery (read-only) |
| `GET` | `/api/health` | API + MongoDB health |

Full request/response reference: [`docs/API.md`](docs/API.md).

---

## Data model

| Collection | Written by | Contents |
|---|---|---|
| `programs` | collector + API (local programs) | `source`, `slug`, `program_name`, `program_url`, `scopes[]`, `outScopes[]`, `meta`, `conflicts[]`, `active`, `first_seen_at`, `last_synced_at` |
| `changes` | collector | `type` (`program_added`, `scope_added`, `scope_removed`, `out_scope_added`, `out_scope_removed`, `program_removed`, `conflict`), `target`, `source`, `detected_at`, `notified` |
| `sync_runs` | collector | one document per run with status, duration and counters |
| `subdomains` | future | reserved for asset discovery |

The Python core and the Laravel models share this schema — it is the contract
between the two services.

---

## Configuration

### Collector (`Watch-Tower-Python-Core/.env`)

| Variable | Default | Purpose |
|---|---|---|
| `MONGO_URI` / `DB_URI` | `mongodb://localhost:27017/` (built from `DB_*`) | MongoDB connection |
| `DB_NAME` | `watch-tower` | Database name |
| `SOURCES` | `bugcrowd,hackerone,yeswehack,intigriti` | Sources to sync |
| `SCAN_INTERVAL_SECONDS` | `1800` | Delay between runs in `--watch` mode |
| `BOUNTY_DATA_BASE_URL` | arkadiyt raw URL | Dataset location |
| `DEACTIVATE_MISSING` | `true` | Mark programs missing from the latest snapshot as inactive |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | — | Telegram channel |
| `DISCORD_WEBHOOK_URL` | — | Discord channel |
| `NOTIFY_MAX_ITEMS` | `40` | Lines per notification message |
| `WATCH_DIR` | project dir | Folder that contains the local `programs/*.json` files |
| `API_PORT` | `8080` | Health service port |

### API (`Watch-Tower-Laravel-Core/.env`)

| Variable | Default | Purpose |
|---|---|---|
| `DB_CONNECTION` | `mongodb` | Must stay `mongodb` |
| `DB_URI` | `mongodb://127.0.0.1:27017` | Mongo connection string |
| `DB_DATABASE` | `watch-tower` | Database name |
| `FRONTEND_URL` | `*` | Allowed CORS origin |
| `WATCHTOWER_SOURCES` | all sources + `local` | Sources displayed by the dashboard |
| `WATCHTOWER_SCAN_INTERVAL` | `1800` | Shown on the dashboard |

### Dashboard (`Watch-Tower-Vue-Js-Core/.env`)

| Variable | Default | Purpose |
|---|---|---|
| `VITE_API_BASE_URL` | `/api/v2.1` | API base as seen by the browser |
| `VITE_PROXY_TARGET` | `http://127.0.0.1:8000` | Dev-server proxy target |
| `VITE_PORT` | `5173` | Dev-server port |

---

## Tests

```bash
cd Watch-Tower-Python-Core
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v     # diff, normaliser, sync (mongomock)

cd ../Watch-Tower-Vue-Js-Core
npm ci && npm run build                     # production build check

cd ../Watch-Tower-Laravel-Core
composer install && php artisan migrate
```

CI runs all three (`.github/workflows/ci.yml`).

---

## Project layout

```
Watch-Tower-Python-Core/    collector: sources, normaliser, diff, notifier, Mongo layer
Watch-Tower-Laravel-Core/   REST API: models, resources, controllers, migrations
Watch-Tower-Vue-Js-Core/    dashboard: Vue 3 + Vite + Tailwind
docs/                       API reference and reviews
docker-compose.yml          full stack (mongo + api + collector + web)
```

---

## Status

This is an early but working build: the full loop
*fetch → normalise → diff → store → notify → display* runs end to end.
Next steps are asset discovery (subdomains), authentication, and team
workspaces. See [`docs/PROJECT-REVIEW-FA.md`](docs/PROJECT-REVIEW-FA.md) for a
detailed audit of the current state.

## License

MIT — see [LICENSE](LICENSE).
