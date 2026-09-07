# Currency Calculator (ЦБ РФ) — микросервис

## Описание
Микросервис предоставляет API для получения официальных курсов валют ЦБ РФ (топ-20) и конвертации сумм. Кэширует курсы на 24 часа.

## Запуск (локально)
1. Убедитесь, что установлен Python 3.10+.
2. Запустите `setup.bat` (Windows) или выполните вручную:
   - `python -m venv venv`
   - `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (Linux)
   - `pip install -r requirements.txt`
   - `uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`
3. Откройте http://localhost:8000/docs для Swagger-документации.

## API Endpoints
- `GET /rates` – все курсы к RUB.
- `GET /convert?from=USD&to=RUB&amount=100` – конвертация.

## Поддерживаемые валюты
USD, EUR, CNY, GBP, JPY, CHF, CAD, AUD, NZD, SGD, HKD, KRW, TRY, INR, BRL, ZAR, MXN, SEK, NOK, DKK, RUB.
