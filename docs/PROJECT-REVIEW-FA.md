> ⚠️ **این سند وضعیت پروژه را *قبل از* اصلاحات توصیف می‌کند.**
> برای فهرست کارهایی که انجام و درست شد، [`FIXES-FA.md`](FIXES-FA.md) را ببینید.

# بررسی کامل پروژه Watch Tower

> تاریخ بررسی: ۲۰۲۶-۱۰-۳۱ · شاخه: `arena/dd3d9033-watch-tower` · کامیت مبنا: `1536543`
> روش بررسی: خواندن کامل کد، تحلیل وابستگی‌ها، بیلد واقعی فرانت‌اند، و اجرای UI

---

## ۱. در یک نگاه

| مورد | مقدار |
|---|---|
| نام | Watch Tower |
| توضیح رسمی ریپو | «If you are a bug hunter who needs a complete watchtower, this program can meet your needs.» |
| ماهیت | پلتفرم رصد لحظه‌ای «دارایی‌ها» (Asset Monitoring) برای باگ‌هانترها و تیم‌های امنیت |
| اجزا | Python Core + Laravel Core + Vue.js Core (سه پروژه جدا در یک ریپو) |
| حجم کد | ≈ ۳٬۵۵۰ خط مؤثر (Python ≈ ۳۵۰ · Laravel ≈ ۱٬۴۳۶ · Vue ≈ ۱٬۷۶۱) |
| ستاره / فورک | ۶ / ۰ |
| ایجاد / آخرین پوش | ۲۰۲۶-۰۵-۰۸ / ۲۰۲۶-۱۰-۳۰ |
| لایسنس | ❌ ندارد (عملاً «همه حقوق محفوظ») |
| Issues | غیرفعال |
| CI / تست | ❌ ندارد (فقط دو تست نمونه‌ی پیش‌فرض لاراول) |
| وضعیت واقعی | نمونه‌ی اولیه‌ی (prototype) جاه‌طلبانه؛ **حدود ۲۵–۳۰٪ راه تا یک محصول قابل استفاده** |

---

## ۲. این پروژه چیست؟

ایده‌ی محوری ساده و درست است:

> «به‌جای اینکه هر روز دستی چک کنی کدام برنامه‌ی باگ‌بانتی دامنه‌ی جدیدی به scope اضافه کرده، یک سرویس این کار را خودکار انجام بدهد و بهت خبر بدهد.»

Watch Tower قرار است:

1. لیست برنامه‌های باگ‌بانتی (در نسخه‌ی فعلی: فقط Bugcrowd) را از یک منبع عمومی بگیرد؛
2. scope / out-of-scope هر برنامه را در دیتابیس نگه دارد؛
3. در هر اجرا، لیست جدید را با قبلی مقایسه کند و «اضافه/حذف شده‌ها» را تشخیص بدهد؛
4. (در آینده) این تغییرات را real-time به داشبورد و کانال‌های Discord/Telegram بفرستد.

نسخه‌ی اول پروژه (که در `img/old-version.jpg` هم دیده می‌شود) یک اسکریپت پایتون + نوتیفیکیشن Discord بوده. نسخه‌ی فعلی تلاش می‌کند همان ایده را به یک پلتفرم سه‌لایه با داشبورد و multi-user تبدیل کند.

---

## ۳. به چه دردی می‌خورد؟ (کاربرد واقعی)

### ۳.۱ برای باگ‌هانتر (کاربرد اصلی و ارزشمندترین بخش)

در باگ‌بانتی، «سرعت» پول است. وقتی یک برنامه دامنه‌ی جدیدی به scope اضافه می‌کند، معمولاً چند ساعت اول رقابت کم است. ابزاری که این تغییر را در همان دقیقه به تو بگوید، مستقیماً روی درآمد اثر دارد.
همین کار امروز به‌صورت دستی با اسکریپت + `diff` + بات تلگرام انجام می‌شود؛ Watch Tower می‌خواهد این را محصول‌محور کند.

### ۳.۲ برای تیم امنیت / مدیریت Attack Surface

رصد «دارایی‌های جدید» سازمان خودت (ساب‌دامین تازه، سرویس جدید، تغییر DNS). این بخشِ محصول هنوز **پیاده‌سازی نشده**، ولی معماری برای آن در نظر گرفته شده (کالکشن `subdomains`، روت `subdomains`).

