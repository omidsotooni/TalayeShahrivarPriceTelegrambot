import requests # type: ignore
import json
from datetime import datetime
import os

url = "https://call4.tgju.org/ajax.json"

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
        
def to_persian_number(n):
    mapping = {"0":"۰","1":"۱","2":"۲","3":"۳","4":"۴","5":"۵", "6":"۶","7":"۷","8":"۸","9":"۹"}
    return "".join(mapping.get(ch, ch) for ch in str(n))
        
def fetch_data():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    response = requests.get(url,headers=headers, timeout=5)
    response.raise_for_status()
    data = response.json()

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
        "time_ir": p.get("base_global_lead", {}).get("t"),
        "time_en": p.get("base_global_lead", {}).get("t_en")
    }

def save_latest(rawData):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = os.path.join(DATA_DIR, "latest_prices.json")
    data = {
        "timestamp": datetime.now().isoformat(),
        "raw": rawData
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data["timestamp"]

if __name__ == "__main__":
    rawData = fetch_data()
    # print("Raw:\n", rawData)
    timestamp = save_latest(rawData)
    print("✅ Saved latest prices, timestamp:", timestamp)
