# Watch Tower ⚡

[![Laravel](https://img.shields.io/badge/laravel-%23ff2d20.svg?style=for-the-badge&logo=laravel&logoColor=white)](https://laravel.com)
[![Livewire](https://img.shields.io/badge/livewire-%234e56a6.svg?style=for-the-badge&logo=livewire&logoColor=white)](https://livewire.laravel.com)

A sleek, modern web application for asset monitoring and notifications, built with **Laravel 12**, **Livewire 3** + **Volt**.  
This is **Version 2** – a complete overhaul from the ground up, making it way more powerful and user-friendly than Version 1.  

> "Stay ahead of the game: Real-time asset tracking, multi-channel alerts, and a beautiful dashboard – all in one place."

Check out [Version 1 (Bat-Tower)](https://github.com/Arash-abraham/Bat-Tower) – the original CLI tool built with Python and Flask. It was great for basics, but v2 takes it to the next level with a full web interface, more notification options, and upcoming real-time features via Laravel Echo.

## ✨ Why Version 2 is Better

Version 1 was a simple command-line tool: It monitored targets, detected new assets, and sent notifications only to Discord.  
Version 2 transforms it into a full-fledged web app:
- Interactive dashboard for real-time updates and in-app notifications.
- Flexible alerts: Choose Discord, Telegram, or both – with high chances of SMS integration soon.
- Reactive UI powered by Livewire and Volt for seamless, no-refresh experiences.
- Scalable backend with Laravel 12 for better performance and easier maintenance.
- Upcoming: Laravel Echo for true real-time broadcasting.

## 🛠️ Tech Stack

- **Backend**: Laravel 12.x
- **Frontend**: Livewire 3 + Volt (class-based components for elegance)
- **Styling**: Tailwind CSS v3 + your favorite UI components (e.g., DaisyUI or Flowbite)
- **Database**: MySQL / PostgreSQL / SQLite (flexible options)
- **Real-time (Coming Soon)**: Laravel Echo for instant updates
- **Notifications**: Discord, Telegram, Dashboard – SMS on the horizon
- **Deployment**: Ready for Docker and CI/CD

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# 2. Install dependencies
composer install
npm install && npm run dev    # or use pnpm/yarn/bun

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

Head to http://localhost:8000 and start monitoring!

## 📊 Version Comparison

Here's a quick showdown between v1 and v2 – see why upgrading is a no-brainer:

| Feature                  | Version 1 (Python/Flask)                  | Version 2 (Laravel/Livewire)                     |
|--------------------------|-------------------------------------------|--------------------------------------------------|
| **Interface**            | Command-line only (CLI)                   | Full web dashboard with reactive UI              |
| **Notifications**        | Discord only                              | Discord, Telegram, In-app dashboard (SMS soon?) |
| **Real-time Updates**    | None                                      | Yes, with Laravel Echo (upcoming)                |
| **Asset Detection**      | Basic scanning                            | Advanced monitoring with instant alerts          |
| **User Experience**      | Terminal-based, manual                    | Intuitive, no-refresh, mobile-responsive         |
| **Tech Stack**           | Python + Flask (lightweight but limited)  | Laravel 12 + Livewire 3 + Volt (robust & modern)|
| **Extensibility**        | Hard to add features                      | Easy scaling, plugins, and integrations          |
| **Deployment**           | Local scripts                             | Docker-ready, cloud-friendly                     |

v2 isn't just an update – it's a revolution for better monitoring!

## 📸 Screenshots (Coming Soon)

- Dashboard overview
- Notification settings
- Real-time alert demo

## 🗺️ Roadmap

- [ ] Integrate Laravel Echo for live broadcasting
- [ ] Add SMS notifications
- [ ] Enhance asset tracking with AI insights
- [ ] Mobile app companion (API endpoints ready)
- [ ] Full test suite and CI/CD
- [ ] Community contributions welcome!

## 🤝 Contributing

Love monitoring tools? Spot a bug or have an idea? Open an issue or PR – let's make Watch Tower even stronger together.

## 📄 License

MIT License – fork, modify, and use as you like (a star on the repo would be awesome 🌟)

---

Crafted with ❤️, ⚡, and endless curiosity.  
Last updated: February 2026
