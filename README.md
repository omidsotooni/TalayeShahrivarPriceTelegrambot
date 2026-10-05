# 📊 TalayeShahrivar Telegram Bot | ربات تلگرام طلای شهریور

**Language / زبان:** [English](#english) | [فارسی](#persian)

---

<a id="english"></a>
# English

A Telegram bot for **real-time gold, coin, cryptocurrency and foreign-exchange prices** (Persian/RTL).
It limits daily requests depending on whether a user is a member of the **@talayeshahrivar** channel, and publishes scheduled price updates to Telegram, WordPress and (optionally) X.

## ⚠️ Disclaimer

- **Not financial advice.** Prices are shown for general information only. Nothing in this project is investment, trading, tax or legal advice. Do not make buying or selling decisions based only on this bot.
- **No accuracy guarantee.** Prices come from third-party websites and APIs (tgju.org, tala.ir, Nobitex). They may be delayed, wrong, incomplete or unavailable at any time. Always check the price with an official or trusted source before any transaction.
- **Provided "as is", without warranty of any kind.** The author(s) accept no liability for any loss, damage or consequence (financial or otherwise) caused by using, modifying or running this software, including wrong prices, downtime, bugs, account bans or leaked credentials.
- **Third-party services and terms.** You are solely responsible for complying with the terms of service, rate limits and laws that apply to every service you connect (Telegram, X/Twitter, WordPress, tgju.org, tala.ir, Nobitex). Some price sources are unofficial endpoints that can change or be blocked without notice.
- **Not affiliated.** This project is not affiliated with, endorsed by or sponsored by Telegram, X, WordPress, tgju.org, tala.ir or Nobitex. All names and trademarks belong to their owners.
- **Your credentials, your responsibility.** Never publish bot tokens, API keys, passwords, cookies or user data. Anyone who deploys this bot is responsible for protecting their users' data (for example `user_ids.txt`) and for following applicable privacy laws.

## 🚀 Features

- 📌 **Gold & coin prices**: 18K/24K gold, Emami and old-design coins, half/quarter/gram coins, Parsian coin, ingots, silver, Brent oil.
- 💱 **Crypto prices**: top 10 coins by volume on Nobitex, plus lookup of a single coin.
- 🌍 **Foreign exchange**: USD, EUR, GBP, AED, TRY and more.
- ✅ **Membership control**: higher daily quota for channel members.
- 🔐 **Admin panel**: manual price push to channel/website, export of user info to CSV.
- 🗓 **Scheduled posting** (Tehran time): **12:12** and **17:17**. The daily counter resets at **00:01**.
- 🌐 **WordPress auto-post**: generates an HTML post (Persian date, time, price table) in the "اخبار طلا و سکه" category with auto title and slug:
  - Title: `قیمت طلا و سکه امروز {weekday} {fa_date} - بروزرسانی {time}`
  - Slug: `gold-coin-prices-today-{YYYY-MM-DD}-{HHMM}`
- 🕊️ **X (Twitter) posting** (`x_sender_service.py`): short summary, max 280 characters, link always kept. The call in `send_price_update()` is **commented out by default**; uncomment it once your X API keys are set.
- 📸 **Featured-media metadata updater** (`update_media_service.py` + Jupyter notebook): updates title/alt/caption/description of daily WordPress images from an Excel file.

Price sources: tgju.org (primary, with several mirrors), tala.ir (fallback), Nobitex (crypto).

## ⚙️ Requirements

- Python 3.9+
- Telegram bot token (from @BotFather), with the bot added as **admin** of your channel (needed for membership checks)
- WordPress site with an Application Password (optional)
- X API keys (optional)

## 📦 Installation

```bash
git clone https://github.com/omidsotooni/TalayeShahrivarPriceTelegrambot
cd TalayeShahrivarPriceTelegrambot

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🛠 Configuration

Open `src/configs/app_config.py` and fill in your own values:

- `BOT_TOKEN` (from @BotFather), `CHAT_ID` (your channel ID), `ADMIN_IDs` (Telegram user IDs of admins), `CHANNEL_USERNAME`
- WordPress (optional): `WP_USER`, `WP_APP_PASS`, `WP_URL` and the related URLs
- X / Twitter (optional): `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET`, `X_BEARER_TOKEN`

> ⚠️ Never commit your filled-in `app_config.py`, `user_ids.txt` or `LogBot.txt`.
> Tip: after cloning on your server run `git update-index --skip-worktree src/configs/app_config.py` so your real credentials can't be committed by mistake.

## ▶️ Run

```bash
cd src
python main.py

# or in the background on a server
nohup python3 main.py > bot.log 2>&1 &
tail -f bot.log
```

## 📂 Project structure

```
.
├── src/
│   ├── configs/
│   │   ├── __init__.py              # from .app_config import *
│   │   └── app_config.py            # fill in your credentials here
│   ├── services/
│   │   └── sender_receiver_service.py
│   ├── templates/
│   │   └── message_builder.py
│   ├── utilities/
│   │   └── utils.py
│   ├── JupyterCodes/
│   │   └── image_metadata_talayeshahrivar.ipynb
│   ├── main.py
│   ├── x_sender_service.py
│   └── update_media_service.py
├── requirements.txt
└── .gitignore
```

Created at runtime: `user_ids.txt` (user ID + membership), `telegram_users.csv`, `LogBot.txt`.

## 🎮 Bot usage

- `/start` opens the main menu: gold & coin prices, crypto prices, currency list, foreign exchange, membership check.
- Admins also get: send prices to channel + website, export users info.

### Daily request limits

| User | Limit |
|---|---|
| Non-member | 5 / day |
| Channel member | 15 / day (5 + `MAX_REQUESTS_MEMBER` = 10) |
| Admin | Unlimited |

## 💡 Roadmap

- Replace `user_ids.txt` with a database
- Multi-language support
- Advanced admin dashboard

---

<a id="persian"></a>

<div dir="rtl" align="right">

# فارسی

یک ربات تلگرام برای **دریافت قیمت لحظه‌ای طلا، سکه، ارزهای دیجیتال و ارزهای خارجی**.
ربات **محدودیت درخواست روزانه** را بر اساس عضویت کاربر در کانال **@talayeshahrivar** مدیریت می‌کند و قیمت‌ها را به‌صورت زمان‌بندی‌شده در تلگرام، وردپرس و (اختیاری) X منتشر می‌کند.

## ⚠️ سلب مسئولیت

- **توصیه مالی نیست.** قیمت‌ها فقط برای اطلاع‌رسانی عمومی نمایش داده می‌شوند. هیچ بخشی از این پروژه توصیه سرمایه‌گذاری، معاملاتی، مالیاتی یا حقوقی نیست. تصمیم خرید یا فروش را فقط بر اساس این ربات نگیرید.
- **تضمینی برای دقت قیمت‌ها وجود ندارد.** قیمت‌ها از وب‌سایت‌ها و APIهای شخص ثالث (tgju.org، tala.ir، نوبیتکس) دریافت می‌شوند و ممکن است دیر، نادرست، ناقص یا در هر زمان در دسترس نباشند. پیش از هر معامله، قیمت را از یک منبع رسمی یا معتبر بررسی کنید.
- **این نرم‌افزار «همان‌گونه که هست» و بدون هیچ‌گونه ضمانتی ارائه می‌شود.** نویسنده یا نویسندگان هیچ مسئولیتی در قبال زیان یا خسارت (مالی یا غیرمالی) ناشی از استفاده، تغییر یا اجرای این نرم‌افزار ندارند؛ از جمله قیمت اشتباه، قطعی سرویس، باگ، مسدود شدن حساب‌ها یا درز اطلاعات احراز هویت.
- **سرویس‌ها و قوانین شخص ثالث.** رعایت شرایط استفاده، محدودیت‌های نرخ درخواست و قوانین مربوط به هر سرویسی که متصل می‌کنید (تلگرام، X/توییتر، وردپرس، tgju.org، tala.ir، نوبیتکس) فقط بر عهده خود شماست. برخی منابع قیمت، endpointهای غیررسمی هستند که ممکن است بدون اطلاع قبلی تغییر کنند یا مسدود شوند.
- **وابستگی رسمی وجود ندارد.** این پروژه هیچ ارتباط، تأیید یا حمایت رسمی از سوی تلگرام، X، وردپرس، tgju.org، tala.ir یا نوبیتکس ندارد. تمام نام‌ها و علائم تجاری متعلق به صاحبان آن‌هاست.
- **اطلاعات احراز هویت شما، مسئولیت شما.** هرگز توکن ربات، کلیدهای API، رمزها، کوکی‌ها یا اطلاعات کاربران را منتشر نکنید. هر کسی که این ربات را راه‌اندازی می‌کند مسئول محافظت از داده‌های کاربران خود (مثلاً `user_ids.txt`) و رعایت قوانین حریم خصوصی مربوطه است.

## 🚀 ویژگی‌ها

- 📌 **قیمت طلا و سکه**: طلای ۱۸ و ۲۴ عیار، سکه امامی و طرح قدیم، نیم‌سکه، ربع‌سکه، سکه گرمی، سکه پارسیان، شمش، نقره و نفت برنت.
- 💱 **قیمت ارزهای دیجیتال**: ۱۰ ارز برتر بر اساس حجم معاملات در نوبیتکس و جستجوی یک ارز مشخص.
- 🌍 **قیمت ارزهای خارجی**: دلار، یورو، پوند، درهم، لیر و غیره.
- ✅ **کنترل عضویت**: اعضای کانال سهمیه روزانه بیشتری دارند.
- 🔐 **پنل ادمین**: ارسال دستی قیمت‌ها به کانال و وب‌سایت، و خروجی گرفتن اطلاعات کاربران در فایل CSV.
- 🗓 **ارسال زمان‌بندی‌شده** (به وقت تهران): ساعت **12:12** و **17:17**. شمارشگر درخواست‌های روزانه ساعت **00:01** بازنشانی می‌شود.
- 🌐 **انتشار خودکار در وردپرس**: تولید پست HTML (تاریخ شمسی، ساعت، جدول قیمت‌ها) در دسته «اخبار طلا و سکه» با عنوان و نامک خودکار:
  - عنوان: `قیمت طلا و سکه امروز {weekday} {fa_date} - بروزرسانی {time}`
  - نامک: `gold-coin-prices-today-{YYYY-MM-DD}-{HHMM}`
- 🕊️ **ارسال در X (توییتر)** (`x_sender_service.py`): متن کوتاه تا ۲۸۰ کاراکتر، با حفظ کامل لینک. فراخوانی آن در `send_price_update()` به‌صورت پیش‌فرض **کامنت شده است**؛ بعد از تنظیم کلیدهای API کامنت را بردارید.
- 📸 **بروزرسانی متادیتای تصاویر ویژه** (`update_media_service.py` و دفترچه Jupyter): عنوان، متن جایگزین، کپشن و توضیحات تصاویر روزانه وردپرس را از فایل اکسل به‌روز می‌کند.

منابع قیمت: tgju.org (اصلی، با چند آینه)، tala.ir (پشتیبان) و نوبیتکس (ارز دیجیتال).

## ⚙️ پیش‌نیازها

- Python نسخه 3.9 به بالا
- توکن ربات تلگرام (از @BotFather) و افزودن ربات به‌عنوان **ادمین** کانال (برای بررسی عضویت لازم است)
- سایت وردپرس با Application Password (اختیاری)
- کلیدهای API ایکس (اختیاری)

## 📦 نصب

```bash
git clone https://github.com/omidsotooni/TalayeShahrivarPriceTelegrambot
cd TalayeShahrivarPriceTelegrambot

python -m venv venv
source venv/bin/activate        # ویندوز: venv\Scripts\activate
pip install -r requirements.txt
```

## 🛠 پیکربندی

فایل `src/configs/app_config.py` را باز کنید و مقادیر خودتان را وارد کنید:

- `BOT_TOKEN` (از @BotFather)، `CHAT_ID` (شناسه کانال)، `ADMIN_IDs` (شناسه عددی تلگرام ادمین‌ها)، `CHANNEL_USERNAME`
- وردپرس (اختیاری): `WP_USER`، `WP_APP_PASS`، `WP_URL` و آدرس‌های مرتبط
- X / توییتر (اختیاری): `X_API_KEY`، `X_API_SECRET`، `X_ACCESS_TOKEN`، `X_ACCESS_TOKEN_SECRET`، `X_BEARER_TOKEN`

> ⚠️ فایل `app_config.py` پرشده، `user_ids.txt` و `LogBot.txt` را هرگز commit نکنید.
> نکته: بعد از clone روی سرور، دستور `git update-index --skip-worktree src/configs/app_config.py` را بزنید تا اطلاعات واقعی شما اشتباهی commit نشود.

## ▶️ اجرا

```bash
cd src
python main.py

# یا اجرا در پس‌زمینه روی سرور
nohup python3 main.py > bot.log 2>&1 &
tail -f bot.log
```

## 📂 ساختار پروژه

```
.
├── src/
│   ├── configs/
│   │   ├── __init__.py              # from .app_config import *
│   │   └── app_config.py            # اطلاعات خود را اینجا وارد کنید
│   ├── services/
│   │   └── sender_receiver_service.py
│   ├── templates/
│   │   └── message_builder.py
│   ├── utilities/
│   │   └── utils.py
│   ├── JupyterCodes/
│   │   └── image_metadata_talayeshahrivar.ipynb
│   ├── main.py
│   ├── x_sender_service.py
│   └── update_media_service.py
├── requirements.txt
└── .gitignore
```

فایل‌هایی که هنگام اجرا ساخته می‌شوند: `user_ids.txt` (شناسه کاربر و وضعیت عضویت)، `telegram_users.csv` و `LogBot.txt`.

## 🎮 نحوه استفاده

- دستور `/start` منوی اصلی را نمایش می‌دهد: قیمت طلا و سکه، قیمت ارز دیجیتال، لیست ارزها، ارزهای خارجی و بررسی عضویت.
- ادمین‌ها علاوه بر این‌ها امکان ارسال قیمت به کانال و وب‌سایت و دریافت اطلاعات کاربران را دارند.

### محدودیت درخواست روزانه

| کاربر | محدودیت |
|---|---|
| غیرعضو | ۵ درخواست در روز |
| عضو کانال | ۱۵ درخواست در روز (۵ + مقدار `MAX_REQUESTS_MEMBER` یعنی ۱۰) |
| ادمین | نامحدود |

## 💡 برنامه‌های آینده

- جایگزینی `user_ids.txt` با پایگاه داده
- پشتیبانی چندزبانه
- داشبورد مدیریتی پیشرفته

</div>