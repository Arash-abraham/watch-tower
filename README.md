# Watch Tower v2 ⚡🔭

<div align="center">
  <img src="https://laravel.com/img/logotype.min.svg" width="180" alt="Laravel">
  <img src="https://livewire.laravel.com/img/logo.svg" width="140" alt="Livewire">
  <img src="https://volt.laravel.com/images/volt-logo.svg" width="140" alt="Volt">
</div>

<br>

<div align="center">
  <h2>🚀 Watch Tower v2 – The Next Generation Alert System</h2>
  <p>
    <strong>From a simple Python CLI notifier → to a beautiful, real-time, multi-channel monitoring dashboard</strong>
  </p>
</div>

> Watch Tower v2 is the complete rewrite and evolution of the original Bat-Tower project.  
> Smarter. Faster. Prettier. And actually enjoyable to use.

## 🌟 What’s New in v2?

- Built with **Laravel 12** + **Livewire 3** + **Volt** (class-based functional components)
- Real-time notifications right in the dashboard (powered by **Laravel Echo** + Reverb coming soon)
- Multiple notification channels: **Discord**, **Telegram**, **In-app dashboard**, and **SMS** (very likely in near future)
- Beautiful, responsive UI with dark mode
- User-friendly target/asset management
- Much better performance, scalability and developer experience

## 📊 v1 vs v2 Comparison

| Feature                        | Bat-Tower v1 (Python + Flask)          | Watch Tower v2 (Laravel 12)                  |
|--------------------------------|----------------------------------------|----------------------------------------------|
| Interface                      | Only CLI                               | Modern web dashboard + real-time updates     |
| Notification Channels          | Discord only                           | Discord + Telegram + In-app + SMS (planned)  |
| Real-time in browser           | No                                     | Yes – with Laravel Echo                      |
| User management                | No                                     | Yes (multiple users, roles coming)           |
| Asset/target management        | Basic text files / config              | Elegant CRUD with Volt components            |
| UI/UX                          | Terminal only                          | Tailwind + dark mode + responsive design     |
| Framework                      | Python + Flask                         | Laravel 12 + Livewire 3 + Volt               |
| Real-time backend              | No                                     | Laravel Reverb + Echo (in progress)          |
| Mobile friendly                | No                                     | Yes                                          |
| Future extensibility           | Limited                                | Very high (API, PWA, more channels, etc.)    |
| Developer joy                  | 🤷‍♂️                                  | 🔥🔥🔥                                       |

## ✨ Current Features

- Live asset & target monitoring
- Instant in-dashboard notifications
- Telegram & Discord bot integration (choose per target)
- Clean Volt components & modern folder structure
- Authentication & user settings
- Responsive + dark mode out of the box
- Easy to extend (more channels, SMS gateway, etc.)

## 🛠 Tech Stack

- **Backend** → Laravel 12
- **Frontend** → Livewire 3 + Volt (functional class-based)
- **Real-time** → Laravel Echo + Reverb (coming very soon)
- **Styling** → Tailwind CSS v3 + daisyUI / shadcn (your choice)
- **Notifications** → Telegram Bot API + Discord Webhooks + In-app + (SMS planned)
- **Icons** → Heroicons / Lucide

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# Install
composer install
npm install && npm run dev

# Environment
cp .env.example .env
php artisan key:generate

# Migrate & seed (if needed)
php artisan migrate --seed

# Run
php artisan serve
# → and in another tab:
npm run dev
```

Open → http://localhost:8000

## 🗺️ Roadmap (v2.x)

- Laravel Reverb + Echo full real-time integration
- SMS notification channel (Twilio / Kavenegar / ...)
- PWA support
- Multi-user roles & permissions
- API for external integrations
- More beautiful UI polish & animations
- Tests (Pest + Dusk)
- Docker Compose ready for production

## 🤝 Contributing

Love real-time apps? Volt fan? Open issues/PRs are very welcome!  
Especially if you have ideas for new notification channels or UI improvements.

## 📄 License

MIT License

---

Made with ❤️ + Laravel 12 + insane amounts of coffee  
v2 – because v1 deserved a glow-up  
February 2026
