import pytz

# Set Tehran time zone
TEHRAN_TZ = pytz.timezone("Asia/Tehran")

# Telegram bot credentials  (FILL IN YOUR OWN VALUES)
BOT_TOKEN = ""            # token from @BotFather
CHAT_ID = 0               # your channel ID, e.g. -100xxxxxxxxxx
ADMIN_IDs = set()         # Telegram user IDs of admins, e.g. {111111111, 222222222}
CHANNEL_USERNAME = "@talayeshahrivar"
MAX_REQUESTS_MEMBER = 10
MAX_REQUESTS_NON_MEMBER = 5
USER_REQUESTS = {}
USER_CACHE = {}
_NOBITEXT_CACHE = {}
_CURRENCY_COUNTRY_CACHE = {}
CACHE_TTL_SECONDS = 80
USER_FILE = 'user_ids.txt'
ENTER_USER_ID = 0

# WordPress  (FILL IN YOUR OWN VALUES)
LOGOURL = "https://talayeshahrivar.ir/wp-content/uploads/2024/12/logo-golden-shahrivar-01.svg"
BASENEWS_URL = "https://talayeshahrivar.ir/news/gold-coin-prices-today-"
WP_URL = "https://talayeshahrivar.ir/wp-json/wp/v2/news"
WP_MEDIA_URL = "https://talayeshahrivar.ir/wp-json/wp/v2/media/"
BASETAGNEWS = "https://talayeshahrivar.ir/news-tag"
WP_USER = ""
WP_APP_PASS = ""
EXCEL_FILE = ""

# API URLs and headers
TGJU_API = "https://call4.tgju.org/ajax.json"
TGJU_ENDPOINTS = [
    "https://call4.tgju.org/ajax.json",
    "https://call3.tgju.org/ajax.json",
    "https://call2.tgju.org/ajax.json",
    "https://call5.tgju.org/ajax.json",
]
BASE_NOBITEXT_URL = "https://apiv2.nobitex.ir/"
API_URL = "https://www.tala.ir/banner/"
HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en,fa;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://www.tala.ir/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
# Optional: add your own browser cookie for tala.ir if needed
# HEADERS["Cookie"] = ""


PERSIAN_MONTHS = {
    1: "فروردین",
    2: "اردیبهشت",
    3: "خرداد",
    4: "تیر",
    5: "اَمرداد",
    6: "شهریور",
    7: "مهر",
    8: "آبان",
    9: "آذر",
    10: "دی",
    11: "بهمن",
    12: "اسفند",
}
PERSIAN_WEEKDAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه", "جمعه"]
MONTHS_TAG_NEWS = {
    654: "فروردین ماه",
    655: "اردیبهشت ماه",
    656: "خرداد ماه",
    657: "تیر ماه",
    658: "اَمرداد ماه",
    659: "شهریور ماه",
    660: "مهر ماه",
    661: "آبان ماه",
    662: "آذر ماه",
    663: "دی ماه",
    664: "بهمن ماه",
    665: "اسفند ماه",
}

VALID_STATUSES = ["member", "administrator", "creator"]
END_MESSAGE = (
    "\n"
    "🌟 Shine rich with us\n"
    "💛 با ما ثروتمند بدرخشید\n"
    "#طلای_مینیمال #قیمت_طلا #قیمت_سکه #قیمت_طلا_امروز #قیمت_سکه_امروز #ارز_دیجیتال #قیمت_ارز_دیجیتال\n"
    "\n"
    "📞 سفارش و مشاوره:\n"
    "📲 +989153678924 | +989917432796\n"
    "\n"
    "🔰 در شبکه‌های اجتماعی همراه ما باشید:\n"
    "🌐 @talayeshahrivar | https://talayeshahrivar.ir"
)
UNRECOGNIZED_COMMAND_MESSAGE = "درخواست شما قابل تشخیص نمیباشد، لطفا از گزینه های بالا یکی را انتخاب نمائید یا گزینه /start را بزنید."
CURRENCY_LIST = {
    "btc": "Bitcoin",
    "eth": "Ethereum",
    "ltc": "Litecoin",
    "usdt": "Tether",
    "xrp": "Ripple",
    "bch": "Bitcoin Cash",
    "bnb": "Binance Coin",
    "eos": "EOS",
    "xlm": "Stellar",
    "etc": "Ethereum Classic",
    "trx": "TRON",
    "doge": "Dogecoin",
    "uni": "Uniswap",
    "dai": "DAI",
    "link": "Chainlink",
    "dot": "Polkadot",
    "aave": "Aave",
    "ada": "Cardano",
    "shib": "Shiba Inu",
    "ftm": "Fantom",
    "matic": "Polygon",
    "mana": "Decentraland",
    "avax": "Avalanche",
    "atom": "Cosmos",
    "ton": "TON (Telegram)",
    "mask": "Mask Network",
    "algo": "Algorand",
    "omg": "OMG Network",
    "rdnt": "Radiant",
    "sushi": "SushiSwap",
    "bal": "Balancer",
    "not": "Notcoin",
    "xmr": "Monero",
    "fil": "Filecoin",
    "sol": "Solana",
    "1m_btt": "1M BitTorrent",
    "ethfi": "Ether.fi",
    "arb": "Arbitrum",
    "fet": "Fetch.ai",
    "skl": "SKALE",
    "chz": "Chiliz",
    "xtz": "Tezos",
    "1m_pepe": "1M Pepe",
    "usdc": "USD Coin",
}

CURRENCIES_COUNTRY_LIST = {
    "$ دلار": "usd",
    "€ یورو": "eur",
    "د.إ درهم امارات": "aed",
    "£ پوند انگلیس": "gbp",
    "₺ لیر ترکیه": "try",
    "₣ فرانک سوئیس": "chf",
    "¥ یوان چین": "cny",
    "$ دلار کانادا": "cad",
    "$ دلار استرالیا": "aud",
    "؋ افغانی": "afn",
    "ريال عمان": "omr",
    "¥ ین ژاپن": "jpy",
}

FEATURED_MEDIA_NEWS = {
    1:  [8081, 8082],
    2:  [8083, 8084],
    3:  [8085, 8086],
    4:  [8087, 8088],
    5:  [8089, 8090],
    6:  [8091, 8092],
    7:  [8093, 8094],
    8:  [8095, 8096],
    9:  [8097, 8098],
    10: [8099, 8100],
    11: [8101, 8102],
    12: [8103, 8104],
    13: [8105, 8106],
    14: [8107, 8108],
    15: [8109, 8110],
    16: [8111, 8112],
    17: [8113, 8114],
    18: [8115, 8116],
    19: [8117, 8118],
    20: [8119, 8120],
    21: [8121, 8122],
    22: [8123, 8124],
    23: [8125, 8126],
    24: [8127, 8128],
    25: [8129, 8130],
    26: [8131, 8132],
    27: [8133, 8134],
    28: [8135, 8136],
    29: [8137, 8138],
    30: [8139, 8140],
}

# X (Twitter) API Credentials  (FILL IN YOUR OWN VALUES)
X_API_KEY = ""
X_API_SECRET = ""
X_ACCESS_TOKEN = ""
X_ACCESS_TOKEN_SECRET = ""
X_BEARER_TOKEN = ""