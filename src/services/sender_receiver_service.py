import os
import time
import html
import asyncio
import requests
import telegram
import threading
import csv
from datetime import datetime
from requests.auth import HTTPBasicAuth
from telegram.ext import CallbackContext
from typing import Optional, Tuple, Union
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from templates.message_builder import build_post_html, make_price_message, make_limit_message, build_post_for_x
from configs.app_config import (
    API_URL, BASE_NOBITEXT_URL, TGJU_API, TGJU_ENDPOINTS, BOT_TOKEN, CACHE_TTL_SECONDS, CHANNEL_USERNAME, END_MESSAGE, HEADERS, 
    MAX_REQUESTS_MEMBER, MAX_REQUESTS_NON_MEMBER, TEHRAN_TZ, UNRECOGNIZED_COMMAND_MESSAGE, USER_CACHE, USER_FILE, 
    USER_REQUESTS, WP_APP_PASS, WP_URL, WP_USER, ADMIN_IDs, CHAT_ID, CURRENCY_LIST, CURRENCIES_COUNTRY_LIST, VALID_STATUSES,
    _NOBITEXT_CACHE, _CURRENCY_COUNTRY_CACHE
)
from utilities.utils import (
    format_rial_to_toman, get_current_month_tag_id, get_farsi_date, 
    get_persian_datetime, get_persian_weekday_from_jdate, log_message, parse_price, get_featured_media_for_today, to_persian_number
)
from x_sender_service import post_price_update_to_x

bot = telegram.Bot(token=BOT_TOKEN)

# ============================================================
# Sender and Receiver functions
# ============================================================
def run_async_task(coroutine):
    thread_loop = asyncio.new_event_loop()
    thread = threading.Thread(target=lambda: thread_loop.run_until_complete(coroutine))
    thread.start()
    thread.join()

def reset_user_requests():
    global USER_REQUESTS
    for user_id in USER_REQUESTS:
        USER_REQUESTS[user_id]["count"] = 0
        USER_REQUESTS[user_id]["date"] = datetime.now().date()
    log_message("✅ Daily user request limits reset.")

def schedule_jobs():
    scheduler = BackgroundScheduler(timezone=TEHRAN_TZ)
    
    times = [(12, 12), (17, 17)]

    for hour, minute in times:
        scheduler.add_job(lambda: run_async_task(send_price_update()), "cron", hour=hour, minute=minute)
   
    # Run every 20 seconds
    # scheduler.add_job(lambda: run_async_task(send_price_update), "interval", seconds=20)

    scheduler.add_job(lambda: run_async_task(reset_user_requests()), "cron", hour=0, minute=1)

    scheduler.start()
    log_message("📅 Task scheduling was done!")

def fetch_from_tala():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "price" not in data:
            return None
        p = data["price"]
        return {
            # GOLD
            "ounce_tala": parse_price(p.get("ounce", "N/A")),
            "bazar_tehran": parse_price(p.get("bazartehran", "N/A")),
            "gold": parse_price(p.get("geram18", "N/A")),
            "gold_740": parse_price(p.get("geram740", "N/A")),
            "gold_24": parse_price(p.get("geram24", "N/A")),
            "coin_new": parse_price(p.get("sekkejad", "N/A")),
            "coin_old": parse_price(p.get("sekkegad", "N/A")),
            "half": parse_price(p.get("sekkenim", "N/A")),
            "quarter": parse_price(p.get("sekkerob", "N/A")),
            "arzesh_sekke": parse_price(p.get("sekke-arzesh", "N/A")),
            "gram_sekke": parse_price(p.get("sekkegrm", "N/A")),
            "shemsh": parse_price(p.get("shemsh1", "N/A")),
            "parsian": parse_price(p.get("parsian1", "N/A")),
            "hobab": parse_price(p.get("hobab", "N/A")),
            # SILVER
            "silver": parse_price(p.get("silver", "N/A")),
            "silver_sachme": parse_price(p.get("silver-sachme", "N/A")),
            # OIL
            "oil": parse_price(p.get("ENERGY_BRENT", "N/A")),
            # CRYPTO CURRENCY
            "btc": parse_price(p.get("BTC_USDT", "N/A")),
            "usdt": parse_price(p.get("USDT_IRT", "N/A")),
            "eth": parse_price(p.get("ETH_USDT", "N/A")),
            "btc_irr": parse_price(p.get("BTC_IRT", "N/A")),
            "eth_irr": parse_price(p.get("ETH_IRT", "N/A")),
            # FOREIGN COUNTRY CURRENCY
            "try": parse_price(p.get("try", "N/A")),
            "omr": parse_price(p.get("omr", "N/A")),
            "usd": parse_price(p.get("usd", "N/A")),
            "eur": parse_price(p.get("eur", "N/A")),
            "aed": parse_price(p.get("aed", "N/A")),
            "gbp": parse_price(p.get("gbp", "N/A")),
            "chf": parse_price(p.get("chf", "N/A")),
            "cny": parse_price(p.get("cny", "N/A")),
            "cad": parse_price(p.get("cad", "N/A")),
            "aud": parse_price(p.get("aud", "N/A")),
            "afn": parse_price(p.get("afn", "N/A")),
        }
    except Exception as e:
        log_message(f"❌ tala.ir failed: {e}")
        return None

