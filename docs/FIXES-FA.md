# چه چیزی در این پاس درست شد

> تاریخ: ۲۰۲۶-۱۰-۳۱ · شاخه: `arena/dd3d9033-watch-tower`
> این فایل مکمل [`PROJECT-REVIEW-FA.md`](PROJECT-REVIEW-FA.md) است؛ آن سند وضعیت **قبل از اصلاحات** را ثبت می‌کند.

## ۱. اتصال سه لایه به هم (مهم‌ترین بخش)

قبلاً سه پروژه‌ی مستقل بودند بدون هیچ ارتباطی. حالا یک مسیر کامل و قابل اجرا وجود دارد:

```
منابع عمومی (Bugcrowd / HackerOne / YesWeHack / Intigriti)
        │
        ▼
Python collector  ──►  MongoDB  ──►  Laravel API  ──►  Vue dashboard
(normalise + diff +    (programs,     (/api/v2.1/*)     (بدون داده‌ی
 notify + schedule)     changes,                          هاردکد)
                        sync_runs)
```

- کالکتور، scope هر برنامه را استخراج و با اجرای قبلی مقایسه می‌کند و برای هر تغییر یک سند در `changes` می‌نویسد.
- API همان کالکشن‌ها را می‌خواند (مدل‌های `Program`، `Change`، `SyncRun`، `Subdomain`).
- داشبورد همه‌ی اعداد و لیست‌ها را از API می‌گیرد.

## ۲. هسته‌ی پایتون (بازنویسی)

| قبل | بعد |
|---|---|
| فقط Bugcrowd، چاپ در ترمینال | چهار منبع + محلی، نرمال‌سازی یکسان (`core/normalizer.py`) |
| `input()` تعاملی در مسیر خودکار | حذف شد؛ بدون prompt |
| بدون تاریخچه‌ی تغییرات | کالکشن `changes` با نوع، هدف، زمان و وضعیت ارسال |
| بدون نوتیفیکیشن | Telegram + Discord با پیام‌های گروه‌بندی‌شده و chunk شده |
| بدون زمان‌بندی | `monitor.py --watch --interval` |
| خطای تضاد scope باعث رد شدن برنامه می‌شد | تضاد ثبت و گزارش می‌شود، داده حفظ می‌شود |
| `reset_db.py` خراب (ایمپورت‌های SQLAlchemy) | بازنویسی برای Mongo با `--yes` |
| `app.py` دموی echo با `debug=True` | سرویس سلامت `/health` و `/status` بدون ورودی کاربر |
| پورت پیش‌فرض ۳۳۰۶ (MySQL) | ۲۷۰۱۷ (MongoDB) + پشتیبانی از `MONGO_URI` |

## ۳. API لاراول

- `SubdomainsController` که وجود نداشت اضافه شد (روت قبلی کرش می‌کرد).
- `ProgramsController` از صفر پیاده شد: لیست با فیلتر/جست‌وجو/صفحه‌بندی، جزئیات، ایجاد/ویرایش/حذف برنامه‌های محلی.
- `ChangesController` (فید آلرت + شمارنده‌ها)، `StatsController` (آمار و منابع)، `HealthController`.
- مدل `Program` حالا واقعاً به اتصال `mongodb` وصل است (`$connection`, `$collection`, casts, fillable).
- migrationها بازنویسی شدند و ایندکس‌ها با نام‌های پیش‌فرض Mongo ساخته می‌شوند تا با ایندکس‌های پایتون تضاد نکنند.
- `config/cors.php` اضافه شد؛ `throttle:120,1` روی API.
- `.env.example` از MySQL به Mongo تغییر کرد؛ `SESSION/CACHE/QUEUE` به file/sync تغییر کردند تا `migrate` بدون جدول SQL کار کند.
- `config/watchtower.php` برای فهرست منابع و فاصله‌ی اسکن.

## ۴. داشبورد Vue

- لایه‌ی `src/services/api.js` + composable `useApi` (loading/error/polling).
- حذف کامل داده‌های هاردکد: داشبورد، Targets، Alerts، Applications و Monitors همه از API می‌خوانند.
- حالت‌های loading / error / empty واقعی (`AsyncState`).
- صفحه‌ی Settings واقعی (وضعیت اتصال، کانال‌های نوتیفیکیشن).
- رفع باگ‌های UI: دکمه‌ی Documentation حالا مودال را باز می‌کند، لینک GitHub درست شد، آمار جعلی حذف شد.
- `vite.config.js`: پروکسی `/api` و `allowedHosts` برای محیط پیش‌نمایش.

## ۵. زیرساخت و بهداشت ریپو

- `package-lock.json`های ویو و لاراول از نو با `registry.npmjs.org` ساخته شدند (قبلاً ۳۱۴ آدرس به `package-mirror.liara.ir` قفل بود).
- `composer.lock`: ۱۲۰ آدرس `mirror-composer.runflare.com` به `codeload.github.com` تبدیل شد.
- `docker-compose.yml` بازنویسی شد: `mongo:7` رسمی + چهار سرویس با healthcheck و Dockerfile.
- `.gitignore` ریشه از نو نوشته شد (نشانگرهای merge حذف شدند).
- فایل‌های `__pycache__/*.pyc` از مخزن خارج شدند.
- `LICENSE` (MIT)، `.github/workflows/ci.yml` (تست پایتون، بیلد ویو، lint لاراول) اضافه شد.
- README از ادعاهای پیاده‌نشده پاک شد و راهنمای اجرای واقعی دارد؛ `docs/API.md` مرجع API است.

## ۶. تست‌ها و اعتبارسنجی انجام‌شده

- `python -m unittest discover -s tests` → **۳۰ تست سبز** (diff، نرمال‌سازی چهار منبع، sync با mongomock).
- اجرای واقعی کالکتور روی داده‌ی کامل چهار منبع (۹۴۷ برنامه، ۴۸٬۴۰۰ دارایی) با mongomock؛ سپس شبیه‌سازی یک delta و تأیید تولید `scope_added` / `out_scope_added` / `program_removed`.
- `npm run build` → بیلد موفق Vite.
- تست مقاوم‌سازی: خطای شبکه در کالکتور حالا ثبت می‌شود و حلقه را نمی‌ترکاند.
- پارس همه‌ی ۴۷ فایل PHP با پارسر PHP 8 (`php-parser`) → بدون خطای سینتکس.
  (اجرای واقعی Laravel در این محیط ممکن نبود چون PHP/MongoDB/Composer نصب نیستند.)

## ۷. چیزهایی که هنوز مانده

- اجرای `composer install` و `php artisan migrate` روی سیستم شما (اولین بار) تا مسیر API واقعاً بوت شود.
- احراز هویت/چندکاربری (token/Sanctum) — فعلاً API عمومی است.
- شمارش ساب‌دامین و مانیتور کشف دارایی — فقط کالکشن و API آماده است.
- تست‌های Feature برای API (نیازمند Mongo در CI).
