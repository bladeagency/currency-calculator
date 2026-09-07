import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, Optional

CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"

TOP_CURRENCIES = {
    "USD", "EUR", "CNY", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD",
    "SGD", "HKD", "KRW", "TRY", "INR", "BRL", "ZAR", "MXN", "SEK",
    "NOK", "DKK"
}

def fetch_cbr_rates() -> Dict[str, float]:
    try:
        response = httpx.get(CBR_URL, timeout=10.0)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        rates = {"RUB": 1.0}
        date_attr = root.attrib.get("Date", datetime.now().strftime("%d.%m.%Y"))
        for valute in root.findall("Valute"):
            char_code = valute.find("CharCode").text
            if char_code not in TOP_CURRENCIES:
                continue
            nominal = int(valute.find("Nominal").text)
            value_str = valute.find("Value").text.replace(",", ".")
            value = float(value_str)
            rates[char_code] = value / nominal
        rates["_date"] = date_attr
        return rates
    except Exception as e:
        print(f"Ошибка загрузки курсов ЦБ: {e}")
        return {}