def fetch_from_tgju_TGJU_API():
    try:
        response = requests.get(TGJU_API, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "current" not in data:
            return None
        p = data["current"]
        return {
            # GOLD
            "ounce_tala": parse_price(p.get("ons", {}).get("p")),
            "bazar_tehran": parse_price(p.get("mesghal", {}).get("p"), to_toman=True),
            "gold": parse_price(p.get("geram18", {}).get("p"), to_toman=True),
            "gold_24": parse_price(p.get("geram24", {}).get("p"), to_toman=True),
            "gold_740": parse_price(p.get("gold_740k", {}).get("p"), to_toman=True),
            "coin_new": parse_price(p.get("sekee", {}).get("p"), to_toman=True),
            "coin_old": parse_price(p.get("sekeb", {}).get("p"), to_toman=True),
            "half": parse_price(p.get("nim", {}).get("p"), to_toman=True),
            "quarter": parse_price(p.get("rob", {}).get("p"), to_toman=True),
            "arzesh_sekke": parse_price(p.get("sekke-arzesh", {}).get("p"), to_toman=True),
            "gram_sekke": parse_price(p.get("gerami", {}).get("p"), to_toman=True),
            "shemsh": parse_price(p.get("shemsh", {}).get("p"), to_toman=True),
            "parsian": parse_price(p.get("parsian1", {}).get("p"), to_toman=True),
            "hobab": parse_price(p.get("hobab", {}).get("p"), to_toman=True),
            # SILVER
            "silver": parse_price(p.get("silver", {}).get("p")),
            "silver_999": parse_price(p.get("silver_999", {}).get("p"), to_toman=True),
            "silver_925": parse_price(p.get("silver_925", {}).get("p"), to_toman=True),
            "silver_sachme": parse_price(p.get("silver-sachme", {}).get("p"), to_toman=True),
            # OIL
            "oil": parse_price(p.get("oil_brent", {}).get("p")),
            # CRYPTO CURRENCY
            "btc": parse_price(p.get("crypto-bitcoin", {}).get("p")),
            "eth": parse_price(p.get("crypto-ethereum", {}).get("p")),
            "usdt": parse_price(p.get("crypto-tether-irr", {}).get("p"), to_toman=True),
            "btc_irr": parse_price(p.get("crypto-bitcoin-irr", {}).get("p"), to_toman=True),
            "eth_irr": parse_price(p.get("crypto-ethereum-irr", {}).get("p"), to_toman=True),
            # FOREIGN COUNTRY CURRENCY
            "usd": parse_price(p.get("price_dollar_rl", {}).get("p"), to_toman=True),
            "eur": parse_price(p.get("price_eur", {}).get("p"), to_toman=True),
            "gbp": parse_price(p.get("price_gbp", {}).get("p"), to_toman=True),
            "aed": parse_price(p.get("price_aed", {}).get("p"), to_toman=True),
            "omr": parse_price(p.get("price_omr", {}).get("p"), to_toman=True),
            "try": parse_price(p.get("price_try", {}).get("p"), to_toman=True),
            "cny": parse_price(p.get("price_cny", {}).get("p"), to_toman=True),
            "chf": parse_price(p.get("price_chf", {}).get("p"), to_toman=True),
            "cad": parse_price(p.get("price_cad", {}).get("p"), to_toman=True),
            "aud": parse_price(p.get("price_aud", {}).get("p"), to_toman=True),
            "afn": parse_price(p.get("price_afn", {}).get("p"), to_toman=True),
            "jpy": parse_price(p.get("price_jpy", {}).get("p"), to_toman=True),
        }
    except Exception as e:
        log_message(f"❌ tgju.org failed: {e}")
        return None

def fetch_from_tgju():
    for url in TGJU_ENDPOINTS:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if "current" not in data:
                log_message(f"❌ tgju invalid response ({url})")
                continue
            p = data["current"]
            return {
                # GOLD
                "ounce_tala": parse_price(p.get("ons", {}).get("p")),
                "bazar_tehran": parse_price(p.get("mesghal", {}).get("p"), to_toman=True),
                "gold": parse_price(p.get("geram18", {}).get("p"), to_toman=True),
                "gold_24": parse_price(p.get("geram24", {}).get("p"), to_toman=True),
                "gold_740": parse_price(p.get("gold_740k", {}).get("p"), to_toman=True),
                "coin_new": parse_price(p.get("sekee", {}).get("p"), to_toman=True),
                "coin_old": parse_price(p.get("sekeb", {}).get("p"), to_toman=True),
                "half": parse_price(p.get("nim", {}).get("p"), to_toman=True),
                "quarter": parse_price(p.get("rob", {}).get("p"), to_toman=True),
                "arzesh_sekke": parse_price(p.get("sekke-arzesh", {}).get("p"), to_toman=True),
                "gram_sekke": parse_price(p.get("gerami", {}).get("p"), to_toman=True),
                "shemsh": parse_price(p.get("shemsh", {}).get("p"), to_toman=True),
                "parsian": parse_price(p.get("parsian1", {}).get("p"), to_toman=True),
                "hobab": parse_price(p.get("hobab", {}).get("p"), to_toman=True),
                # SILVER
                "silver": parse_price(p.get("silver", {}).get("p")),
                "silver_999": parse_price(p.get("silver_999", {}).get("p"), to_toman=True),
                "silver_925": parse_price(p.get("silver_925", {}).get("p"), to_toman=True),
                "silver_sachme": parse_price(p.get("silver-sachme", {}).get("p"), to_toman=True),
                # OIL
                "oil": parse_price(p.get("oil_brent", {}).get("p")),
                # CRYPTO CURRENCY
                "btc": parse_price(p.get("crypto-bitcoin", {}).get("p")),
                "eth": parse_price(p.get("crypto-ethereum", {}).get("p")),
                "usdt": parse_price(p.get("crypto-tether-irr", {}).get("p"), to_toman=True),
                "btc_irr": parse_price(p.get("crypto-bitcoin-irr", {}).get("p"), to_toman=True),
                "eth_irr": parse_price(p.get("crypto-ethereum-irr", {}).get("p"), to_toman=True),
                # FOREIGN COUNTRY CURRENCY
                "usd": parse_price(p.get("price_dollar_rl", {}).get("p"), to_toman=True),
                "eur": parse_price(p.get("price_eur", {}).get("p"), to_toman=True),
                "gbp": parse_price(p.get("price_gbp", {}).get("p"), to_toman=True),
                "aed": parse_price(p.get("price_aed", {}).get("p"), to_toman=True),
                "omr": parse_price(p.get("price_omr", {}).get("p"), to_toman=True),
                "try": parse_price(p.get("price_try", {}).get("p"), to_toman=True),
                "cny": parse_price(p.get("price_cny", {}).get("p"), to_toman=True),
                "chf": parse_price(p.get("price_chf", {}).get("p"), to_toman=True),
                "cad": parse_price(p.get("price_cad", {}).get("p"), to_toman=True),
                "aud": parse_price(p.get("price_aud", {}).get("p"), to_toman=True),
                "afn": parse_price(p.get("price_afn", {}).get("p"), to_toman=True),
                "jpy": parse_price(p.get("price_jpy", {}).get("p"), to_toman=True),
            }
        except Exception as e:
            log_message(f"❌ tgju failed ({url}): {e}")
            continue

    return None

def get_prices():
    try:
        # log_message("🌐 Trying tgju.org ...")
        data = fetch_from_tgju()
        if data:
            log_message("✅ Data fetched from tgju.org")
            return data
        
        # log_message("🔁 Falling back to tala.ir ...")
        data = fetch_from_tala()
        if data:
            log_message("✅ Data fetched from tala.ir")
            return data
        
        log_message("❌ Both sources failed")
        return {}
    except Exception as e:
        log_message(f"Error fetching prices: {e}")
        return {}

def publish_post(title: str, content: str, slug: str) -> Optional[tuple[str, str]]:
    month_tag_id = get_current_month_tag_id()
    featured_media = get_featured_media_for_today(slug=slug)
    post = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "publish", # publish or draft
        "news_category": [606],
        "news_tag": [608, 609, 612, 613, 614, 615, 616,
                     617, 618, 619, 620, 621, 624, 625,
                     626, 627, 628, 629, 630, 631, month_tag_id],
        "featured_media": featured_media
    }
    response = requests.post(WP_URL, auth=HTTPBasicAuth(WP_USER, WP_APP_PASS), json=post)
    if response.status_code == 201:
        data = response.json()
        post_id = data.get("id")
        full_link = data.get("link")
        short_link = f"https://talayeshahrivar.ir/?p={post_id}"        
        log_message(f"✅ منتشر شد: {full_link}")
        return full_link, short_link
    else:
        log_message(f"❌ خطا: {response.text}")
        return None

