from configs.app_config import BASETAGNEWS, LOGOURL, PERSIAN_MONTHS, CHANNEL_USERNAME, END_MESSAGE
from utilities.utils import get_farsi_month_year, get_yesterday_today_tomorrow_urls, to_persian_number
from typing import Optional

# ============================================================
# 📘 # Message formatting functions
# ============================================================
def make_price_message(prices: dict, f_time: str, farsi_date:str, ap_date: str) -> str:
    def is_valid(value):
        return value not in (0, "0", "N/A", "N.A", None, "")
    
    message = f"""
💰💎 آخرین قیمت طلا و سکه - طلای شهریور
📅 قیمت‌ها امروز: {to_persian_number(farsi_date)} - {to_persian_number(ap_date)}
⏰ آخرین بروزرسانی: {to_persian_number(f_time)}
"""
    # Gold & coins
    base_rows = [
        ("🔸 یک گرم طلای ۱۸ عیار", prices.get('gold'), "تومان"),
        ("🔸 یک گرم طلای ۱۷ عیار", prices.get('gold_740'), "تومان"),
        ("🔹 سکه طرح قدیم", prices.get('coin_old'), "تومان"),
        ("🔹 سکه طرح جدید", prices.get('coin_new'), "تومان"),
        ("🪙 نیم سکه", prices.get('half'), "تومان"),
        ("🟡 ربع سکه", prices.get('quarter'), "تومان"),
        ("🟡 سکه پارسیان", prices.get('parsian'), "تومان"),
        ("🏅 شمش", prices.get('shemsh'), "تومان"),
    ]
    for label, value, unit in base_rows:
        if is_valid(value):
            message += f"{label}: {value} {unit}\n"
    # Crypto & foreign currencies
    extra_rows = [
        ("  ₿ بیت کوین", prices.get("btc"), "دلار"),
        ("💠 اتریوم", prices.get("eth"), "دلار"),
        ("💵 تتر", prices.get("usdt"), "تومان"),
        ("💲 دلار", prices.get("usd"), "تومان"),
        ("💶 یورو", prices.get("eur"), "تومان"),
    ]
    for label, value, unit in extra_rows:
        if is_valid(value):
            message += f"{label}: {value} {unit}\n"
    message += END_MESSAGE
    return message

def make_limit_message(max_request: int) -> str:
    return (
        f"📊 محدودیت درخواست روزانه\n"
        f"❌ شما امروز {max_request} بار قیمت‌ها را دریافت کرده‌اید و به سقف مجاز رسیده‌اید.\n\n"
        f"✅ با عضویت در کانال «طلای شهریور»، می‌توانید روزانه درخواست‌های بیشتری ثبت کنید!\n"
        f"📢 عضویت در کانال: {CHANNEL_USERNAME}\n\n"
        f"🔄 اگر به‌تازگی عضو شده‌اید، لطفاً روی دکمه «بررسی عضویت» بزنید تا محدودیت برداشته شود.\n"
        f"⏳ یا فردا دوباره امتحان کنید. {END_MESSAGE}"
    )

