# Watch Tower v2 ⚡👀

<div align="center">
  <img src="https://laravel.com/img/logotype.min.svg" width="180" alt="Laravel"> 
  <span style="font-size: 3rem; margin: 0 1rem;">+</span>
  <img src="https://livewire.laravel.com/img/logo.svg" width="180" alt="Livewire"> 
  <span style="font-size: 3rem; margin: 0 1rem;">+</span>
  <img src="https://volt.laravel.com/images/volt-logo.svg" width="140" alt="Volt">
</div>

<br>

<div align="center">
  <h3>The next generation of asset & target monitoring</h3>
  <p><strong>v2 is here</strong> — faster, prettier, more channels, real dashboard</p>
</div>

<br>

<p align="center">
  <a href="https://github.com/Arash-abraham/watch-tower/releases">
    <img src="https://img.shields.io/github/v/release/Arash-abraham/watch-tower?style=for-the-badge&color=ef4444&logo=laravel&logoColor=white" alt="Latest Release">
  </a>
  <a href="https://github.com/Arash-abraham/watch-tower/stargazers">
    <img src="https://img.shields.io/github/stars/Arash-abraham/watch-tower?style=for-the-badge&color=yellow" alt="Stars">
  </a>
  <img src="https://img.shields.io/badge/Laravel-12.x-ff2d20?style=for-the-badge&logo=laravel&logoColor=white" alt="Laravel 12">
  <img src="https://img.shields.io/badge/Livewire-3.x-4f46e5?style=for-the-badge&logo=livewire&logoColor=white" alt="Livewire 3">
  <img src="https://img.shields.io/badge/Volt-%E2%9A%A1-6366f1?style=for-the-badge" alt="Volt">
</p>

<br>

### What’s new in v2 (compared to v1)

| Feature                          | Watch Tower v1 (Python + Flask)     | Watch Tower v2 (Laravel + Livewire + Volt)              |
|----------------------------------|--------------------------------------|-----------------------------------------------------------|
| Interface                        | Only CLI                            | Beautiful real-time dashboard + CLI support              |
| Notification channels            | Discord only                        | Discord + Telegram + In-app dashboard notifications      |
| SMS support                      | No                                  | Very likely coming soon                                  |
| Real-time updates                | No (polling or manual refresh)      | Full reactive UI with Livewire                           |
| Asset / target discovery         | Basic                               | Smarter detection + richer metadata                      |
| Tech stack                       | Python + Flask + Requests           | Laravel 12 + Livewire 3 + Volt + Tailwind                |
| Development speed & maintainability | Moderate                          | Much faster iteration & cleaner code                     |
| Mobile friendliness              | None                                | Responsive design + dark mode                            |

**v1 was a proof-of-concept CLI tool. v2 is the real product.**

<br>

### ✨ Core Features

- Real-time dashboard with Livewire reactivity
- Instant in-app notifications when new assets/targets are discovered
- Multiple notification channels:
  - Discord webhook
  - Telegram bot
  - Browser/in-app toast notifications
- Upcoming: SMS gateway integration
- Clean Volt class-based components
- Tailwind + modern UI components
- Dark / light mode toggle
- Easy target & asset management
- History & logs viewer
- Secure authentication

<br>

### 🚀 Quick Start

```bash
# Clone & enter directory
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# Install PHP & JS dependencies
composer install
npm install && npm run dev    # or pnpm install && pnpm dev

# Environment setup
cp .env.example .env
php artisan key:generate

# Database & migrations
php artisan migrate --seed    # optional seed for demo data

# Run (two terminals)
php artisan serve
npm run dev
```

→ Open http://localhost:8000

<br>

### 🗺️ Roadmap (short-term)

- [ ] SMS notifications (Twilio / Kavenegar / ... integration)
- [ ] Advanced filtering & search on dashboard
- [ ] Export reports (CSV / PDF)
- [ ] Multi-user & team support
- [ ] Docker compose ready for production
- [ ] Unit + feature tests coverage ↑
- [ ] Reverb / Echo for even faster real-time

<br>

### 🤝 Contributing & Feedback

PRs, issues, feature requests, bug reports — all welcome.  
Especially if you have ideas about better UX or new notification channels.

<br>

<div align="center">
  Made with ❤️ + Laravel 12 + Livewire + Volt + lots of ☕  
  <br><br>
  <strong>Enjoy watching your targets! 👀</strong>
</div>