def check_limit_and_increment(user_id: int, max_request: int) -> Tuple[bool, Optional[str]]:
    current_date = datetime.now().date()
    if user_id not in USER_REQUESTS:
        USER_REQUESTS[user_id] = {"count": 0, "date": current_date}
    user_data = USER_REQUESTS[user_id]
    if user_data["date"] != current_date:
        user_data["count"] = 0
        user_data["date"] = current_date      
    if user_data["count"] >= max_request:
        return False, make_limit_message(max_request)
    user_data["count"] += 1
    return True, None

async def check_and_store_user(user_id: int):
    if user_id in USER_CACHE:
        return
    is_member, _ = await check_membership(user_id=user_id)
    append_user_to_file(user_id=user_id, is_member=is_member)
    USER_CACHE[user_id] = is_member

async def check_request_limit(query):
    user_id = query.from_user.id    
    max_request = MAX_REQUESTS_NON_MEMBER
    is_member = False
    if user_id in USER_CACHE:
        is_member = USER_CACHE[user_id]    
    if is_member:
        max_request += MAX_REQUESTS_MEMBER
    allowed, limit_msg = check_limit_and_increment(user_id, max_request)
    if not allowed:
        await query.message.reply_text(limit_msg)
    return allowed

def load_users_from_file():
    global USER_CACHE
    USER_CACHE.clear()
    if not os.path.exists(USER_FILE):
        return
    with open(USER_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                uid_str, member_str = line.strip().split(',')
                uid = int(uid_str)
                is_member = member_str.strip().lower() == 'true'
                USER_CACHE[uid] = is_member
            except Exception:
                continue

async def get_users_info():
    users_info = []
    for user_id in USER_CACHE.keys():
        try:
            # get latest membership status
            is_member, member = await check_membership(user_id)
            # get user info
            user = await bot.get_chat(user_id)
            users_info.append({
                "Id": user.id,
                "Username": user.username or "",
                "FirstName": user.first_name or "",
                "LastName": user.last_name or "",
                "LanguageCode": getattr(user, "language_code", "") or "",
                "IsMember": is_member,
                "Error": ""
            })
        except Exception as e:
            log_message(
                f"{user_id} -> ERROR: {e}"
            )
            users_info.append({
                "Id": user_id,
                "Username": "",
                "FirstName": "",
                "LastName": "",
                "LanguageCode": "",
                "IsMember": False,
                "Error": str(e)
            })
    with open(
        "telegram_users.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "Id",
                "Username",
                "FirstName",
                "LastName",
                "LanguageCode",
                "IsMember",
                "Error"
            ]
        )
        writer.writeheader()
        writer.writerows(users_info)
    log_message("✅ telegram_users.csv created successfully")
    return users_info