### ۳.۳ برای DevSecOps

هشدار خودکار وقتی سطح حمله تغییر می‌کند، به‌جای اسکن دوره‌ای و گزارش‌های PDF که کسی نمی‌خواند.

### ۳.۴ ارزش تجاری (چشم‌انداز README)

SaaS چندمستأجری با workspace مشترک، API و تحلیل. این هدف قابل دفاع است، اما فاصله‌ی زیادی تا آن وجود دارد.

### ۳.۵ این پروژه چه چیزی **نیست**

- اسکنر آسیب‌پذیری نیست (و همین خوب است؛ از نظر حقوقی هم امن‌تر).
- ابزار پیدا کردن ساب‌دامین (subdomain enumeration) نیست؛ فعلاً فقط scope عمومی برنامه‌ها را می‌خواند.
- جایگزین HackerOne/Bugcrowd نیست؛ لایه‌ی «رصد» روی داده‌ی عمومی آن‌هاست.

> نکته‌ی حقوقی: تا وقتی فقط داده‌ی عمومی scope را می‌خواند، ریسک پایین است. اگر بعداً enumeration/اسکن اضافه شود، باید به مجوز برنامه و محدوده‌ی scope پایبند باشد.

---

## ۴. معماری و جریان داده

```
        arkadiyt/bounty-targets-data  (JSON عمومی، تقریباً ساعتی آپدیت می‌شود)
                        │
                        ▼
      Watch-Tower-Python-Core  ──────────────►  MongoDB  (watch-tower)
      • watch_find_programs.py  (fetch)           ├─ bugcrowd_programs
      • watch_sync_programs.py  (JSON محلی)       └─ programs
      • db.py (upsert + diff + گزارش تغییرات)
                        │
                        │  (فعلاً هیچ ارتباطی وجود ندارد!)
                        ▼
      Watch-Tower-Laravel-Core  (API v2.1 + Sanctum + Swagger + Mongo driver)
                        │
                        │  (فعلاً fetch/axios/Echo وجود ندارد)
                        ▼
      Watch-Tower-Vue-Js-Core  (داشبورد سایبرپانک، داده‌ی هاردکد)
```

**مهم‌ترین شکاف معماری:** سه لایه به هم وصل نیستند. پایتون داده را در Mongo می‌نویسد، لاراول قرار است همان را سرو کند، ویو قرار است همان را نشان دهد — اما در کد فعلی هیچ‌کدام از این دو پل وجود ندارد.

---

## ۵. کد به کد: چه چیزی واقعاً وجود دارد

### ۵.۱ پایتون (تنها بخشی که واقعاً کار می‌کند)

| فایل | وضعیت |
|---|---|
| `bounty-programs/watch_find_programs.py` | ✅ کار می‌کند: دانلود `bugcrowd_data.json` از `arkadiyt/bounty-targets-data` (ریپوی زنده، ۳٫۹k ستاره، آخرین پوش ۲۰۲۶-۱۰-۳۱) |
| `database/db.py` → `insert_all_bugcrowd_programs` | ✅ منطق درست upsert + شمارش insert/update |
| `database/db.py` → `upsert_program` | ✅ منطق خوب: تشخیص تضاد scope و out-of-scope، محاسبه‌ی added/removed و چاپ diff |
| `programs/watch_sync_programs.py` | ✅ اسکن `WATCH_DIR/programs/*.json` و upsert |
| `database/reset_db.py` | ❌ **شکسته**: `from db import engine, Base` باقی‌مانده‌ی نسخه‌ی SQLAlchemy است؛ در نسخه‌ی Mongo وجود ندارد → ImportError |
| `app.py` | ⚠️ فقط یک دموی Flask با روت `/home-test` که ورودی کاربر را echo می‌کند و `debug=True` دارد؛ بخشی از محصول نیست و اگر عمومی اجرا شود، بازتاب HTML خام = XSS + debug console |
| `config.py` | ⚠️ `DB_PORT` پیش‌فرض `3306` (MySQL) در حالی که داکر Mongo روی `27017` است |
| `programs/benz.json` | ⚠️ کلید اشتباه: `"ooscope"` به‌جای `outScopes` → out-of-scope این برنامه همیشه خالی خوانده می‌شود |
| `programs/test.json` | ℹ️ عمداً تضاد دارد تا رفتار «CONFLICT» نمایش داده شود |

