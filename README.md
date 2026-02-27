# Watch Tower v2 ⚡❤️

![Laravel](https://img.shields.io/badge/Laravel-FF2D20?style=flat&logo=laravel&logoColor=white) ![Livewire](https://img.shields.io/badge/Livewire-4e56a6?style=flat&logo=livewire&logoColor=white)

A sleek, modern web application for monitoring targets and assets – built with **Laravel 12**, **Livewire 3** + **Volt**.  
This is the upgraded v2 of [Bat-Tower (v1)](https://github.com/Arash-abraham/Bat-Tower), now with a full web dashboard, multi-channel notifications, and real-time updates on the horizon. Say goodbye to command-line only – v2 is faster, more intuitive, and way more powerful!

> "Eyes on the horizon: Detect new assets instantly, notify smarter."

## Why v2 is Better Than v1
v1 (Bat-Tower) was a solid Python/Flask CLI tool that sent Discord notifications for new assets. But v2 takes it to the next level:  
- Interactive web dashboard for real-time monitoring.  
- Flexible notifications: Choose Discord, Telegram, or in-app alerts – with SMS support likely coming soon.  
- Reactive UI powered by Livewire + Volt for seamless experiences.  
- Scalable backend with Laravel 12 for better performance and extensibility.

## ✨ Key Features

- **Real-time Asset Detection**: Instant alerts when new assets from targets are found.
- **Multi-Channel Notifications**: Discord, Telegram, in-dashboard popups – and potential SMS integration.
- **Class-Based Volt Components**: Elegant, single-file reactive components for a clean codebase.
- **Full Livewire Reactivity**: No page reloads – everything updates dynamically.
- **Tailwind CSS Styling**: Responsive, mobile-friendly design with dark mode support.
- **Authentication & Security**: Built-in user management for secure access.
- **Upcoming Real-Time Magic**: Laravel Echo integration for live broadcasting.

## 🛠️ Tech Stack

- **Backend**: Laravel 12.x (PHP 8+)
- **Frontend**: Livewire 3 + Volt (class-based components)
- **Styling**: Tailwind CSS v3 + modern UI components
- **Database**: MySQL / PostgreSQL / SQLite
- **Real-Time (Soon)**: Laravel Echo + Reverb
- **Notifications**: Integrated with Discord, Telegram APIs – extensible for more

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# 2. Install dependencies
composer install
npm install && npm run dev  # or yarn / pnpm / bun

# 3. Setup environment
cp .env.example .env
php artisan key:generate

# 4. Run migrations & seed
php artisan migrate --seed

# 5. Launch
php artisan serve
# In another terminal:
npm run dev
```

Head to http://localhost:8000 – start monitoring!

## 📊 v1 vs v2 Comparison

| Feature                  | v1 (Bat-Tower)                  | v2 (Watch-Tower)                          |
|--------------------------|---------------------------------|-------------------------------------------|
| **Interface**            | Command-Line Only               | Interactive Web Dashboard                 |
| **Language/Framework**   | Python + Flask                  | PHP + Laravel 12                          |
| **Notifications**        | Discord Only                    | Discord, Telegram, In-Dashboard (SMS soon)|
| **Real-Time Updates**    | None                            | Livewire Reactivity + Laravel Echo (WIP)  |
| **UI/UX**                | Text-Based                      | Responsive, Dark Mode, Mobile-Friendly    |
| **Extensibility**        | Limited (CLI Scripts)           | Full Web App with APIs & Components       |
| **Deployment**           | Simple Scripts                  | Docker-Ready + CI/CD Pipeline (Coming)    |

v2 is designed for ease, scalability, and user-friendliness – perfect for developers and teams.

## 🗺️ Roadmap

- [ ] Integrate Laravel Echo for true real-time notifications.
- [ ] Add SMS support via Twilio or similar.
- [ ] Enhance dashboard with charts and analytics.
- [ ] API for mobile integrations.
- [ ] More tests and optimizations.

## 🤝 Contributing

Love monitoring tools? Open issues, submit PRs, or share ideas – especially for Volt/Livewire tweaks!

## 📄 License

MIT – Fork, modify, and star if it helps! 🌟

---

Crafted with ❤️⚡ + endless curiosity  
Updated: February 2026
