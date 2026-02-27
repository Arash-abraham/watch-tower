<p align="center">
  <img src="https://laravel.com/img/logomark.min.svg" width="70" alt="Laravel Logo" />
  &nbsp;&nbsp;&nbsp;
  <img src="https://livewire.laravel.com/img/logo.svg" width="70" alt="Livewire Logo" />
</p>

<h1 align="center">⚡ Watch Tower</h1>

<p align="center">
  <strong>Real-Time Asset Monitoring Platform built with Laravel 12 & Livewire 3</strong>
</p>

<p align="center">
  Modern. Reactive. Scalable. Powerful.
</p>

---

## 🚀 About Watch Tower

**Watch Tower (v2)** is a complete evolution of the original project:

🔗 **Version 1 (Bat-Tower)**  
Python + Flask CLI Tool  
👉 https://github.com/Arash-abraham/Bat-Tower  

Version 1 was:
- Command-line only
- Built with Python & Flask
- Sent notifications **only to Discord**
- Triggered only when a new asset was detected

It worked.  
But it was limited.

---

## ⚡ What Changed in Version 2?

Version 2 is not just an update —  
It’s a full architectural transformation.

Now built with:

- **Laravel 12**
- **Livewire 3**
- **Volt (Class-Based Components)**
- **Tailwind CSS**
- (Upcoming) **Laravel Echo for real-time broadcasting**

No more CLI.  
No more single-channel alerts.  
No more static outputs.

Welcome to a full monitoring dashboard.

---

## ✨ Core Features (v2)

### 🖥 Reactive Web Dashboard
Live updates without refreshing — powered by Livewire 3.

### 🔔 Multi-Channel Notifications

When a new asset is detected from your targets, you can choose:

- ✅ Discord  
- ✅ Telegram  
- ✅ Instant In-Dashboard Notification  
- 🔜 SMS (very high probability – planned integration)

Unlike v1 which only supported Discord,  
v2 gives you flexibility and real-time visibility.

---

### ⚡ Real-Time Ready (Laravel Echo)

The system is designed to integrate with **Laravel Echo** for:

- Live broadcast notifications  
- Instant UI updates  
- Future collaborative monitoring  
- WebSocket-powered real-time interactions  

Infrastructure is ready — full implementation is on the roadmap.

---

### 🧩 Clean Architecture

- Volt class-based components  
- Full Livewire 3 reactivity  
- Structured backend logic  
- Role-based authentication system  
- Expandable for teams and APIs  

---

### 🌙 Modern UI

- Tailwind CSS v3
- Dark mode support
- Responsive design
- Clean monitoring-focused layout

Because monitoring should feel powerful.

---

## 🛠 Tech Stack

**Backend**
- Laravel 12.x
- PHP 8.3+

**Frontend**
- Livewire 3
- Volt
- Tailwind CSS

**Database**
- MySQL
- PostgreSQL
- SQLite

**Notifications**
- Discord Webhooks
- Telegram Bot API
- SMS Gateway (planned)

**Real-Time**
- Laravel Echo (Upcoming)

---

## 📊 Version 1 vs Version 2

| Feature | 🦇 Bat-Tower (v1) | ⚡ Watch Tower (v2) |
|----------|------------------|--------------------|
| Tech Stack | Python + Flask | Laravel 12 + Livewire 3 + Volt |
| Interface | CLI Only | Modern Web Dashboard |
| Real-Time UI | ❌ None | ✅ Live Reactive UI |
| Notification Channels | Discord Only | Discord + Telegram + In-App |
| SMS Support | ❌ No | 🔜 Very Likely |
| Architecture | Script-Based | Full Web Application |
| Scalability | Limited | Expandable (Teams / APIs) |
| User Experience | Text Output | Responsive + Dark Mode |

v1 was a script.  
v2 is a platform.

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# Install dependencies
composer install
npm install && npm run dev

# Setup environment
cp .env.example .env
php artisan key:generate

# Run database
php artisan migrate --seed

# Start server
php artisan serve
```

Open:

http://localhost:8000

Start monitoring instantly.

---

## 🗺 Roadmap

- [ ] Full Laravel Echo integration
- [ ] SMS Notifications (Twilio or similar)
- [ ] Multi-user team dashboards
- [ ] Advanced analytics
- [ ] Mobile API layer
- [ ] Full automated test suite
- [ ] Docker production setup

---

## 🤝 Contributing

Ideas, improvements, performance optimizations?

Open an issue.  
Submit a PR.  
Let’s build something powerful.

---

## 📄 License

MIT License

---

<p align="center">
  Crafted with ⚡ + ☕ by Arash Abraham  
  February 2026
</p>
