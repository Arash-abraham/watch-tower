# ⚡ Watch Tower

> Real-Time Asset Monitoring. Instant Alerts. Zero Blind Spots.

A modern, reactive monitoring platform built with **Laravel 12**, **Livewire 3**, and **Volt**.  
Watch Tower transforms asset tracking from a simple notifier into a powerful, real-time web command center.

This is **Version 2** — a complete architectural rebirth of  
🔗 Bat-Tower (v1 – Python/Flask CLI)

No more terminals.  
No more manual runs.  
No more limitations.

Welcome to live monitoring — done right. 🚀

---

## 🧠 What is Watch Tower?

Watch Tower is a sleek monitoring dashboard that:

• Detects new assets from your defined targets  
• Notifies you instantly across multiple channels  
• Updates live without page refresh  
• Scales from solo usage to team environments  

It’s built to feel fast.  
It’s built to feel modern.  
It’s built to feel powerful.

---

## ✨ Core Features

### ⚡ Reactive Live Dashboard
Real-time asset updates powered by Livewire 3 — no refresh needed.

### 🔔 Multi-Channel Notifications
Choose how you want to be alerted:
- Discord
- Telegram
- In-app dashboard alerts
- SMS (coming soon – very likely 👀)

### 🧩 Class-Based Volt Components
Single-file elegance. Clean architecture. Maintainable structure.

### 🌙 Dark Mode First
Because monitoring hits different at 2AM.

### 🔐 Authentication & Roles
Secure user system with expandable team support.

### 📡 Real-Time Ready
Laravel Echo integration for:
- Live broadcasts
- Instant notifications
- Future collaborative monitoring

### 🐳 Deployment Friendly
Docker support in progress for easy scaling & production deployment.

---

## 🛠 Tech Stack

Backend:
- Laravel 12.x
- PHP 8.3+

Frontend:
- Livewire 3
- Volt (Class-Based Components)
- Tailwind CSS v3
- Heroicons / Lucide

Database:
- MySQL
- PostgreSQL
- SQLite

Real-Time:
- Laravel Echo
- Pusher / Reverb ready

Notifications:
- Discord Webhooks
- Telegram Bot API
- SMS Gateway (Planned)

---

## 🚀 Quick Start

```bash
# 1️⃣ Clone
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# 2️⃣ Install dependencies
composer install
npm install && npm run dev

# 3️⃣ Environment setup
cp .env.example .env
php artisan key:generate

# 4️⃣ Database
php artisan migrate --seed

# 5️⃣ Run servers
php artisan serve
npm run dev
```

Open:

http://localhost:8000

You're live. 🔥

For real-time broadcasting:
Configure Laravel Echo with your preferred broadcaster (Pusher / Reverb).

---

## 📊 v1 vs v2 — The Evolution

|                | 🦇 Bat-Tower (v1) | ⚡ Watch Tower (v2) |
|----------------|-------------------|---------------------|
| Interface      | CLI Only          | Modern Web Dashboard |
| Stack          | Python + Flask    | Laravel + Livewire + Volt |
| Real-Time      | ❌ None           | ✅ Yes (Echo Ready) |
| Notifications  | Discord Only      | Discord + Telegram + In-App |
| UX             | Text Output       | Responsive + Dark Mode |
| Scalability    | Script-Based      | Full Web Architecture |
| Deployment     | Manual            | Docker-Ready (WIP) |

v2 isn’t an upgrade.  
It’s a transformation.

From script → to system.  
From notifier → to platform.

---

## 🗺 Roadmap

- [ ] Full Laravel Echo implementation
- [ ] SMS Notifications (Twilio)
- [ ] Multi-user Team Dashboards
- [ ] API + Mobile Integration
- [ ] Advanced Analytics
- [ ] Test Coverage (Unit + Feature + E2E)
- [ ] CI/CD Pipeline
- [ ] Public Contributions

---

## 🤝 Contributing

Ideas? Improvements? Performance tweaks?  
Open an issue. Submit a PR. Let’s build it bigger.

If it sparks joy — ⭐ the repo.

---

## 📄 License

MIT License  
Fork it. Modify it. Deploy it. Just keep the credit.

---

### Crafted with ⚡ + ☕ by Arash Abraham  
Last updated: February 27, 2026