**چیزهایی که در پایتون وجود ندارد (با اینکه README وعده داده):**
- هیچ کد ارسال نوتیفیکیشن (Discord/Telegram) نیست — «چاپ در ترمینال» تنها خروجی است.
- هیچ scheduler/cron نیست؛ تغییرات فقط وقتی دیده می‌شوند که دستی اسکریپت را اجرا کنی.
- منبع HackerOne / YesWeHack / Federacy استفاده نشده (فقط Bugcrowd).
- هیچ مدل داده‌ی «alert» یا «event» ساخته نمی‌شود؛ diff فقط چاپ و دور ریخته می‌شود.

### ۵.۲ لاراول (اسکلت خام)

- نسخه‌ها: Laravel **13.9**، Sanctum 4، `mongodb/laravel-mongodb` 5.8، l5-swagger 11.
- `routes/api.php` → `api/v2.1/programs` و `api/v2.1/subdomains`
  - ❌ `SubdomainsController` **اصلاً وجود ندارد** → هر درخواست به این روت خطای Class not found می‌دهد.
  - ❌ `ProgramsController` تمام متدهایش خالی است (`//`) → پاسخ خالی/`null`.
- `app/Models/Program.php` خالی است: نه `$connection = 'mongodb'`، نه `$fillable` → اگر استفاده شود، روی اتصال پیش‌فرض (MySQL) می‌رود و جدول ندارد.
- تنها migration، `Schema::connection('mongodb')->create('programs', ...)` است؛ ولی خودِ راننده‌ی migration روی اتصال پیش‌فرض کار می‌کند → برای `php artisan migrate` هم MySQL لازم است هم Mongo.
- `.env.example` عملاً پیش‌فرض لاراول است: `DB_CONNECTION=mysql`، هیچ `DB_URI`/متغیر Mongo ندارد، ولی `config/database.php` انتظار `DB_URI` دارد (با `'options' => ['database' => 'admin']` که مشکوک/اشتباه است).
- `SESSION_DRIVER=database`، `QUEUE_CONNECTION=database`، `CACHE_STORE=database` — اما هیچ جدول sessions/cache/jobs ساخته نمی‌شود → اجرای پیش‌فرض خطا می‌دهد.
- بدون `config/cors.php` → فرانت روی پورت دیگر نمی‌تواند API را صدا بزند (حتی اگر API پیاده شده باشد).
- بدون احراز هویت روی `v2.1` (فقط `/api/user` سنکتوم دارد).

### ۵.۳ ویو (زیباترین بخش، ولی نمایشی)

- Vue 3.5 + Vite 8 + Tailwind 3 (توجه: Laravel Core از Tailwind 4 استفاده می‌کند → دو toolchain ناسازگار در یک ریپو).
- ۷ روت: Home, Dashboard, Apps, Targets, Monitors, Alerts, Setting.
- `TargetsPage.vue` بالغ‌ترین صفحه است: جست‌وجو، فیلتر، grid/list، صفحه‌بندی، باز/بسته کردن out-of-scope — همه کلاینت‌ساید روی **۶ برنامه‌ی نمونه‌ی هاردکد** (Tesla، Google، Apple… با مبالغ ساختگی مثل ۱۰۰٬۰۰۰ دلار برای Apple).
- بقیه‌ی صفحه‌ها آمار ثابت دارند: ۲۴ مانیتور، ۱۸ اپ، ۴۷ آلرت. یعنی داشبورد هیچ داده‌ی واقعی‌ای نمی‌خواند.
- `setting.vue` یک `<div>setting</div>` است.
- هیچ `fetch`/`axios`/Pinia/`laravel-echo`/`pusher-js` در `package.json` نیست → ادعای «WebSocket / Laravel Echo» در README **صفر پیاده‌سازی** دارد.
- باگ‌های ریز اما واقعی:
  - دکمه‌ی Documentation در HomePage رویداد `show-modal` را dispatch می‌کند (`HomePage.vue:146`) ولی `App.vue` هیچ listenerی برای آن ندارد (فقط `window.showDevelopmentModal` را تعریف کرده) → **دکمه هیچ کاری نمی‌کند**.
  - دکمه‌ی GitHub به `github.com/AryaKhorasan/watch-tower` لینک می‌دهد، نه ریپوی فعلی `Arash-abraham/watch-tower`.

