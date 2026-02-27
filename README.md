# Watch Tower - Laravel Livewire Wallet

A simple digital wallet system built with **Laravel** + **Livewire** (v3).

> **Status:** In active development – not production-ready yet

Personal finance / virtual wallet project for learning & experimenting.

## Current Features (so far)

- User authentication (register/login)
- Wallet balance display (real-time with Livewire)
- Deposit money (manual for now)
- Withdraw money with simple validation
- Basic transaction history list
- Responsive layout (Tailwind + some custom CSS)

## Planned / Coming Soon

- Multiple wallets per user
- Transaction categories & search/filter
- Export transactions (CSV/PDF)
- Email notifications
- Better security (2FA, rate limiting)
- Dark mode toggle
- Mobile-friendly improvements

## Tech Stack

- Laravel 11 / 12 (depending on when you read this)
- Livewire 3.x
- Alpine.js
- Tailwind CSS
- MySQL / SQLite (for local dev)
- Laravel Breeze or custom auth

## Installation (local development)

```bash
# 1. Clone the repo
git clone https://github.com/Arash-abraham/watch-tower.git
cd watch-tower

# 2. Install dependencies
composer install
npm install && npm run dev    # or npm run build

# 3. Copy env file
cp .env.example .env

# 4. Generate app key
php artisan key:generate

# 5. Setup database
php artisan migrate --seed   # optional: seeds some test data

# 6. Run the app
php artisan serve
# or better: php artisan livewire:serve (if you like hot-reload)
