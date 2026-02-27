# Watch Tower ⚡ 

<grok-card data-id="b93528" data-type="image_card" data-plain-type="render_searched_image"  data-arg-size="LARGE" ></grok-card>

 

Elevate your monitoring game with **Watch Tower v2** – a sleek, real-time web application powered by **Laravel 12**, **Livewire 3**, and **Volt**.  
This is the evolved successor to [Bat-Tower v1](https://github.com/Arash-abraham/Bat-Tower), rebuilt from the ground up for superior performance, user-friendly interface, and expanded features. Say goodbye to command-line limitations and hello to a dynamic dashboard that keeps you informed effortlessly!

> "Watch smarter, not harder – real-time insights at your fingertips. 🚀"

## Why v2 is a Game-Changer

While v1 (built with Python and Flask) was a solid CLI tool limited to Discord notifications for new asset discoveries, v2 takes it to the next level:
- **Interactive Web Dashboard**: Monitor everything in a beautiful, responsive UI – no more terminal tinkering.
- **Multi-Channel Notifications**: Choose Discord, Telegram, or in-app dashboard alerts. SMS integration is highly likely in upcoming updates!
- **Real-Time Magic**: Powered by Laravel Echo for instant updates without refreshing.
- **Scalable & Modern**: Leveraging Laravel 12's latest features for robustness and speed.

## Comparison: v1 vs. v2

| Feature                  | Bat-Tower v1 (Python/Flask)                  | Watch Tower v2 (Laravel 12/Livewire/Volt)                  |
|--------------------------|----------------------------------------------|------------------------------------------------------------|
| **Interface**            | Command-Line Only (CLI)                      | Interactive Web Dashboard + CLI Options                    |
| **Notifications**        | Discord Only (for new assets)                | Discord, Telegram, In-Dashboard Real-Time; SMS Coming Soon |
| **Real-Time Updates**    | None – Manual Checks Required                | Yes, via Laravel Echo for Seamless Live Alerts             |
| **Tech Stack**           | Python + Flask (Backend-Focused)             | Laravel 12 + Livewire 3 + Volt (Full-Stack Elegance)       |
| **User Experience**      | Basic Terminal Output                        | Responsive UI, Dark Mode, Mobile-Friendly                  |
| **Extensibility**        | Limited to Scripts                           | Easy Integration with APIs, Databases, and More            |
| **Development Status**   | Stable but Static                            | Actively Evolving – Faster, Smarter, More Features         |

v2 isn't just an upgrade; it's a complete transformation – more intuitive, versatile, and future-proof!

## ✨ Key Features

- **Volt-Powered Components**: Class-based, single-file elegance for reactive UIs without the JavaScript hassle.
- **Livewire Reactivity**: Instant updates on asset discoveries – no page reloads needed.
- **Tailwind CSS Styling**: Clean, modern design with optional themes (e.g., DaisyUI for extra flair).
- **Authentication & Security**: Built-in with Laravel Breeze/Jetstream for safe access.
- **Responsive & Dark Mode**: Looks stunning on any device, day or night.
- **Upcoming: Laravel Echo Integration**: For even more powerful real-time broadcasting.

## 🛠️ Tech Stack

- **Backend**: Laravel 12.x – The PHP framework that's fast, secure, and developer-friendly.
- **Frontend**: Livewire 3 + Volt – Reactive components that feel like magic.
- **Styling**: Tailwind CSS v3 + Customizable UI Kits.
- **Database**: Flexible support for MySQL, PostgreSQL, or SQLite.
- **Real-Time**: Laravel Echo (in progress) for broadcast notifications.
- **Deployment**: Ready for Docker, with CI/CD pipelines on the horizon.

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# 2. Install dependencies
composer install
npm install && npm run dev  # Or use yarn/pnpm/bun

# 3. Set up environment
cp .env.example .env
php artisan key:generate

# 4. Run migrations (and seed if available)
php artisan migrate --seed

# 5. Launch the app
php artisan serve
# In a separate terminal:
npm run dev
```

Head to http://localhost:8000 and start watching!

## 📸 Screenshots (Coming Soon)

- v1: Simple CLI output.
- v2: Polished dashboard with real-time alerts.

## 🗺️ Roadmap

- [ ] Full Laravel Echo integration for broadcasts.
- [ ] SMS notifications via Twilio or similar.
- [ ] Advanced analytics and reporting.
- [ ] Mobile app companion (API-ready).
- [ ] Enhanced security audits.
- [ ] Community contributions welcome!

## 🤝 Contributing

Dive in! Open issues for bugs/ideas or submit PRs to make Watch Tower even better. Especially if you're a Laravel/Livewire enthusiast.

## 📄 License

MIT – Free to use, modify, and share (a star on the repo would make my day! 🌟)

---

Crafted with ❤️, ⚡, and endless curiosity.  
Last updated: February 2026