> ✅ نکته‌ی مثبت: من فرانت را واقعاً بیلد کردم (Vite 8.3.5) و بدون خطا در ~۱ ثانیه بیلد شد؛ UI هم بالا می‌آید و کار می‌کند. یعنی بخش نمایشی سالم است، فقط به داده وصل نیست.

---

## ۶. ادعای README در مقابل واقعیت

| ادعا در README | واقعیت |
|---|---|
| Real-time asset detection | ❌ فقط اجرای دستی + چاپ diff |
| Multi-channel notifications (Discord/Telegram) | ❌ هیچ کدی وجود ندارد |
| Real-Time Sync / WebSocket / Laravel Echo | ❌ وابستگی‌ها هم نصب نشده‌اند |
| Reactive dashboard | ⚠️ UI ری‌اکتیو، ولی روی داده‌ی ثابت |
| Multi-user support | ❌ نه جدول users/sessions، نه auth روی API |
| Scalable backend structure | ⚠️ ساختار پوشه‌ها مرتب است، ولی backend عملاً خالی است |
| «Laravel 13» | ✅ درست (13.9) |
| «Expected stable release in 2–3 months» | با کد فعلی، خوش‌بینانه ولی غیرممکن نیست |

---

## ۷. باگ‌ها و ریسک‌ها (به ترتیب اهمیت)

### 🔴 P0 — الان جلوی اجرا/استفاده را می‌گیرد

| # | مشکل | مسیر |
|---|---|---|
| 1 | **lockfileها به میرورهای ایرانی قفل شده‌اند**: ۲۱۵ آدرس `package-mirror.liara.ir` در `package-lock.json` ویو و ۹۹ تا در لاراول؛ ۲۴۰ آدرس `mirror-composer.runflare.com` در `composer.lock`. بیرون از ایران `npm install` و `composer install` شکست می‌خورند (من دقیقاً همین خطا را گرفتم: ECONNRESET) | `*/package-lock.json`, `composer.lock` |
| 2 | **ایمیج داکر از `registry.docker.ir`** کشیده می‌شود → بیرون از ایران pull نمی‌شود | `docker-compose.yml` |
| 3 | `SubdomainsController` وجود ندارد → روت `v2.1/subdomains` کرش می‌کند | `routes/api.php:13` |
| 4 | `.gitignore` ریشه با **نشانگرهای تضاد merge کامیت شده** (خطوط ۲،۳،۵،۱۲،۱۴،۲۰) → فایل خرابِ کامیت‌شده | `.gitignore` |
| 5 | پورت پیش‌فرض Mongo پایتون `3306` است (MySQL) → اتصال ناموفق | `config.py:15` |
| 6 | لاراول: `DB_CONNECTION=mysql` + نبود `DB_URI` + مدل `Program` بدون اتصال Mongo → مدل و migration از دو دنیای مختلف | `.env.example:23`, `app/Models/Program.php` |
| 7 | `reset_db.py` ایمپورت‌های ناموجود دارد → همیشه کرش | `database/reset_db.py` |

### 🟠 P1 — قبل از هر انتشار عمومی

| # | مشکل |
|---|---|
| 8 | API بدون احراز هویت، بدون rate limit، بدون CORS |
| 9 | `debug=True` در Flask و `APP_DEBUG=true` در env نمونه؛ روت echo ورودی = بازتاب HTML |
| 10 | migration روی اتصال پیش‌فرض ولی schema روی `mongodb`؛ برای migrate به دو دیتابیس نیاز است |
| 11 | `SESSION_DRIVER/QUEUE/CACHE = database` بدون جداول مربوطه |
| 12 | فرانت هیچ اتصالی به API ندارد؛ همه‌ی اعداد ساختگی‌اند (خطر «دموی گمراه‌کننده») |
| 13 | `input()` تعاملی داخل `check_and_create_database` → در cron/CI با EOFError می‌خوابد |
| 14 | بدون لایسنس (ریپوی عمومی بدون license = استفاده‌ی دیگران از نظر حقوقی مبهم) |
| 15 | بدون CI، بدون تست واقعی، Issues غیرفعال |

