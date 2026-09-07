from pydantic import BaseModel
from typing import Dict, Optional

class RatesResponse(BaseModel):
    base: str = "RUB"
    date: str
    rates: Dict[str, float]

class ConvertResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    result: float
    rate: Optional[float] = None
