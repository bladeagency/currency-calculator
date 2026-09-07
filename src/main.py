from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Optional
from .models import RatesResponse, ConvertResponse
from .cache import cache
from .bank_rates import get_bank_rates, BANKS

app = FastAPI(
    title="Currency Calculator (ЦБ РФ)",
    description="Калькулятор валют + курсы 20 банков РФ",
    version="3.0.0"
)

import os

_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
with open(os.path.join(_TEMPLATE_DIR, 'index.html'), 'r', encoding='utf-8') as _f:
    HTML_PAGE = _f.read()

@app.get("/rates", response_model=RatesResponse)
async def get_rates():
    rates = cache.get_rates()
    date = cache.get_date()
    return RatesResponse(base="RUB", date=date, rates=rates)

@app.get("/convert", response_model=ConvertResponse)
async def convert_currency(
    from_: str = Query(..., alias="from"),
    to: str = Query(...),
    amount: float = Query(..., gt=0)
):
    rates = cache.get_rates()
    if from_ not in rates:
        raise HTTPException(status_code=404, detail=f"Валюта {from_} не найдена")
    if to not in rates:
        raise HTTPException(status_code=404, detail=f"Валюта {to} не найдена")
    rate_from = rates[from_]
    rate_to = rates[to]
    result = amount * (rate_from / rate_to)
    return ConvertResponse(
        from_currency=from_,
        to_currency=to,
        amount=amount,
        result=round(result, 6),
        rate=round(rate_from / rate_to, 6)
    )

@app.get("/bank-rates")
async def bank_rates():
    return get_bank_rates()

@app.get("/bank-rates/{bank_id}")
async def bank_rate_detail(bank_id: str):
    bank = get_bank_rates().get(bank_id)
    if not bank:
        raise HTTPException(status_code=404, detail=f"Банк {bank_id} не найден")
    return bank

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return HTMLResponse(HTML_PAGE)
