<div align="center">

  <img src="https://laravel.com/img/logotype.min.svg" alt="Laravel" width="120">
  <h1>Watch Tower ⚡</h1>

  <p>
    <strong>A clean, modern Laravel project powered by Livewire 3 + Volt</strong><br>
    Building something useful, one functional component at a time.
  </p>

  <p>
    <a href="https://laravel.com"><img src="https://img.shields.io/badge/Laravel-12.x-ff2d20?style=for-the-badge&logo=laravel&logoColor=white" alt="Laravel"></a>
    <a href="https://livewire.laravel.com"><img src="https://img.shields.io/badge/Livewire-v3-4f46e5?style=for-the-badge&logo=livewire&logoColor=white" alt="Livewire"></a>
    <a href="https://livewire.laravel.com/docs/volt"><img src="https://img.shields.io/badge/Volt-%E2%9A%A1-blueviolet?style=for-the-badge" alt="Volt"></a>
  </p>

  <p>
    <em>Under active development → expect magic ✨ soon</em>
  </p>

</div>

<br>

## ✨ What's this project?

Just a fresh Laravel application that's being shaped with:

- **Livewire 3** + **Volt** → single-file components that feel like magic
- Functional components (no more huge class files)
- Tailwind CSS (of course)
- Clean folder structure & modern practices

Currently building [your main idea – e.g. a real-time dashboard / task manager / monitoring tool / whatever it is].  
More features coming every week.

<br>

## 🚀 Quick Start

```bash
# 1. Clone & go inside
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# 2. Install dependencies
composer install
npm install && npm run dev    # or pnpm / yarn

# 3. Setup environment
cp .env.example .env
php artisan key:generate

# 4. Database (sqlite for quick testing)
touch database/database.sqlite
php artisan migrate --seed

# 5. Run it!
php artisan serve
# open http://127.0.0.1:8000