def build_post_html(prices: dict, f_time: str, fa_date: str, weekday: str) -> str:
    def is_valid(value):
        return value not in (0, "0", "N/A", "N.A", None, "")
     
    # Base rows with units   
    rows = [
        ("اونس طلا", prices.get('ounce_tala'), "دلار"),
        ("یک گرم طلای ۲۴ عیار", prices.get('gold_24'), "تومان"),
        ("یک گرم طلای ۱۸ عیار", prices.get('gold'), "تومان"),
        ("یک گرم طلای ۱۷ عیار", prices.get('gold_740'), "تومان"),
        ("مثقال ۱۷", prices.get('bazar_tehran'), "تومان"),
        ("سکه طرح قدیم", prices.get('coin_old'), "تومان"),
        ("سکه طرح جدید (امامی)", prices.get('coin_new'), "تومان"),
        ("نیم سکه", prices.get('half'), "تومان"),
        ("ربع سکه", prices.get('quarter'), "تومان"),
        ("سکه گرمی", prices.get('gram_sekke'), "تومان"),
        ("سکه پارسیان", prices.get('parsian'), "تومان"),
        ("شمش", prices.get('shemsh'), "تومان"),
        ("ارزش سکه", prices.get('arzesh_sekke'), "تومان"),
        ("حباب سکه", prices.get('hobab'), "تومان"),
        ("نقره (ساچمه)", prices.get('silver_sachme'), "تومان"),
        ("گرم نقره ۹۹۹", prices.get('silver_999'), "تومان"),
        ("گرم نقره ۹۲۵", prices.get('silver_925'), "تومان"),
        ("نقره (اونس)", prices.get('silver'), "دلار"),
        ("نفت برنت", prices.get('oil'), "دلار"),
        ("دلار", prices.get("usd"), "تومان"),
        ("یورو", prices.get("eur"), "تومان"),
        ("تتر", prices.get("usdt"), "تومان"),
        ("بیت کوین", prices.get("btc"), "دلار"),
        ("بیت کوین", prices.get("btc_irr"), "تومان"),
        ("اتریوم", prices.get("eth"), "دلار"),
        ("اتریوم", prices.get("eth_irr"), "تومان"),
    ]
    # Keep only valid rows
    valid_rows = [(title, f"{value} {unit}") for title, value, unit in rows if is_valid(value)]
    # Build table rows
    table_rows = ""
    for i, (title, value) in enumerate(valid_rows, 1):
        table_rows += f"<tr><th style='padding: 0px 5px;'>{i}</th><td>{title}</td><td>{value}</td></tr>\n"
    
    month, year = get_farsi_month_year()
    current_archive_url = f"{BASETAGNEWS}/gold-prices-{year}-{month:02d}/"
    current_month_year = f"{PERSIAN_MONTHS[month]} {year}"
    (yesterday_url, today_url, tomorrow_url, yesterday_fa, today_fa, tomorrow_fa) = get_yesterday_today_tomorrow_urls()

    html = f"""
<article class="gold-price-article">
<h1>قیمت طلا و سکه امروز {weekday} {fa_date} - بروزرسانی {f_time}</h1>
در این صفحه از <strong>طلای شهریور</strong> آخرین <strong>قیمت طلا و سکه امروز</strong> را مشاهده می‌کنید.
جدول شامل <strong>طلای ۱۸ عیار، طلای ۲۴ عیار، سکه امامی (طرح جدید)، سکه طرح قدیم، نیم‌سکه، ربع‌سکه، سکه گرمی، سکه گرمی پارسیان، شمش، مثقال ۱۷، نقره (ساچمه)، ارزش سکه</strong> و همچنین نرخ <strong>تتر، یورو، دلار، بیت کوین و اتریوم</strong> است. این اطلاعات روزانه و لحظه‌ای بروزرسانی می‌شود تا شما بتوانید با اطمینان خرید یا سرمایه‌گذاری کنید.
<div class="table-responsive">
  <table class="table table-hover text-center align-middle"
         style="width:100%; border:1px solid #00adee; border-radius:8px; border-collapse:collapse; text-align: center; margin-top:20px;">
    <thead>
      <tr style="background:#f0f8ff;">
        <th style="padding:7px; width:65px; text-align:center; border-bottom:1px solid #00adee;">
          <img src="{LOGOURL}" alt="طلای شهریور" style="height:40px; width:auto; vertical-align:middle;">
        </th>
        <th colspan="2"
            style="padding:7px; text-align:center; color:#FFC91D; font-size:1rem; border-bottom:1px solid #00adee;">
          نرخ طلا و سکه {weekday} {fa_date}
        </th>
      </tr>
      <tr class="table-light">
        <th scope="col" style="padding: 0px 5px; width:65px; text-align:center;">ردیف</th>
        <th scope="col" style="padding: 0px 5px;">عنوان ارز</th>
        <th scope="col" style="padding: 0px 5px;">قیمت</th>
      </tr>
    </thead>
    <tbody>
      {table_rows}
    </tbody>
  </table>
</div>

<strong>⏰ آخرین بروزرسانی: <span style="color: #00adee;">{f_time}</span></strong> | <strong>📅 تاریخ:<span style="color: #00adee;"> {fa_date}</span></strong>

<div style="margin-top: 15px; padding: 12px; background: #f8f8f8; border: 1px solid #ddd; border-radius: 8px; line-height: 1.8;">
    <h3>📌 اونس طلا (انس)</h3>
    <p>
    اونس یا انس (Ounce) یکی از واحدهای رایج سنجش وزن است که در بازار جهانی برای اندازه‌گیری فلزات گران‌بها به‌کار می‌رود. 
    اونس طلا بر اساس «اونس تروا» محاسبه می‌شود که برابر با <strong>۳۱٫۱۰۳۴۷۶۸ گرم</strong> است و مبنای قیمت‌گذاری شمش‌ها و سکه‌های طلا در جهان قرار دارد. 
    قیمت امروز {weekday} {fa_date} هر اونس (انس) طلا: <strong style="color: #d4af37;">{prices['ounce_tala']} دلار</strong>
    </p>
</div>

<h2>تحلیل قیمت طلا و سکه امروز</h2>
بازار طلا و سکه در ایران تحت تأثیر قیمت دلار، انس جهانی طلا و شرایط اقتصادی نوسان دارد. اطلاع از نرخ روز طلا و سکه برای خریداران و سرمایه‌گذاران اهمیت بالایی دارد
قیمت‌های ارائه‌شده شامل <strong>طلای ۱۸ عیار، طلای ۲۴ عیار، مثقال ۱۷، سکه امامی (طرح جدید)، سکه طرح قدیم، نیم‌سکه، ربع‌سکه، سکه گرمی، سکه گرمی پارسیان، شمش، نقره (ساچمه) و ارزش سکه و ارزهایی مانند تتر، یورو، دلار، بیت کوین و اتریوم</strong> است.
همچنین نرخ <strong>دلار (تتر)</strong> به‌عنوان مرجع معاملات ارزی و <strong>اونس طلا (انس طلا)</strong> به‌عنوان معیار جهانی قیمت طلا نمایش داده می‌شود.
اگر قصد خرید طلا یا سرمایه‌گذاری دارید، می‌توانید قیمت نهایی را از طریق صفحه <span style="color: #00adee;"><a style="color: #00adee;" href="https://talayeshahrivar.ir/calculate-gold-price/">محاسبه قیمت طلای شهریور</a></span> بررسی کرده و سپس برای خرید یا مشاوره با ما تماس بگیرید.
<h2>برای سفارش طلا چگونه با طلای شهریور تماس بگیرید؟</h2>
<ul>
    <li><strong>دایرکت اینستاگرام:</strong> <a style="color: #00adee;" href="https://instagram.com/talayeshahrivar" target="_blank" rel="noopener">@talayeshahrivar</a></li>
    <li><strong>چت واتساپ:</strong> <a style="color: #00adee;" href="https://wa.me/989153678924" target="_blank" rel="noopener">+989153678924</a></li>
    <li><strong>تماس تلفنی:</strong> <a style="color: #00adee;" href="tel:+989153678924">+989153678924</a> | <a style="color: #00adee;" href="tel:+989917432796">+989917432796</a></li>
    <li><strong>تلگرام:</strong> <a style="color: #00adee;" href="https://t.me/talayeshahrivar" target="_blank" rel="noopener">@talayeshahrivar</a></li>
</ul>
<strong>بعد از مشاهده نرخ طلا و سکه، می‌توانید برای خرید یا مشاوره تماس بگیرید و سفارش خود را ثبت کنید.</strong>
توجه داشته باشید که قیمت طلا و سکه تحت تأثیر نرخ جهانی طلا، ارز و شرایط اقتصادی داخلی است. بروزرسانی لحظه‌ای این اطلاعات برای خریداران و سرمایه‌گذاران بسیار ضروری است.
طلای شهریور با ارائه قیمت‌های معتبر، امکان خرید مطمئن را برای شما فراهم می‌کند.
<div style="padding: 12px; border: 1px solid #ddd; border-radius: 8px;color:#00adee; line-height: 1.8;">
  <h3>🔁 مشاهده قیمت طلا و سکه در روزهای دیگر:</h3>
  <ul>
    <li>🔹 <a href="{yesterday_url}">قیمت طلا و سکه دیروز ({yesterday_fa})</a></li>
    <li>🔹 <a href="{today_url}">قیمت طلا و سکه امروز ({today_fa})</a></li>
    <li>🔹 <a href="{tomorrow_url}">قیمت طلا و سکه فردا ({tomorrow_fa})</a></li>
  </ul>
  <p>📆 مشاهده آرشیو قیمت‌ها در ماه جاری: 
     <a href="{current_archive_url}">نرخ طلا و سکه {current_month_year} - آرشیو روزانه طلای شهریور</a></p>
</div>
🌟 Shine rich with us – <strong>با ما ثروتمند بدرخشید</strong>
<div style="color:#00adee; text-decoration:none;">
  <a href="{BASETAGNEWS}/talaye-minimal/">#طلای_مینیمال</a> <a href="{BASETAGNEWS}/gheymat-tala/">#قیمت_طلا</a> <a href="{BASETAGNEWS}/gheymat-sekke/">#قیمت_سکه</a> <a href="{BASETAGNEWS}/gheymat-tala-emroz/">#قیمت_طلا_امروز</a> <a href="{BASETAGNEWS}/gheymat-sekke-emroz/">#قیمت_سکه_امروز</a> <a href="{BASETAGNEWS}/gheymat-arz-digital/">#قیمت_ارز_دیجیتال</a> <a href="{BASETAGNEWS}/talaye-shahrivar/">#طلای_شهریور</a> <a href="{BASETAGNEWS}/talayeshahrivar-en/">#talayeshahrivar</a>
</div>
</article>
"""
    return html.strip()