### 🟡 P2 — کیفیت و نگهداشت

| # | مشکل |
|---|---|
| 16 | دو نسخه Tailwind (۳ در ویو، ۴ در لاراول) و دو زنجیره‌ی build جدا |
| 17 | فایل‌های `__pycache__/*.pyc` کامیت شده‌اند |
| 18 | کلید `"ooscope"` در `benz.json` |
| 19 | دکمه‌ی Documentation مرده (رویداد `show-modal` بدون listener) |
| 20 | لینک GitHub به اکانت قدیمی (`AryaKhorasan`) |
| 21 | `vite-plugin-vue-devtools` در لیست وابستگی‌های معمولی/کانفیگ بیلد |
| 22 | توابع تکراری انیمیشن/پس‌زمینه در چند کامپوننت (کپی‌پیست) → جای استخراج به کامپوننت مشترک |
| 23 | مستندات اجرا برای هر سه ماژول وجود ندارد؛ `WATCH_DIR` هیچ‌جا توضیح داده نشده |
| 24 | نام‌گذاری ناسازگار دیتابیس/کلیدها (`outScopes` vs `out-scope` vs `out_of_scope`) |

---

## ۸. الان چطور اجرا می‌شود؟ (و کجا می‌شکند)

### پایتون — قابل اجرا با کمی دستکاری

```bash
docker compose up -d mongo
cd Watch-Tower-Python-Core
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cat > .env <<'EOF'
DB_HOST=localhost
DB_PORT=27017        # ← پیش‌فرض کد 3306 است؛ باید override شود
DB_USER=root
DB_PASS=secret
DB_NAME=watch-tower
WATCH_DIR=/absolute/path/to/Watch-Tower-Python-Core
EOF

python bounty-programs/watch_find_programs.py   # دانلود + upsert برنامه‌های Bugcrowd
python programs/watch_sync_programs.py          # upsert فایل‌های JSON محلی
```

خروجی: لاگ insert/update و diff دامنه‌ها در ترمینال. همین. هیچ نوتیفیکیشنی ارسال نمی‌شود.

### لاراول — فعلاً عملاً قابل اجرا نیست

```bash
cd Watch-Tower-Laravel-Core
composer install        # ❌ بیرون از ایران روی میرور runflare گیر می‌کند
cp .env.example .env
php artisan key:generate
# نیاز است دستی اضافه شود:
#   DB_URI=mongodb://root:secret@127.0.0.1:27017/?authSource=admin
#   DB_CONNECTION=mongodb
php artisan migrate     # ❌ به MySQL هم نیاز دارد؛ جداول session/cache هم نیست
```

راه‌حل موقت برای محیط غیرایران: حذف `composer.lock`/`package-lock.json` (یا جایگزینی هاست میرورها با `registry.npmjs.org` و `repo.packagist.org`) و تست مجدد.

### ویو — بیلد و اجرا می‌شود (تنها با lockfile اصلاح‌شده)

```bash
cd Watch-Tower-Vue-Js-Core
rm package-lock.json && npm install    # با registry عمومی
npm run dev -- --host 0.0.0.0
```

من همین کار را انجام دادم و UI را برایت بالا آوردم (پیش‌نمایش زنده در پنل).

---

## ۹. امتیازدهی

| معیار | نمره (از ۱۰) | توضیح |
|---|---|---|
| ایده و اهمیت مسئله | ۸ | مسئله واقعی، بازار مشخص، نیاز اثبات‌شده |
| معماری کلی | ۵ | تفکیک سه‌لایه درست، ولی بدون قرارداد/اتصال بین لایه‌ها |
| Python Core | ۵ | منطق diff و upsert خوب؛ اجرا شکننده، بدون scheduler/نوتیفیکیشن |
| Laravel Core | ۲ | اسکلت تقریباً خالی + روت شکسته |
| Vue Frontend | ۶ | UI تمیز و بیلد سالم؛ بدون داده‌ی واقعی و بدون state management |
| مستندات / تست / CI | ۲ | README بازاریابی است، نه راهنما |
| «آماده به کار» بودن | ۲ | با وایب‌کدینگ سریع ساخته شده، هنوز قابل استفاده نیست |
| **جمع‌بندی** | **≈ ۲۵–۳۰٪** | پروتوتایپ چشم‌نواز، محصول نه |

