# Watch Tower ⚡ v2

**Modern, reactive dashboard & monitoring app**  
Built with **Laravel 12** + **Livewire 3** + **Volt**  

This is **version 2** — cleaner, faster, more elegant than the previous one.

[Previous version (v1)](https://github.com/Arash-abraham/Bat-Tower) → much simpler structure, fewer features, old-school Livewire components.

v2 brings a complete rethink with class-based Volt components, better organization, improved DX, and modern Laravel 12 goodies.

> "Watch everything that matters — beautifully, reactively, without the bloat."

## ✨ What's New & Better in v2

- Pure **class-based Volt components** (no more messy blade + @script mess)
- Laravel **12.x** — latest performance, type-hinting improvements, new packages ecosystem
- Full **Livewire 3** reactivity + Volt functional elegance
- Much cleaner architecture & naming conventions
- Tailwind CSS v4-ready styling (with your favorite UI kit: DaisyUI / Flowbite / etc.)
- Dark mode that actually looks premium
- Mobile-first responsive design from day one
- Prepared for real-time (Reverb + Echo integration planned)
- Better separation of concerns → easier to scale & maintain

## 🛠 Tech Stack (v2)

- **Backend** → Laravel 12.x
- **Frontend** → Livewire 3 + Volt (class-based)
- **Styling** → Tailwind CSS v3/v4 + component library of choice
- **Database** → MySQL / PostgreSQL / SQLite
- **Icons** → Heroicons / Lucide / Remix Icon
- **Future** → Laravel Reverb, Horizon, Telescope, Docker Compose

## 🚀 Quick Start (v2)

```bash
# Clone v2
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# Install everything
composer install
npm install && npm run dev

# Environment setup
cp .env.example .env
php artisan key:generate

# Database
php artisan migrate --seed   # if you have seeders

# Run (two terminals)
php artisan serve
npm run dev
```

Open http://localhost:8000 — welcome to v2 ✨

## 🗺 Roadmap (still cooking)

- Real-time notifications & live updates
- Advanced filtering & search
- Role-based access control
- API layer for future mobile/web apps
- PWA support
- Comprehensive test suite
- Docker + production deployment guide

## Why v2 > v1?

- Better developer experience (Volt classes >> old Livewire syntax)
- More maintainable code structure
- Leverages latest Laravel 12 features
- Prettier UI defaults
- Easier to extend & add features

v1 was a solid proof-of-concept — v2 is production-grade thinking.

## 🤝 Contributing

Love Volt? Hate messy code?  
Issues, PRs, ideas — all welcome.  
Let's make this even more beautiful together.

## 📄 License

MIT — free to use, fork, modify.  
A star would be awesome though 🌟

---

Made with ❤️ + Laravel 12 + Volt magic  
February 2026