def build_post_for_x(prices: dict, f_time: str, farsi_date: str, link: Optional[str] = None) -> str:
    base_lines = [
        "آخرین قیمت طلا و سکه - طلای شهریور",
        f"{to_persian_number(farsi_date)} ساعت {to_persian_number(f_time)}",
        f"طلای ۱۸ عیار: {prices.get('gold', 'N/A')} تومان",
        f"سکه جدید: {prices.get('coin_new', 'N/A')} تومان",
    ]

    for key, label, unit in [
        ("btc", "بیت کوین", "دلار"),
        ("usdt", "تتر", "تومان"),
        ("usd", "دلار", "تومان"),
    ]:
        val = prices.get(key)
        if val and val not in ("0", "N/A"):
            base_lines.append(f"{label}: {val} {unit}")

    if link:
        base_lines.append(f"جزئیات: {link}")

    base_msg = "\n".join(base_lines)
    hashtag = " #طلا"
    full_with_hashtag = base_msg + hashtag

    if len(full_with_hashtag) <= 280:
        return full_with_hashtag
    else:
        lines = base_lines.copy()
        while len("\n".join(lines) + hashtag) > 280 and len(lines) > 4:
            if "بیت کوین" in lines[-2] or "تتر" in lines[-2] or "دلار" in lines[-2]:
                lines.pop(-2)
            else:
                break

        base_msg = "\n".join(lines)
        if len(base_msg + hashtag) <= 280:
            return base_msg + hashtag
        else:
            if len(base_msg) > 280:
                link_line = lines[-1]
                available = 280 - len(link_line) - 1
                truncated = "\n".join(lines[:-1])[:available]
                return f"{truncated}…\n{link_line}"
            return base_msg
