# Watch Tower ⚡ <img src="https://laravel.com/img/logomark.min.svg" alt="Laravel" width="30" height="30" style="vertical-align: middle; margin-left: 10px;"> <img src="https://livewire.laravel.com/img/livewire-logo.svg" alt="Livewire" width="30" height="30" style="vertical-align: middle; margin-left: 5px;">

A sleek, modern web application for monitoring and notifications – powered by **Laravel 12**, **Livewire 3** + **Volt**.  
This is **Version 2** of the original [Bat-Tower](https://github.com/Arash-abraham/Bat-Tower), rebuilt from the ground up for better performance, usability, and features.  
Currently under active development – stay tuned for more!

> "Elevate your monitoring game: real-time insights, flexible notifications, and effortless scalability."

## Why Version 2? (Better Than Ever)

The original Bat-Tower (v1) was a Python + Flask CLI tool – efficient but limited: it ran in the terminal, detected new assets from targets, and only sent notifications to Discord.  

Now, **Watch Tower (v2)** transforms it into a full-fledged web app:  
- Choose your notification channels: Discord, Telegram, or both.  
- Real-time alerts right in the dashboard – no more waiting for external apps.  
- High chance of SMS integration soon for even broader reach.  
- Built with a reactive UI for seamless user experience.  

Upgrade to v2 for a more intuitive, extensible, and powerful monitoring solution!

## ✨ Key Features

- **Reactive Dashboard**: Live updates on new assets – powered by Livewire 3 and Volt's class-based components.  
- **Multi-Channel Notifications**: Send alerts to Discord, Telegram, or view them instantly in-app. (SMS coming soon?)  
- **Asset Monitoring**: Scan and detect new targets efficiently, with customizable rules.  
- **User Authentication**: Secure login with Laravel Breeze (or your preferred stack).  
- **Responsive Design**: Works beautifully on desktop, tablet, and mobile – with dark mode for late-night sessions.  
- **Real-Time Ready**: Integrating Laravel Echo for broadcast notifications and live events.  
- **Clean Architecture**: Single-file Volt components for rapid development and maintenance.  

## 🛠️ Tech Stack

- **Backend**: Laravel 12.x – robust, scalable, and developer-friendly.  
- **Frontend**: Livewire 3 + Volt – reactive components without the JavaScript fatigue.  
- **Styling**: Tailwind CSS v3 + your favorite UI kit (e.g., DaisyUI or Flowbite) for pixel-perfect interfaces.  
- **Database**: MySQL / PostgreSQL / SQLite – flexible storage options.  
- **Real-Time**: Laravel Echo (upcoming) for seamless broadcasts.  
- **Icons & Extras**: Heroicons or Lucide for crisp visuals; ready for expansions like Docker.  

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# 2. Install dependencies
composer install
npm install && npm run dev    # or use pnpm / yarn / bun

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

Head to http://localhost:8000 – start monitoring!

## 📸 Screenshots (Coming Soon)

- v1 CLI simplicity vs. v2's polished dashboard.  
- Real-time notification previews in action.

## 🗺️ Roadmap

- [ ] Full Laravel Echo integration for broadcast events.  
- [ ] SMS notifications via Twilio or similar.  
- [ ] Advanced asset scanning with AI enhancements.  
- [ ] Role-based access for teams.  
- [ ] Mobile app API endpoints.  
- [ ] Comprehensive testing suite.  
- [ ] Dockerized deployment for easy scaling.  

## 🤝 Contributing

Love Laravel and Livewire? Jump in! Open issues for bugs, suggestions, or PRs for features.  
Especially welcome: ideas to make notifications even smarter.

## 📄 License

MIT License – fork, modify, and build upon it freely (a star ⭐ would make my day!).

---

Crafted with ❤️, ⚡, and endless curiosity.  
Last updated: February 2026
