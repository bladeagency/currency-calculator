import time
from typing import Dict, Optional
from .cbr_client import fetch_cbr_rates

CACHE_TTL_SECONDS = 24 * 60 * 60

class RatesCache:
    def __init__(self):
        self._data: Optional[Dict[str, float]] = None
        self._timestamp: float = 0
        self._date: str = ""

    def get_rates(self) -> Dict[str, float]:
        now = time.time()
        if self._data is None or (now - self._timestamp) > CACHE_TTL_SECONDS:
            new_data = fetch_cbr_rates()
            if new_data:
                self._date = new_data.pop("_date", "")
                self._data = new_data
                self._timestamp = now
            else:
                if self._data is None:
                    self._data = {"RUB": 1.0, "USD": 75.0, "EUR": 85.0}
                    self._date = "запасной курс"
        return self._data

    def get_date(self) -> str:
        return self._date

cache = RatesCache()
