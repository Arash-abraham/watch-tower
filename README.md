
<p align="center">
  <img src="https://laravel.com/img/logomark.min.svg" height="80" alt="Laravel Logo" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://livewire.laravel.com/img/logo.svg" height="80" alt="Livewire Logo" />
</p>

<h1 align="center">Watch Tower</h1>

<p align="center">
  Real-Time Asset Monitoring Platform<br>
  Built with Laravel 12 & Livewire 3
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Laravel-12-red?style=for-the-badge&logo=laravel" />
  <img src="https://img.shields.io/badge/Livewire-3-4E56A6?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Version-2.0-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" />
</p>

---

# Real-Time Monitoring Without Blind Spots

Watch Tower is a modern monitoring system designed to detect newly added assets from defined targets and notify you instantly across multiple channels.

Version 2 is a complete architectural rebuild of:

Bat-Tower (Version 1 – Python/Flask CLI)  
https://github.com/Arash-abraham/Bat-Tower  

---

# Hero Preview

<p align="center">
  <img src="img/demo.gif" alt="Watch Tower Live Demo" width="900"/>
</p>

> Replace `img/demo.gif` with your animated dashboard recording.

This dashboard demonstrates:

- Live asset feed updates  
- Instant notification triggers  
- Multi-channel alert routing  
- Reactive UI powered by Livewire 3  

---

# Product Evolution

## Before Version 1 (Early Prototype)

Originally, the system was a very small local script.

It simply monitored HackerOne program updates and immediately printed when a new asset was added.

<p align="center">
  <img src="img/photo_2026-02-27_18-22-04.jpg" alt="Early Monitoring Script Screenshot" width="700"/>
</p>

This was the seed.

---

## Version 1 – Bat-Tower

- Python + Flask
- CLI-only interface
- Trigger-based detection
- Discord-only notifications
- No dashboard
- No multi-user support

Functional, but limited in scope.

---

## Version 2 – Watch Tower

Rebuilt entirely using:

- Laravel 12
- Livewire 3
- Volt class-based components
- Tailwind CSS
- Architected for Laravel Echo (WebSocket broadcasting)

This version introduces:

- Reactive web dashboard
- Multi-channel notifications
- Authentication system
- Scalable architecture
- SaaS-ready foundation

---

# Core Capabilities

## Real-Time Reactive Dashboard

Assets appear instantly without refresh.

Powered by Livewire 3 reactivity, structured for Laravel Echo integration.

Designed for speed and clarity.

---

## Multi-Channel Notification Engine

When a new asset is detected:

You choose how you’re notified:

- Discord
- Telegram
- In-dashboard alerts
- SMS (planned, high probability)

Unlike v1 which supported only Discord, v2 introduces redundancy and flexibility.

---

## Laravel Echo Ready

The architecture is prepared for:

- WebSocket-powered live broadcasting
- Real-time UI synchronization
- Multi-user concurrent updates
- Future collaborative monitoring features

---

# Full Comparison — v1 vs v2

| Category | Bat-Tower (v1) | Watch Tower (v2) |
|-----------|----------------|------------------|
| Core Stack | Python + Flask | Laravel 12 + Livewire 3 + Volt |
| Interface | CLI Only | Modern Web Dashboard |
| Real-Time UI | None | Live Reactive UI |
| WebSockets | No | Laravel Echo Ready |
| Notification Channels | Discord Only | Discord + Telegram + In-App |
| SMS Support | No | Planned |
| Dashboard | None | Live Monitoring Panel |
| Authentication | None | Built-in Auth |
| Multi-User | No | Architecture Ready |
| Role System | No | Expandable |
| Scalability | Script-Based | Full Web Application |
| Deployment | Manual | Docker-Ready (WIP) |
| Extensibility | Limited | Designed for Growth |
| UX | Text Output | Responsive + Dark Mode |

Version 1 was a script.

Version 2 is a monitoring platform.

---

# For Users

Watch Tower helps you:

- Detect new assets instantly
- Reduce manual monitoring
- Centralize alerts
- Scale monitoring workflows
- Eliminate blind spots

Built for security researchers, DevSecOps teams, and monitoring-heavy workflows.

---

# For Investors & Product Vision

Watch Tower is positioned as:

A scalable monitoring infrastructure platform.

Potential expansion paths:

- SaaS multi-tenant deployment
- Subscription-based alert tiers
- Team collaboration features
- Enterprise integrations
- API-based monitoring ecosystem
- Advanced analytics & reporting layer

With Laravel 12 foundation and reactive architecture, the product is designed for growth, not just utility.

The goal is to evolve from a monitoring dashboard into a full asset intelligence platform.

---

# Roadmap

- Full Laravel Echo broadcasting
- SMS integration (Twilio or similar)
- Multi-user team dashboards
- Advanced analytics module
- Public API
- CI/CD automation
- Production Docker setup
- Comprehensive test coverage

---

# Quick Start

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

Visit:

http://localhost:8000

---

# License

MIT License

---

<p align="center">
  Built by Arash Abraham — 2026
</p>
