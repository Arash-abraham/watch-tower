# <img src="https://laravel.com/img/logomark.min.svg" alt="Laravel" width="50" height="50" style="vertical-align: middle;"> <img src="https://livewire.laravel.com/img/logo.svg" alt="Livewire" width="50" height="50" style="vertical-align: middle;"> Watch Tower ⚡

A sleek, powerful web application for asset monitoring and real-time notifications. Built with **Laravel 12**, **Livewire 3**, and **Volt** for a seamless, reactive experience.  

This is **Version 2** – a complete overhaul and massive upgrade from [Version 1 (Bat-Tower)](https://github.com/Arash-abraham/Bat-Tower), which was a Python/Flask CLI tool. V2 brings a modern web dashboard, multi-channel notifications, and real-time updates, making it far more versatile, user-friendly, and scalable. Say goodbye to command-line limitations!

> "Elevate your monitoring game – watch, detect, notify, all in real-time. 🚀"

## ✨ Key Features

- **Reactive Dashboard**: Live updates on new assets from targets – no refreshing needed!
- **Multi-Channel Notifications**: Choose Discord, Telegram, or in-app dashboard alerts. SMS integration coming soon (high probability!).
- **Class-Based Volt Components**: Elegant, single-file components for clean, maintainable code.
- **Full Livewire 3 Reactivity**: Instant interactions without page reloads.
- **Tailwind CSS Styling**: Beautiful, responsive UI with dark mode support (because monitoring in the dark is cooler 🌙).
- **Real-Time Ready**: Powered by Laravel Echo for upcoming broadcast features like live notifications and collaborative monitoring.
- **Authentication & Security**: Built-in user auth with roles (expandable for teams).
- **Easy Deployment**: Docker support in the works for effortless scaling.

## 🛠️ Tech Stack

- **Backend**: Laravel 12.x (robust, enterprise-grade PHP framework)
- **Frontend**: Livewire 3 + Volt (class-based components for reactive UIs)
- **Styling**: Tailwind CSS v3 + customizable component libraries (e.g., Flowbite or DaisyUI)
- **Database**: MySQL / PostgreSQL / SQLite (flexible options)
- **Real-Time**: Laravel Echo (for websockets and broadcasts)
- **Notifications**: Integrations with Discord, Telegram, and potential SMS gateways
- **Icons & Extras**: Heroicons / Lucide for crisp visuals

[![Laravel 12](https://img.shields.io/badge/Laravel-12-red?style=flat-square&logo=laravel)](https://laravel.com)
[![Livewire 3](https://img.shields.io/badge/Livewire-3-blue?style=flat-square&logo=livewire)](https://livewire.laravel.com)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-38bdf8?style=flat-square&logo=tailwindcss)](https://tailwindcss.com)

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# 2. Install dependencies
composer install
npm install && npm run dev    # or use pnpm / yarn / bun for faster installs

# 3. Setup environment
cp .env.example .env
php artisan key:generate

# 4. Run migrations & seed (if applicable)
php artisan migrate --seed

# 5. Start the servers
php artisan serve
# In another terminal:
npm run dev
```

Head to http://localhost:8000 and start monitoring! For real-time features, set up Laravel Echo with your preferred broadcaster (e.g., Pusher or Reverb).

## 📊 v1 vs v2: Why Upgrade?

Here's a quick comparison to show how Watch Tower (v2) levels up from Bat-Tower (v1):

| Feature                  | v1 (Bat-Tower)                          | v2 (Watch Tower)                              |
|--------------------------|-----------------------------------------|-----------------------------------------------|
| **Tech Stack**           | Python + Flask                          | Laravel 12 + Livewire 3 + Volt               |
| **Interface**            | Command-Line Only (CLI)                 | Modern Web Dashboard with Reactive UI         |
| **Notifications**        | Discord Only (on new assets)            | Discord, Telegram, In-Dashboard + SMS (soon)  |
| **Real-Time Updates**    | None                                    | Yes, via Laravel Echo for instant alerts      |
| **User Experience**      | Basic, text-based                       | Responsive, Dark Mode, Intuitive & Visual     |
| **Scalability**          | Limited to scripts                      | Full web app, easy to extend for teams/APIs   |
| **Deployment**           | Manual script runs                      | Docker-ready, with CI/CD pipeline in roadmap  |
| **Monitoring Depth**     | Basic asset detection                   | Advanced tracking + live dashboard insights   |

v2 isn't just an update – it's a transformation. From a simple CLI notifier to a full-fledged monitoring powerhouse. If you loved v1's simplicity, you'll adore v2's power and polish!

## 📸 Screenshots (Coming Soon)

- v1: Raw CLI output
- v2: Sleek dashboard with live notifications
- Dark mode toggle in action

## 🗺️ Roadmap

- [ ] Integrate Laravel Echo for real-time broadcasting
- [ ] Add SMS notifications (Twilio or similar)
- [ ] Team collaboration features (multi-user dashboards)
- [ ] Mobile app integration via APIs
- [ ] Enhanced analytics & reporting
- [ ] Full test suite (unit, feature, end-to-end)
- [ ] Open-source contributions welcome!

## 🤝 Contributing

Dive in! Open issues for bugs/ideas, or submit PRs to make it even better. Especially if you're into Laravel Echo or Volt optimizations.

Star the repo if it sparks joy 🌟 – feedback is gold!

## 📄 License

MIT License – fork, modify, deploy freely (but credit where due!).

---

Crafted with ❤️⚡☕ by Arash Abraham  
Last updated: February 27, 2026
