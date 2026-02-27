<p align="center">
  <img src="https://laravel.com/img/logomark.min.svg" width="70" alt="Laravel Logo" />
  &nbsp;&nbsp;&nbsp;
  <img src="https://livewire.laravel.com/img/logo.svg" width="70" alt="Livewire Logo" />
</p>

<h1 align="center">⚡ Watch Tower</h1>

<p align="center">
  <strong>Enterprise-Ready Real-Time Asset Monitoring</strong><br>
  Built with Laravel 12 + Livewire 3
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Laravel-12-red?style=for-the-badge&logo=laravel" />
  <img src="https://img.shields.io/badge/Livewire-3-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active_Development-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Version-2.0-informational?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" />
</p>

---

# 🚀 Monitor Smarter. React Faster. Miss Nothing.

**Watch Tower v2** is a full-scale transformation of the original CLI-based monitoring tool into a modern, reactive SaaS-ready platform.

> From script → to system  
> From notifier → to real-time platform  

🔗 **Version 1 (Bat-Tower – Python/Flask CLI)**  
https://github.com/Arash-abraham/Bat-Tower  

---

# 🧠 The Evolution

## 🦇 Version 1 — Bat-Tower

- Built with Python + Flask  
- CLI-only interface  
- Triggered when new asset detected  
- Sent notification only to Discord  
- No dashboard  
- No real-time UI  
- No multi-user capability  

It worked — but it was limited.

---

## ⚡ Version 2 — Watch Tower

Now rebuilt with:

- **Laravel 12**
- **Livewire 3**
- **Volt (Class-Based Components)**
- **Tailwind CSS**
- **Laravel Echo (Planned for WebSocket Broadcasting)**

This is not a refactor.  
This is a complete architectural redesign.

---

# 💎 SaaS-Style Feature Highlights

## 🖥 Real-Time Reactive Dashboard
No refresh.  
No polling hacks.  
Pure Livewire 3 reactivity.

Assets appear instantly when detected.

---

## 🔔 Multi-Channel Smart Notifications

When a new asset is detected from your targets, choose your preferred alert channel:

- ✅ Discord Webhook  
- ✅ Telegram Bot  
- ✅ Instant In-Dashboard Notification  
- 🔜 SMS Integration (high probability, planned)

Unlike v1 which only supported Discord —  
v2 gives you flexibility and redundancy.

---

## ⚡ Laravel Echo Ready (Real-Time Broadcasting)

The system is structured to integrate **Laravel Echo** for:

- WebSocket-powered notifications  
- Live broadcast events  
- Future collaborative monitoring  
- Real-time multi-user sync  

Infrastructure prepared. Full rollout on roadmap.

---

## 🏗 Clean, Scalable Architecture

- Volt class-based components  
- Fully reactive UI  
- Role-based authentication  
- Expandable to teams  
- API-ready structure  
- Designed for Docker deployment  

---

## 🌙 Modern Monitoring Experience

- Dark mode  
- Responsive layout  
- Clean monitoring-centric design  
- Built for performance  

Monitoring should feel powerful — not primitive.

---

# 📊 Complete Comparison — v1 vs v2

| Category | 🦇 Bat-Tower (v1) | ⚡ Watch Tower (v2) |
|-----------|------------------|--------------------|
| Core Stack | Python + Flask | Laravel 12 + Livewire 3 + Volt |
| Interface | Command Line Only | Modern Web Dashboard |
| UI Reactivity | ❌ None | ✅ Full Livewire Reactivity |
| Real-Time Updates | ❌ No | ⚡ Laravel Echo (Planned) |
| Notification Channels | Discord Only | Discord + Telegram + In-App |
| SMS Support | ❌ No | 🔜 Planned |
| User Authentication | ❌ None | ✅ Built-in Auth |
| Role System | ❌ None | ✅ Expandable |
| Multi-User Support | ❌ No | ✅ Architecture Ready |
| Dashboard Visibility | ❌ None | ✅ Live Asset Feed |
| Scalability | Limited Script | Full Web Application |
| Deployment | Manual Execution | Docker-Ready (WIP) |
| Code Structure | Script-Based | Component-Based Architecture |
| API Capability | ❌ No | 🔜 Planned |
| UX | Text Output | Responsive + Dark Mode |
| Extensibility | Hard | Designed for Expansion |

v1 was a utility.  
v2 is a monitoring platform.

---

# 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# Install dependencies
composer install
npm install && npm run dev

# Environment setup
cp .env.example .env
php artisan key:generate

# Database
php artisan migrate --seed

# Run server
php artisan serve
```

Visit:

http://localhost:8000

Start monitoring instantly.

---

# 🗺 Roadmap

- [ ] Full Laravel Echo broadcasting
- [ ] SMS integration (Twilio or similar)
- [ ] Team dashboards
- [ ] Advanced analytics
- [ ] Mobile/API layer
- [ ] CI/CD pipeline
- [ ] Full automated testing
- [ ] Production Docker setup

---

# 🤝 Contributing

This project is evolving fast.

Have ideas?
Performance optimizations?
Architecture suggestions?

Open an issue or submit a PR.

Let’s build something powerful.

---

# 📄 License

MIT License

---

<p align="center">
  Built with ⚡ + ☕ by Arash Abraham  
  2026
</p>
