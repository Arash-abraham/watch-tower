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

The scope collector only reads public scope definitions. Optional asset discovery reads multiple third-party indexes and is run explicitly by the operator.

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
| Subdomain / asset discovery | ✅ opt-in, passive multi-provider discovery for explicit wildcard scopes |
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
docker compose --profile manual up --build
```

| Service | URL |
|---|---|
| Dashboard | http://localhost:5173 |
| API | http://localhost:8000/api/v2.1/stats |
| API health | http://localhost:8000/api/health |
| MongoDB | `mongodb://root:secret@localhost:27017/?authSource=admin` |

The `manual` profile enables the collector; without it Compose starts only MongoDB, the API and the dashboard.
With this profile the collector starts syncing immediately and then every 30 minutes
(`WATCHTOWER_SCAN_INTERVAL`). The first run only records `program_added`
events, so the alert feed is not flooded on a fresh install.

Stop with `docker compose down` (add `-v` to drop the database volume).

### Opt-in subdomain discovery

After syncing programs, review the program rules and authorization before running discovery.
Discovery is manual and limited to explicit `*.example.com` in-scope entries of one
active program. Exact hostnames do not authorize collecting their subdomains.
By default it combines **Subfinder**, **crt.sh**, and **Common Crawl**, plus
any credentialed providers with a key set in the collector environment.
These are third-party services that may receive the wildcard root. No discovered
hostname is directly queried, resolved or probed by Watch Tower.

```bash
# Docker: sync first, then use the source and slug shown on the program's detail page
docker compose --profile manual run --rm collector python monitor.py --once --sources hackerone --no-notify
docker compose --profile manual run --rm collector python discover.py --source hackerone --program PROGRAM_SLUG

# Local: install Subfinder separately and ensure it is on PATH (or select crtsh only)
cd Watch-Tower-Python-Core
python discover.py --source hackerone --program PROGRAM_SLUG --provider crtsh
```

Use `--provider <id>` to select only specific sources (repeatable).
Use `--subfinder /path/to/subfinder` to choose the binary. The Docker image
includes Subfinder. `--timeout` bounds provider/root lookups (300 seconds by
default; HTTP provider budgets are capped at 45 seconds).

| Provider ID | Data | Collector environment |
|---|---|---|
| `subfinder` | Passive sources bundled with the binary | No key needed to start |
| `crtsh` | Public certificate index | No key |
| `commoncrawl` | URL index of the latest published crawl | No key |
| `securitytrails` | Known DNS subdomains | `DISCOVERY_SECURITYTRAILS_KEY` |
| `dnsdb` | Farsight Passive DNS | `DISCOVERY_DNSDB_KEY` |
| `urlscan` | Existing public search results only (no scan submissions) | `DISCOVERY_URLSCAN_KEY` |
| `chaos` | ProjectDiscovery DNS dataset | `DISCOVERY_CHAOS_KEY` |
| `certspotter` | SSLMate certificate index | `DISCOVERY_CERTSPOTTER_KEY` |
| `virustotal` | VirusTotal's direct subdomain relationship (not recursive) | `DISCOVERY_VIRUSTOTAL_KEY` |

For Docker set keys in the root `.env`; for a local collector use
`Watch-Tower-Python-Core/.env`. Keys are passed to the collector, not the API or
browser. Leave unused keys blank. If an explicitly selected provider is missing
its key, the CLI stops before making requests. Provider plans and quotas may vary.

Paginated lookups read at most three pages per root, and DNSDB requests at most
5,000 rows. A run is marked partial when these bounds truncate a response or a
provider fails while other requests succeed. Names already obtained are retained;
a limit alone does not cause a nonzero exit, but a provider failure does.

Results are filtered against machine-readable exclusions; an unparseable exclusion
blocks collection before requests are made. Wildcard certificate names do not count
as exact hostnames. Observations are deduplicated per program, including `crtsh` results
reported by both run paths, and each source retains its most recent collection time.
Counts exclusive to a collector are relative to what the selected collectors returned
on that run. These counts do not prove independent confirmation or current reachability.

Open **Targets → a program** and select **Subdomains** at the top of the page to see historical names,
source timestamps, search, source filters and the latest run summary. Data is also
available from `/api/v2.1/subdomains`. Older names are not deleted when a source fails,
returns no results, or the program scope changes. Always check current rules separately.
Discovery is not scheduled automatically and does not generate change alerts.

### Enabling notifications

Add the following settings to the repository-root `.env` for Docker, or to
`Watch-Tower-Python-Core/.env` for a local collector. Keep this file private.
Either channel can be configured independently.

```dotenv
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
DISCORD_WEBHOOK_URL=
```

- **Telegram:** Create a bot with BotFather and use its token. Start a private
  chat with the bot, or add it to the group/channel and give it permission to
  post. Set the destination chat ID (preserving its minus sign, if present).
- **Discord:** Create a webhook in the destination channel's integrations and
  use its full URL.

Send a test message to each configured channel without syncing data or connecting
to MongoDB:

```bash
# Docker (from the repository root)
docker compose --profile manual run --rm --no-deps --build collector python monitor.py --test-notifications

# Local (from Watch-Tower-Python-Core, with dependencies installed)
python monitor.py --test-notifications
```

The command exits nonzero if no channel is configured or a configured test fails.
For automatic alerts in Docker, start (or recreate after editing `.env`) the
collector with `docker compose --profile manual up -d --build collector`. For
local operation, restart `python monitor.py --watch` after editing its `.env`.
The `WATCHTOWER_TELEGRAM_ENABLED` and `WATCHTOWER_DISCORD_ENABLED` settings affect
only the dashboard indicators and are not needed to send messages.

New alerts are queued for the channels configured when the change is detected.
A failed channel retries its pending batches on the next normal run without
resending batches already acknowledged for the other channel. `notified` is set
once every queued channel confirms delivery; changes recorded before enabling
notifications are not sent retroactively. `--no-notify` neither queues nor sends
alerts. Set `NOTIFY_ON_FIRST_SEEN=false` before the initial sync to suppress new
program alerts while still recording them. Run a single collector per database;
a partially delivered batch or a failure to save confirmation can result in a
retry of messages the provider already accepted.

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
| `GET` | `/subdomains` | Historical passive subdomain observations (read-only) |
| `GET` | `/api/health` | API + MongoDB health |

Full request/response reference: [`docs/API.md`](docs/API.md).

---

## Data model

| Collection | Written by | Contents |
|---|---|---|
| `programs` | collector + API (local programs) | `source`, `slug`, `program_name`, `program_url`, `scopes[]`, `outScopes[]`, `meta`, `conflicts[]`, `active`, `first_seen_at`, `last_synced_at` |
| `changes` | collector | `type` (`program_added`, `scope_added`, `scope_removed`, `out_scope_added`, `out_scope_removed`, `program_removed`, `conflict`), `target`, `source`, `detected_at`, `notified` |
| `sync_runs` | collector | one document per run with status, duration and counters |
| `subdomains` | manual discovery | Historical hostname per program; `observations` stores the latest collection time per source |

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
| `NOTIFY_ON_FIRST_SEEN` | `true` | Send alerts for newly seen programs |
| `NOTIFY_MAX_ITEMS` | `40` | Maximum events per notification batch (no events are dropped) |
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
Manual passive subdomain discovery is available. Next steps include authentication
and team workspaces. See [`docs/PROJECT-REVIEW-FA.md`](docs/PROJECT-REVIEW-FA.md) for a
detailed audit of the current state.

## License

MIT — see [LICENSE](LICENSE).
