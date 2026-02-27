# Watch Tower v2 ⚡

<div align="center">
  <img src="https://download.logo.wine/logo/Laravel/Laravel-Logo.wine.png" alt="Laravel" width="80" style="vertical-align: middle; margin: 0 10px;">
  <span style="font-size: 2.5em; vertical-align: middle; color: #ff2d20;">+</span>
  <img src="https://picperf.io/https://laravelnews.s3.amazonaws.com/images/laravel-livewire.png" alt="Livewire" width="180" style="vertical-align: middle; margin: 0 10px;">
  <span style="font-size: 2.5em; vertical-align: middle; color: #007bff;">+</span>
  <img src="https://pbs.twimg.com/media/F1gZ_otWwAc9qGp.jpg" alt="Volt" width="80" style="vertical-align: middle; margin: 0 10px; border-radius: 12px;">
</div>

<br>

**Watch Tower v2** – A modern, reactive web application rebuilt from the ground up.

This is the **second major version** – completely rewritten in **Laravel 12** + **Livewire 3** + **Volt** for a dramatically better experience.

Previous version (v1): [Bat-Tower](https://github.com/Arash-abraham/Bat-Tower)  
→ Built with **Python + Flask**, **pure command-line interface** (no real UI, just terminal magic).

v2 brings a beautiful, interactive, real-time capable web UI while keeping the core idea alive.

> "From terminal to browser – faster, prettier, more powerful."

## ✨ Why v2 is way better

- Full modern web interface (no more staring at terminal output)
- Instant reactivity with Livewire 3 & Volt functional components
- Elegant single-file components (logic + view together)
- Stunning Tailwind + modern component library look
- Built on **Laravel 12** – latest features, better performance
- Dark mode, responsive, mobile-friendly from day one
- Ready for real-time (Reverb, Echo, notifications...)
- Much cleaner code structure & easier to extend

## 🛠 Tech Stack (v2)

- **Backend** → Laravel 12.x
- **Frontend Magic** → Livewire 3 + **Volt** (functional/class-based components)
- **Styling** → Tailwind CSS v3 + (DaisyUI / Flowbite / custom components)
- **Database** → MySQL / PostgreSQL / SQLite
- **Icons** → Heroicons / Lucide
- **Future** → Laravel Reverb, PWA support, Docker

## 🚀 Quick Start

```bash
# Clone & enter
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# Install PHP deps
composer install

# Install frontend deps
npm install && npm run dev    # or pnpm install && pnpm dev

# Environment setup
cp .env.example .env
php artisan key:generate

# Database
php artisan migrate --seed    # if you have seeders

# Run (two terminals)
php artisan serve
# second terminal:
npm run dev
```

Open → http://localhost:8000  
Enjoy the glow-up! ✨

## 🗺 Roadmap (v2 & beyond)

- [ ] More Volt functional components & cleanup
- [ ] Real-time updates with Reverb + Echo
- [ ] User roles, permissions, multi-tenancy
- [ ] Advanced search & filtering
- [ ] Export / import features
- [ ] API layer for future mobile apps
- [ ] Comprehensive test suite
- [ ] Docker Compose + production deployment guide

## 🤝 Contributing

Love reactive UIs? Found a bug? Have a crazy idea?  
Issues, PRs, discussions – all welcome!

Stars are very appreciated 🌟

## 📄 License

MIT License – free to use, modify, enjoy.

---

Made with ❤️, Laravel 12, Livewire 3, Volt & endless ☕  
February 2026