**نگاه منصفانه:** این پروژه یک «نمونه‌کار» (portfolio) خوب است — نشان می‌دهد نویسنده هم Python و هم Laravel و هم Vue را می‌شناسد و طراحی UI خوبی دارد. اما بین «دموی زیبا» و «ابزاری که یک باگ‌هانتر روزانه به آن تکیه کند» فاصله‌ی جدی وجود دارد؛ مهم‌ترین فاصله، **نبود حلقه‌ی end-to-end** است.

---

## ۱۰. نقشه‌ی راه پیشنهادی (MVP در ۲–۳ هفته)

### P0 — اول «یک نخ از سر تا ته» را بساز (۳–۴ روز)

1. یک اسکریپت واحد `monitor.py` که:
   - داده‌ی Bugcrowd (+ HackerOne) را بگیرد؛
   - diff را در کالکشن `changes` با فیلدهای `program, type(added/removed), target, detected_at` بنویسد؛
   - پیام را به Telegram/Discord بفرستد (۲۰ خط کد).
2. یک cron/APScheduler ساده (هر ۳۰–۶۰ دقیقه).
3. حذف `input()` و تبدیل آن به فلگ `--yes`.

با همین مقدار، پروژه از «دمو» به **ابزاری که خودت هر روز استفاده می‌کنی** تبدیل می‌شود — این ارزشمندترین قدم است.

### P1 — API واقعی (۳–۴ روز)

4. `GET /api/v2.1/programs`, `GET /api/v2.1/changes`, `GET /api/v2.1/stats` با Eloquent روی Mongo (`protected $connection = 'mongodb'`).
5. اصلاح env/CORS/session؛ حذف MySQL از مسیر یا مهاجرت کامل به Mongo.
6. Sanctum + یک لایه‌ی توکن ساده برای API.

### P2 — اتصال فرانت به داده (۳–۵ روز)

7. حذف داده‌های هاردکد از `TargetsPage`/`DashboardPage` و جایگزینی با `fetch` از API.
8. یک store ساده (Pinia) + حالت loading/empty/error.
9. (اختیاری) Laravel Reverb/`laravel-echo` برای push تغییرات — یا ساده‌تر: polling هر ۳۰ ثانیه. برای MVP، polling کافی است.

### P3 — تمیزکاری

10. حذف میرورهای ایرانی از lockfileها، `registry` ایمیج داکر → `mongo:7`، حذف `__pycache__`، اصلاح `.gitignore`، افزودن LICENSE، فعال‌کردن Issues، یک GitHub Action برای lint/build.
11. یکتاسازی نام کلیدها (`out_of_scope`) و ساخت مدل داده‌ی مشترک بین پایتون و لاراول.

### معماری هدف (پیشنهاد)

```
scheduler → collector (Python) → MongoDB (programs, changes)
                                        │
                          Laravel API (repo pattern + sanctum)
                                   │            │
                            Vue SPA (fetch)   notifier (Telegram/Discord/webhook)
```

---

## ۱۱. جمع‌بندی در یک پاراگراف

Watch Tower یک ایده‌ی درست و به‌موقع است: «رصد خودکار تغییر scope برنامه‌های باگ‌بانتی و اطلاع فوری». تنها بخشی که امروز واقعاً کار می‌کند، هسته‌ی پایتونی است که داده‌ی Bugcrowd را می‌گیرد، تغییرات را حساب می‌کند و در Mongo می‌نویسد — ولی حتی همان هم نوتیفیکیشن ندارد. لاراول تقریباً خالی و کمی شکسته است، و ویو یک داشبورد خوش‌ساخت اما کاملاً نمایشی با داده‌ی ساختگی است. با ۲ تا ۳ هفته کار متمرکز روی «حلقه‌ی end-to-end» (جمع‌آوری → تغییر → هشدار → داشبورد)، این پروژه می‌تواند به ابزاری واقعاً مفید و حتی یک SaaS کوچک تبدیل شود؛ بدون آن، در حد یک نمونه‌کار جذاب باقی می‌ماند.
