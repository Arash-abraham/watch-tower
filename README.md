# Watch Tower v2 ⚡🔭

<div align="center">
  <img src="https://laravel.com/img/logotype.min.svg" width="180" alt="Laravel Logo">
  <br><br>
  <img src="https://livewire.laravel.com/img/logo.svg" width="140" alt="Livewire Logo">
  <br><br>
  <h3>A modern, reactive web dashboard built with Laravel 12 + Livewire 3 + Volt</h3>
  <p><strong>v2 is here – way better, prettier, and actually usable!</strong></p>
</div>

---

> From a simple Python + Flask CLI tool → to a beautiful, real-time web application  
> Watch Tower v2 is the complete glow-up.

## What's New in v2 (compared to v1)

| Feature                  | v1 (Python + Flask)          | v2 (Laravel 12 + Livewire + Volt)              |
|--------------------------|------------------------------|-------------------------------------------------|
| Interface                | Command-line only            | Modern SPA-like web UI, reactive & beautiful    |
| Real-time updates        | No                           | Yes – instant reactivity with Livewire          |
| Frontend framework       | None (just HTML?)            | Livewire 3 + Volt (class-based components)      |
| Styling                  | Basic / none                 | Tailwind CSS + modern component library         |
| Authentication           | Maybe basic                  | Built-in (Breeze/Jetstream or custom)           |
| Mobile / Responsive      | No                           | Yes – looks great on phone & tablet             |
| Dark mode                | No                           | Yes – automatic + toggle                        |
| Development speed        | Slow iterations              | Blazing fast with Volt & Laravel's ecosystem    |
| Future-proof             | Limited                      | Laravel 12 ecosystem + Reverb, Pulse, etc.      |

## ✨ Highlights of v2

- Laravel **12** – the latest & greatest
- **Volt** functional components – clean, elegant, powerful
- Full **Livewire 3** magic – zero JavaScript fatigue
- Tailwind + modern UI kit (DaisyUI / Flowbite / Shadcn-Laravel / ...)
- Beautiful dark mode by default
- Clean architecture with domain-driven structure
- Ready for real-time (Laravel Reverb / Echo planned)
- Much better DX – hot-reloading, auto-refresh, Volt dev tools

## 🚀 Get Started in 60 Seconds

```bash
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

composer install
npm install && npm run dev    # or pnpm install && pnpm dev

cp .env.example .env
php artisan key:generate
php artisan migrate --seed    # if you have seeders

# Run both in separate terminals
php artisan serve
npm run dev
```

→ Open http://localhost:8000

Welcome to the upgraded Watch Tower! 🌙✨

## 🗺️ What's Coming Next

- Real-time notifications & live updates
- Multi-user support + roles/permissions
- PWA + offline capabilities
- More Volt components & reusable blocks
- API layer for future mobile apps
- Better testing suite
- Docker + production deployment guides

## 🤝 Contributing & Feedback

Love Volt? Hate something? Found a bug?  
Issues, PRs, ideas – all welcome!

Star ⭐ if you're excited about v2!

## 📄 License

MIT – free to use, modify, enjoy.

---

Made with ❤️ Laravel 12 + Livewire + Volt + way too much coffee  
February 2026
