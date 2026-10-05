import jdatetime
from typing import Tuple
from datetime import datetime
from configs.app_config import BASENEWS_URL, MONTHS_TAG_NEWS, TEHRAN_TZ, PERSIAN_MONTHS, PERSIAN_WEEKDAYS, FEATURED_MEDIA_NEWS

# ===============================
# 📘 Utility Helpers
# ===============================
def log_message(message: str):
    persian_date, formatted_time = get_persian_datetime()
    file_path = "LogBot.txt"
    
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{persian_date} - {formatted_time} - {message}\n")
    
    print(f"Message logged to {file_path}")

def get_persian_datetime() -> Tuple[str, str]:
    now = datetime.now(TEHRAN_TZ)
    persian_datetime = jdatetime.datetime.fromgregorian(datetime=now)
    persian_date = persian_datetime.strftime('%Y/%m/%d')
    formatted_time = persian_datetime.strftime('%H:%M')
    return persian_date, formatted_time

def get_farsi_date() -> str:
    now = datetime.now(TEHRAN_TZ)
    persian_datetime = jdatetime.datetime.fromgregorian(datetime=now)
    day = persian_datetime.day
    month = PERSIAN_MONTHS[persian_datetime.month]
    year = persian_datetime.year
    return f"{day} {month} {year}"

def get_farsi_month_year() -> Tuple[int, int]:
    now = datetime.now(TEHRAN_TZ)
    persian_datetime = jdatetime.datetime.fromgregorian(datetime=now)
    month = persian_datetime.month
    year = persian_datetime.year
    return month, year

def get_persian_weekday_from_jdate(persian_date_str: str) -> str:
    year, month, day = map(int, persian_date_str.split("/"))
    jd = jdatetime.date(year, month, day)
    return PERSIAN_WEEKDAYS[jd.weekday()]

def parse_price(value, to_toman=False):
    if value is None:
        return "N/A"
    
    if isinstance(value, str):
        value = value.replace(",", "").replace("/", ".")
    try:
        value = float(value)
        if to_toman:
            value = value // 10

        formatted = f"{int(value):,}"
        return to_persian_number(formatted)
    except ValueError:
        return value
    
def format_rial_to_toman(value):
    try:
        formatted = f"{int(float(value) // 10):,} تومان"
        return to_persian_number(formatted)
    except (ValueError, TypeError):
        return "اطلاعات موجود نیست"
  
def get_yesterday_today_tomorrow_urls() -> Tuple[str, str, str, str, str, str]:
    today_j = jdatetime.date.today()
    yesterday_j = today_j - jdatetime.timedelta(days=1)
    tomorrow_j = today_j + jdatetime.timedelta(days=1)

    yesterday_url = f"{BASENEWS_URL}{yesterday_j.year}-{yesterday_j.month:02d}-{yesterday_j.day:02d}-1212/"
    today_url = f"{BASENEWS_URL}{today_j.year}-{today_j.month:02d}-{today_j.day:02d}-1212/"
    tomorrow_url = f"{BASENEWS_URL}{tomorrow_j.year}-{tomorrow_j.month:02d}-{tomorrow_j.day:02d}-1212/"

    def format_date(d: jdatetime.date) -> str:
        return f"{d.day} {PERSIAN_MONTHS[d.month]} {d.year}"

    yesterday_fa = format_date(yesterday_j)
    today_fa = format_date(today_j)
    tomorrow_fa = format_date(tomorrow_j)

    return (
        yesterday_url, today_url, tomorrow_url,
        yesterday_fa, today_fa, tomorrow_fa
    )

def get_current_month_tag_id() -> int:
    persian_date = jdatetime.date.today()
    month_name = f"{PERSIAN_MONTHS[persian_date.month]} ماه"
    for tag_id, name in MONTHS_TAG_NEWS.items():
        if name == month_name:
            return tag_id
    raise ValueError(f"Month tag not found for {month_name}")

def get_featured_media_for_today(slug: str) -> int:
    try:
        time_code = slug.split('-')[-1].replace('/', '')
    except Exception:
        time_code = "0000"

    persian_today = jdatetime.date.today()
    day = persian_today.day
    media_pair = FEATURED_MEDIA_NEWS.get(day)
    if not media_pair:
        media_pair = FEATURED_MEDIA_NEWS[max(FEATURED_MEDIA_NEWS.keys())]

    if time_code == "1212":
        return media_pair[0]
    elif time_code == "1717":
        return media_pair[1]
    else:
        return 5642

def to_persian_number(n):
    mapping = {"0":"۰","1":"۱","2":"۲","3":"۳","4":"۴","5":"۵", "6":"۶","7":"۷","8":"۸","9":"۹"}
    return "".join(mapping.get(ch, ch) for ch in str(n))