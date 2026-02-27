<p align="center">
  <img src="https://via.placeholder.com/120x120/6366f1/ffffff?text=WT" alt="Watch Tower Logo" width="120">
  <h1 align="center">Watch Tower ⚡ v2</h1>
  <p align="center">
    <i>A modern recon & monitoring dashboard built with Laravel + Livewire Volt</i><br>
    <strong>Successor to <a href="https://github.com/Arash-abraham/Bat-Tower">Bat-Tower</a></strong>
  </p>

  <p align="center">
    <a href="https://github.com/Arash-abraham/watch-tower/stargazers"><img src="https://img.shields.io/github/stars/Arash-abraham/watch-tower?style=social" alt="Stars"></a>
    <a href="https://github.com/Arash-abraham/watch-tower/forks"><img src="https://img.shields.io/github/forks/Arash-abraham/watch-tower?style=social" alt="Forks"></a>
    <img src="https://img.shields.io/badge/Laravel-12.x-red?style=flat&logo=laravel&logoColor=white" alt="Laravel">
    <img src="https://img.shields.io/badge/Livewire-3.x-4f46e5?style=flat&logo=livewire" alt="Livewire">
    <img src="https://img.shields.io/badge/Volt-%E2%9A%A1-blueviolet?style=flat" alt="Volt">
    <img src="https://img.shields.io/badge/Status-In%20Development-yellow?style=flat" alt="In Development">
  </p>
</p>

---

### ✨ What is Watch Tower?

Watch Tower is the **next evolution** of [Bat-Tower](https://github.com/Arash-abraham/Bat-Tower) — a powerful reconnaissance and asset monitoring tool, now rebuilt as a beautiful **web dashboard**.

Instead of scattered Python scripts and terminal outputs, you now get:

- Real-time monitoring interface  
- Interactive sub-domain & certificate views  
- Discord / Slack / Email notifications (coming soon)  
- Clean, reactive UI powered by **Laravel Volt + Livewire 3**

Perfect for bug bounty hunters, security researchers, and anyone who wants to keep an eye on their attack surface — without leaving the browser.

---

### 🛠 Tech Stack (The Dream Team)

| Layer          | Technology                  | Why we love it                     |
|----------------|-----------------------------|-------------------------------------|
| Backend        | Laravel 12.x                | Elegant, batteries-included         |
| Frontend       | Livewire 3 + **Volt**       | Reactivity without leaving PHP      |
| Styling        | Tailwind CSS + DaisyUI / MaryUI | Fast & beautiful components         |
| Database       | MySQL / PostgreSQL          | Reliable & scalable                 |
| Realtime       | Laravel Echo + Pusher       | (planned) live updates              |
| Notifications  | Discord Webhooks            | Instant alerts                      |

---

### 🚧 Current Status — In Active Development

✅ Project skeleton & authentication  
✅ Basic dashboard layout (Volt components)  
✅ Sub-domain & certificate data models  
✅ Import from Bat-Tower outputs  

🛠 Coming very soon:  
- Live table views & search  
- Chart visualizations (sub-domain growth, cert expiry)  
- One-click sync from external tools (subfinder, crt.sh, etc.)  
- Dark mode & responsive design polish  
- Export / report generation  

---

### 🏃 Quick Start (When it's ready)

```bash
# 1. Clone & enter
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# 2. Install dependencies
composer install
npm install && npm run dev

# 3. Setup environment
cp .env.example .env
php artisan key:generate

# 4. Run migrations & seed (if any)
php artisan migrate --seed

# 5. Start everything
php artisan serve
# in another terminal:
npm run dev