async def check_membership(user_id: int) -> Tuple[bool, Union[telegram.ChatMember, None]]:
    try:
        member = await bot.get_chat_member(chat_id=CHAT_ID, user_id=user_id)        
        is_valid = member.status in VALID_STATUSES
        return is_valid, member
    except Exception as e:
        log_message(f"Membership check failed: {e}")
        return False, None

def append_user_to_file(user_id: int, is_member: bool):
    if user_id in USER_CACHE:
        return
    with open(USER_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{user_id},{is_member}\n")

async def check_user_membership_status(query: telegram.CallbackQuery, user_id: int):
    try:
        load_users_from_file()
        if user_id in USER_CACHE and USER_CACHE[user_id] is True:
            await query.message.reply_text("✅ شما قبلاً به عنوان عضو شناخته شده‌اید و می‌توانید از خدمات ربات استفاده کنید.")
            return
        
        waiting_message = await query.message.reply_text("⏳ لطفاً صبر کنید...")
        await asyncio.sleep(3)

        is_member, member = await check_membership(user_id=user_id)
        status = member.status.lower()
        user = member.user
        user_identifier = f"@{user.username}" if user.username else f"{user.id}"
        
        USER_CACHE[user_id] = is_member
        append_user_to_file(user_id, is_member)
        if status in VALID_STATUSES:
            await waiting_message.edit_text(
                f"✅ خوش آمدید!\n"
                f"کاربر گرامی {user_identifier}، شما عضو کانال «طلای شهریور» هستید و می‌توانید از خدمات ربات استفاده نمایید. 🌟"
                )
        elif status == "restricted":
            await waiting_message.edit_text(
                f"⛔ محدودیت دسترسی\n"
                f"کاربر گرامی {user_identifier}، دسترسی شما به کانال «طلای شهریور» محدود شده است. "
                f"لطفاً برای رفع مشکل با ادمین [@TalayeShahrivar_Admin] تماس بگیرید. 📩"
                )
        elif status == "left":
            await waiting_message.edit_text(
                f"🚪 خروج از کانال\n"
                f"کاربر گرامی {user_identifier}، شما از کانال «طلای شهریور» خارج شده‌اید. 😔\n\n"
                f"برای استفاده از خدمات ربات:\n"
                f"1️⃣ ابتدا در کانال عضو شوید: {CHANNEL_USERNAME}\n"
                f"2️⃣ سپس مجدداً روی دکمه «📋 وضعیت من؟» کلیک کنید تا عضویت شما بررسی شود.\n\n"
                f"در صورت بروز مشکل، با ادمین [@TalayeShahrivar_Admin] تماس بگیرید. 🙏"
                )
        else:
            await waiting_message.edit_text(
                "❌ عضویت نامشخص\n"
                "شما عضو کانال «طلای شهریور» نیستید. لطفاً ابتدا عضو کانال شوید تا بتوانید از خدمات ربات استفاده کنید. 📢"
                )
    except telegram.error.BadRequest as e:
        log_message(f"❌ Error fetching user status: {e}")
        await query.message.reply_text("⚠️ دریافت وضعیت عضویت ممکن نیست. لطفاً بعداً دوباره امتحان کنید.")  
        
async def user_status_message(query: telegram.CallbackQuery, user_id: int):
    try:
        is_member, member = await check_membership(user_id=user_id)        
        user = member.user
        status = member.status
        user_identifier = f"@{user.username}" if user.username else f"ID: {user.id}"

        await query.message.reply_text(
            "✅ شما عضو کانال طلای شهریور هستید!" if is_member else "❌ شما عضو کانال طلای شهریور نیستید."
        )
        current_date = datetime.now().date()
        user_data = USER_REQUESTS.get(user_id)        
        if user_data and user_data["date"] == current_date:
            user_requests_today = user_data["count"]
        else:
            user_requests_today = 0

        status_mapping = {
            "member": "شما به عنوان عضو گرامی کانال طلای شهریور به ما پیوسته‌اید. خوش آمدید!",
            "administrator": "شما ادمین محترم کانال طلای شهریور هستید. از همکاری شما سپاسگزاریم!",
            "creator": "شما هم‌بنیان‌گذار طلای شهریور هستید. از پشتیبانی و رهبری شما سپاسگزاریم!",
            "left": "شما از عضویت در کانال خارج شده‌اید. لطفاً برای استفاده از ربات دوباره عضو شوید.",
            "restricted": "دسترسی شما به کانال محدود شده است.",
        }
        persian_status = status_mapping.get(status, "وضعیت شما مشخص نیست! لطفاً وضعیت خود را بررسی کنید.")
        message = (
            "<b>✨ اطلاعات وضعیت کاربر ✨</b>\n\n"
            f"📌 <b>نام:</b> {user.first_name} {user.last_name or ''}\n"
            f"🔹 <b>شناسه:</b> {user_identifier}\n"
            f"📢 <b>وضعیت:</b> <i>{persian_status}</i>\n\n"
            f"📊 <b>تعداد درخواست‌های شما امروز:</b> {user_requests_today}\n"
            f"{END_MESSAGE}"
        )
        await query.message.reply_text(message, parse_mode="HTML", disable_web_page_preview=True)        
    except telegram.error.BadRequest as e:
        log_message(f"❌ Error fetching user status: {e}")
        await query.message.reply_text("⚠️ Unable to retrieve user status. Please try again later.")

async def show_currency_list(query):
    keyboard = []
    row = []
    count = 0
    for symbol, name in CURRENCY_LIST.items():
        row.append(InlineKeyboardButton(name, callback_data=f"currency_{symbol}"))
        count += 1
        if count % 3 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("📋 انتخاب ارز مورد نظر:", reply_markup=reply_markup)

async def send_cryptocurrency_price_update_to_user(query):
    await query.answer()
    prices = await get_nobitex_prices()
    if not prices:
        log_message("No prices available.")
        wrong_message_lines = [
            "⚠️ درحال حاضر قیمت‌ها در دسترس نمی‌باشد. لطفا بعدا تلاش نمائید.",
            ""
        ]
        wrong_message_lines.append(END_MESSAGE)
        await query.message.reply_text("\n".join(wrong_message_lines))
        return    
    stats = prices.get('stats', {})
    if not stats:
        log_message("Stats data not available.")
        wrong_message_lines = [
            "⚠️ درحال حاضر قیمت‌ها در دسترس نمی‌باشد. لطفا بعدا تلاش نمائید.",
            ""
        ]
        wrong_message_lines.append(END_MESSAGE)
        await query.message.reply_text("\n".join(wrong_message_lines))
        return
    
    rial_stats = {k: v for k, v in stats.items() if k.endswith('-rls')}
    sorted_stats = sorted(rial_stats.items(), key=lambda item: float(item[1].get('volumeDst', 0)), reverse=True)
    top_10 = sorted_stats[:10]
    
    if not any(symbol.startswith('eth') for symbol, _ in top_10):
        if 'eth-rls' in rial_stats:
            top_10.append(('eth-rls', rial_stats['eth-rls']))
    if not any(symbol.startswith('btc') for symbol, _ in top_10):
        if 'btc-rls' in rial_stats:
            top_10.append(('btc-rls', rial_stats['btc-rls']))

    persian_date, formatted_time = get_persian_datetime()

    message_lines = [
        "💰💱 آخرین قیمت ارزهای دیجیتال - طلای شهریور",
        f"⏰ آخرین بروزرسانی: {to_persian_number(formatted_time)}",
        f"📅 قیمت‌ها امروز: {to_persian_number(persian_date)}",
        ""
    ]
    for symbol, data in top_10:
        name = symbol.upper().replace("-RLS", "")
        try:
            price_rial = float(data.get('bestSell', 0))
            formatted_price = format_rial_to_toman(price_rial)
            message_lines.append(f"🔹 {name}: {formatted_price}")            
        except Exception as e:
            log_message(f"Error formatting {symbol}: {e}")
    message_lines.append(END_MESSAGE)
    try:
        await query.message.reply_text("\n".join(message_lines))        
        if formatted_time == "20:20":
            log_message("✅ Top 10 cryptocurrency prices sent to user!")
    except telegram.error.TelegramError as e:
        log_message(f"Error sending message to user: {e}")

async def get_nobitex_prices():
    global _NOBITEXT_CACHE
    now = time.time()
    if 'timestamp' in _NOBITEXT_CACHE:
        if now - _NOBITEXT_CACHE['timestamp'] < CACHE_TTL_SECONDS:
            return _NOBITEXT_CACHE['data']

    market_stats_url = BASE_NOBITEXT_URL + '/market/stats'
    try:
        response = requests.get(url=market_stats_url)        
        response.raise_for_status()
        data = response.json()
        _NOBITEXT_CACHE = { 'timestamp': now, 'data': data }
        # log_message("Nobitex Response: " + json.dumps(data, indent=2, ensure_ascii=False))  # <-- Add this
        return data
    except Exception as e:
        log_message(f"Error fetching prices from Nobitex: {e}")
        return None

async def get_currency_country_prices():
    global _CURRENCY_COUNTRY_CACHE
    now = time.time()
    if 'timestamp' in _CURRENCY_COUNTRY_CACHE:
        if now - _CURRENCY_COUNTRY_CACHE['timestamp'] < CACHE_TTL_SECONDS:
            return _CURRENCY_COUNTRY_CACHE['data']
    try:
        prices = get_prices()
        if not prices:
            log_message("No prices available.")
            return
        
        _CURRENCY_COUNTRY_CACHE = {
            'timestamp': now,
            'data': prices
        }
        return prices
    except Exception as e:
        log_message(f"Error fetching currency country prices: {e}")
        return None
    
async def send_foreign_currency_prices(update: Update, context: CallbackContext):
    def is_valid(value):
        return value not in (0, "0", "N/A", "N.A", None, "")

    prices = await get_currency_country_prices()
    if not prices:
        await update.callback_query.message.reply_text("❌ خطا در دریافت اطلاعات.")
        return
    
    persian_date, formatted_time = get_persian_datetime()

    lines = [
        "💰💱 آخرین قیمت ارز کشورهای خارجی - طلای شهریور",
        f"⏰ آخرین بروزرسانی: {to_persian_number(formatted_time)}",
        f"📅 قیمت‌ها امروز: {to_persian_number(persian_date)}",
        ""
        ]
    for title_fa, code in CURRENCIES_COUNTRY_LIST.items():
        value = prices.get(code)
        if value:
            if is_valid(value=value):
                lines.append(f"▫️ {title_fa}: {to_persian_number(value)} تومان")
    
    lines.append(END_MESSAGE)
    message = "\n".join(lines)
    await update.callback_query.message.reply_text(message)

async def send_symbol_price(query, currency_symbol: str):
    await query.answer()
    currency_name = CURRENCY_LIST.get(currency_symbol, "Unknown Currency")        
    symbol_price = await get_currency_price(currency_symbol=currency_symbol.upper())
    response_message = f"📊 آخرین اطلاعات ارز {currency_name} - طلای شهریور\n\n"
    response_message += f"✅ نام ارز: {currency_name}\n"
    response_message += f"🔸 نماد: {currency_symbol.upper()}\n"
    if symbol_price:
        response_message += symbol_price
    else:
        response_message += f"💸 قیمت: اطلاعات قیمت در دسترس نیست\n"
    await query.message.reply_text(response_message)

async def get_currency_price(currency_symbol: str):
    data = await get_nobitex_prices()
    if not data:
        return f"❌ داده‌ای برای {currency_symbol} یافت نشد."
    # log_message(data)
    key = f"{currency_symbol.lower()}-rls"
    price_info = data.get('stats', {}).get(key)
    if price_info:
        day_low = format_rial_to_toman(price_info.get('dayLow'))
        day_high = format_rial_to_toman(price_info.get('dayHigh'))
        best_buy = format_rial_to_toman(price_info.get('bestBuy'))
        best_sell = format_rial_to_toman(price_info.get('bestSell'))

        return (
            f"📉 پایین‌ترین قیمت امروز: {day_low}\n"
            f"📈 بالاترین قیمت امروز: {day_high}\n"
            f"💸 بهترین خرید: {best_buy}\n"
            f"💰 بهترین فروش: {best_sell}\n"
            f"{END_MESSAGE}"
        )
    else:
        return f"❌ قیمت ارز {currency_symbol.upper()} در داده‌ها موجود نیست."

async def send_price_update_to_user(query):
    await query.answer()
    prices = get_prices()
    if not prices:
        log_message("No prices available.")
        wrong_message_lines = [
            "⚠️ درحال حاضر قیمت‌ها در دسترس نمی‌باشد. لطفا بعدا تلاش نمائید.",
            ""
        ]
        wrong_message_lines.append(END_MESSAGE)
        await query.message.reply_text("\n".join(wrong_message_lines))
        return
    
    ap_date, f_time = get_persian_datetime()
    weekday = get_persian_weekday_from_jdate(ap_date)
    fa_date = get_farsi_date()
    farsi_date = f'{weekday} {fa_date}'
    message = make_price_message(prices=prices, f_time=f_time, farsi_date=farsi_date, ap_date=ap_date)
    try:
        await query.message.reply_text(message)
        if f_time == "20:20":
            log_message("✅ Prices of gold and coin sent to user!")
    except telegram.error.TelegramError as e:
        log_message(f"Error sending message to user: {e}")

async def send_price_update():
    prices = get_prices()
    if not prices:
        log_message("No prices available.")        
        return
    
    # Build WordPress post and Telegram message
    ap_date, f_time = get_persian_datetime()
    fa_date = get_farsi_date()
    weekday = get_persian_weekday_from_jdate(ap_date)
    post_title = f"قیمت طلا و سکه امروز {weekday} {fa_date} - بروزرسانی {f_time}"
    slug = f"gold-coin-prices-today-{ap_date.replace('/', '-')}-{f_time.replace(':', '')}"
    post_content = build_post_html(prices=prices, f_time=f_time, fa_date=fa_date, weekday=weekday)
    farsi_date = f'{weekday} {fa_date}'
    log_message(f"slug: {slug} - post title: {post_title}")

    post_link = None
    try:
        post_link, short_link = publish_post(title=post_title, content=post_content, slug=slug)
    except Exception as e:
        log_message(f"❌ Error publishing to WordPress: {e}")
    
    message = make_price_message(prices=prices, f_time=f_time, farsi_date=farsi_date, ap_date=ap_date)
    if post_link:
        safe_title = html.escape(post_title)
        message += f'\n✅ <a href="{post_link}">{safe_title}</a>'
        message += f'\n\n🔗 {post_link}'

    try:
        # Send Telegram message
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")
        if f_time == "20:20":
            log_message("✅ Prices of gold and coin sent!")
    except telegram.error.TelegramError as e:
        log_message(f"❌ Error sending Telegram message: {e}")

    # ------------------------------------------------------------------
    # Inside send_price_update() – replace the X block
    # ------------------------------------------------------------------
    # Comment should be check authorization for X posting before trying to post.
    # try:
    #     # ----- X (Twitter) -----
    #     x_message = build_post_for_x(prices=prices, f_time=f_time, farsi_date=farsi_date, link=post_link)
    #     log_message("Preparing X post …")
    #     success = await post_price_update_to_x(x_message)
    #     log_message("✅ X post succeeded" if success else "❌ X post failed")
    # except Exception as exc:
    #     log_message(f"❌ Unexpected X error: {exc}")

async def start(update: Update, context: CallbackContext):
    if update.message:
        user_id = update.message.from_user.id
    elif update.callback_query:
        user_id = update.callback_query.from_user.id
        await update.callback_query.answer()

    if user_id in ADMIN_IDs:
        keyboard = [
            [InlineKeyboardButton("📢 ارسال آخرین قیمت به کانال", callback_data='send_prices_to_message')],
            [InlineKeyboardButton("💰 دریافت آخرین تغییرات قیمت طلا و سکه", callback_data='get_new_prices')],
            [InlineKeyboardButton("💱 دریافت قیمت ارزهای دیجیتال", callback_data='get_currency_prices')],
            [InlineKeyboardButton("🌍 دریافت قیمت ارز کشورهای خارجی", callback_data='get_foreign_currency_prices')],
            [InlineKeyboardButton("📋 مشاهده لیست ارزها", callback_data='show_currency_list')],
            [InlineKeyboardButton("ℹ️ وضعیت من ℹ️", callback_data='get_status')],
            [InlineKeyboardButton("🔍 بررسی عضویت من", callback_data='check_user_status')],
            [InlineKeyboardButton("گرفتن اطلاعات کاربران", callback_data='get_users_info')],
            # [InlineKeyboardButton("رفع محدودیت کاربر", callback_data=f"remove_restriction")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("💰 دریافت آخرین تغییرات قیمت طلا و سکه", callback_data='get_new_prices')],
            [InlineKeyboardButton("💱 دریافت قیمت ارزهای دیجیتال", callback_data='get_currency_prices')],
            [InlineKeyboardButton("🌍 دریافت قیمت ارز کشورهای خارجی", callback_data='get_foreign_currency_prices')],
            [InlineKeyboardButton("📋 مشاهده لیست ارزها", callback_data='show_currency_list')],
            # [InlineKeyboardButton("ℹ️ وضعیت من ℹ️", callback_data='get_status')],
            [InlineKeyboardButton("🔍 بررسی عضویت من", callback_data='check_user_status')]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("لطفاً یک گزینه را انتخاب کنید:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text("لطفاً یک گزینه را انتخاب کنید:", reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data
    await check_and_store_user(user_id)

    if data == "check_user_status":
        await check_user_membership_status(query=query, user_id=user_id)
    elif data == "get_status":
        await user_status_message(query=query, user_id=user_id)
    elif data == "get_currency_prices":
        if user_id not in ADMIN_IDs and not await check_request_limit(query):
            return
        await send_cryptocurrency_price_update_to_user(query)
    elif data == "get_foreign_currency_prices":
        if user_id not in ADMIN_IDs and not await check_request_limit(query):
            return
        await send_foreign_currency_prices(update=update, context=context)
    elif data == "show_currency_list":
        await show_currency_list(query=query)
        return
    elif data.startswith("currency_"):
        if user_id not in ADMIN_IDs and not await check_request_limit(query):
            return
        currency_symbol = data.split("_")[1]        
        await send_symbol_price(query=query, currency_symbol=currency_symbol)
    elif data == "back_to_main_menu":
        await start(update, context)
        return
    elif data == "get_new_prices":
        if user_id not in ADMIN_IDs and not await check_request_limit(query):
            return
        await send_price_update_to_user(query)
    elif data == "send_prices_to_message":
        if user_id in ADMIN_IDs:
            await send_price_update()
            await query.message.reply_text("✅ قیمت‌ها به وبسایت و کانال ارسال شد.\nطلای شهریور\n🌐 @talayeshahrivar | https://talayeshahrivar.ir")
        else:
            await query.message.reply_text("❌ شما دسترسی به این گزینه ندارید. تنها مدیر می‌تواند قیمت‌ها را به وبسایت و کانال ارسال کند.")
    elif data == "get_users_info":
        if user_id in ADMIN_IDs:
            await get_users_info()
            await query.message.reply_text("✅ اطلاعات کاربران ذخیره شد.")
    else:
        await query.message.reply_text(UNRECOGNIZED_COMMAND_MESSAGE)

    await start(update, context)
