<p align="center">
  <img src="https://laravel.com/img/logomark.min.svg" height="80" alt="Laravel Logo" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://livewire.laravel.com/img/logo.svg" height="80" alt="Livewire Logo" />
</p>

<h1 align="center">⚡ Watch Tower</h1>

<p align="center">
  <strong>Real-Time Asset Monitoring Platform</strong><br>
  Built with Laravel 12 + Livewire 3
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Laravel-12-red?style=for-the-badge&logo=laravel" />
  <img src="https://img.shields.io/badge/Livewire-3-4E56A6?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Version-2.0-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Actively_Developed-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" />
</p>

---

# 🚀 From CLI Tool → To Real-Time Monitoring Platform

**Watch Tower v2** is a complete evolution of:

🦇 **Bat-Tower (Version 1)**  
Python + Flask CLI Tool  
🔗 https://github.com/Arash-abraham/Bat-Tower  

---

## 🦇 Version 1 – What It Was

- Built with Python + Flask  
- CLI-only interface  
- Checked targets for new assets  
- If found → Sent notification to Discord  
- No dashboard  
- No real-time UI  
- No flexibility in notification channels  

Simple. Functional. Limited.

---

# ⚡ Version 2 – What It Became

Rebuilt from the ground up using:

- **Laravel 12**
- **Livewire 3**
- **Volt (Class-Based Components)**
- **Tailwind CSS**
- Designed for **Laravel Echo (WebSocket Broadcasting)**

This isn’t an upgrade.

It’s an architectural transformation.

---

# 💎 SaaS-Style Feature Highlights

## 🖥 1️⃣ Real-Time Reactive Dashboard

A live monitoring control panel.

- Assets appear instantly  
- No refresh required  
- Powered by Livewire 3 reactivity  
- Designed for real-time experience  

Feels like a SaaS product — not a script.

---

## 🔔 2️⃣ Smart Multi-Channel Notifications

When a new asset is detected from your targets:

Choose your delivery channel:

- ✅ Discord Webhook  
- ✅ Telegram Bot  
- ✅ Instant In-Dashboard Notification  
- 🔜 SMS Integration (very high probability – planned)

Unlike v1 which only supported Discord,  
v2 provides redundancy + flexibility.

Never miss critical updates again.

---

## ⚡ 3️⃣ Laravel Echo Ready (Real-Time Broadcasting)

Infrastructure prepared for:

- WebSocket-based live events  
- Instant broadcast notifications  
- Multi-user live synchronization  
- Future collaborative monitoring  

Laravel Echo integration is on the roadmap and architecturally supported.

---

## 🔐 4️⃣ Authentication & Expandability

- Built-in authentication system  
- Role-ready structure  
- Multi-user scalable design  
- API-ready foundation  

Ready to evolve into a team-ready SaaS platform.

---

## 🌙 5️⃣ Modern Monitoring Experience

- Dark mode  
- Responsive layout  
- Clean Tailwind UI  
- Monitoring-focused UX  

Because powerful tools should look powerful.

---

# 📊 Full Comparison — v1 vs v2

| Category | 🦇 Bat-Tower (v1) | ⚡ Watch Tower (v2) |
|-----------|------------------|--------------------|
| Core Stack | Python + Flask | Laravel 12 + Livewire 3 + Volt |
| Interface | CLI Only | Modern Web Dashboard |
| UI Reactivity | ❌ None | ✅ Full Livewire Reactivity |
| Real-Time Capability | ❌ No | ⚡ Laravel Echo Ready |
| Notification Channels | Discord Only | Discord + Telegram + In-App |
| SMS Alerts | ❌ No | 🔜 Planned |
| Dashboard | ❌ None | ✅ Live Asset Feed |
| Authentication | ❌ None | ✅ Built-in Auth |
| Multi-User | ❌ No | ✅ Architecture Ready |
| Role System | ❌ No | 🔜 Expandable |
| Scalability | Script-Based | Full Web Application |
| Deployment | Manual Run | Docker-Ready (WIP) |
| Extensibility | Limited | Designed for Growth |
| UX | Text Output | Responsive + Dark Mode |
| Architecture | Single Script | Component-Based System |

v1 was a tool.  
v2 is a platform.

---

# 🚀 Quick Start

```bash
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

composer install
npm install && npm run dev

cp .env.example .env
php artisan key:generate

php artisan migrate --seed
php artisan serve
```

Open:

http://localhost:8000

Start monitoring instantly.

---

# 🗺 Roadmap

- [ ] Full Laravel Echo broadcasting
- [ ] SMS integration (Twilio or similar)
- [ ] Team dashboards
- [ ] Advanced analytics
- [ ] Mobile/API integration
- [ ] CI/CD pipeline
- [ ] Full test coverage
- [ ] Production Docker setup

---

# 🤝 Contributing

Watch Tower is evolving fast.

Ideas? Improvements? Architecture upgrades?

Open an issue.  
Submit a PR.  
Let’s build something serious.

---

# 📄 License

MIT License

---

<p align="center">
  Crafted with ⚡ + ☕ by Arash Abraham  
  2026
</p>
