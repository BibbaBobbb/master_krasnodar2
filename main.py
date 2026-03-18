import os
import time
import re
import requests
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import sqlite3
from typing import List, Dict
from datetime import datetime

app = FastAPI()

# CORS (локальная разработка — без домена)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Загрузка .env (рядом с main.py) ---------
try:
    from dotenv import load_dotenv
    load_dotenv()  # без аргументов — ищет .env в текущей папке
except Exception:
    # Если python-dotenv не установлен, просто продолжаем — переменные могут быть заданы извне
    pass

# Секреты берём из окружения (не хардкодим в коде)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "")

# --------- Простые security-заголовки ----------
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    # Для локалки HSTS не добавляем
    return response

# --------- Простой rate limit (в памяти) ----------
RATE_LIMIT_BUCKETS: Dict[str, List[float]] = {}
RATE_LIMIT_MAX = 5       # 5 запросов
RATE_LIMIT_WINDOW = 60.0 # за 60 секунд

def client_key(req: Request) -> str:
    # Простой ключ по IP
    return req.client.host if req.client else "unknown"

def check_rate_limit(req: Request):
    now = time.time()
    key = client_key(req)
    bucket = RATE_LIMIT_BUCKETS.setdefault(key, [])
    # чистим старые события
    cutoff = now - RATE_LIMIT_WINDOW
    while bucket and bucket[0] < cutoff:
        bucket.pop(0)
    if len(bucket) >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=429, detail="Too Many Requests")
    bucket.append(now)

class Order(BaseModel):
    name: str
    phone: str
    text: str = ""  # Необязательное поле

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = (v or "").strip()
        if not (1 <= len(v) <= 50):
            raise ValueError("name length invalid")
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\s\-]+", v):
            raise ValueError("name has invalid characters")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = (v or "").strip()
        # Нормализуем: 8XXXXXXXXXX -> +7XXXXXXXXXX
        digits = re.sub(r"\D", "", v)
        if digits.startswith("8"):
            digits = "7" + digits[1:]
        if not digits.startswith("7"):
            digits = "7" + digits
        digits = digits[:11]
        phone = f"+{digits}"
        if not re.fullmatch(r"\+7\d{10}", phone):
            raise ValueError("phone must be +7XXXXXXXXXX")
        return phone


@app.post("/send-order")
async def send_to_tg(order: Order, request: Request):
    check_rate_limit(request)
    msg = (
        f"🚀 Новая заявка!\n"
        f"👤 Имя: {order.name}\n"
        f"📞 Тел: {order.phone}\n"
        f"💬 Сообщение: {order.text}"
    )

    # Важно: у Telegram API должен быть префикс /bot
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=15)

    if resp.status_code == 200:
        return {"status": "success"}
    else:
        return {"status": "error", "details": resp.text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import List
from datetime import datetime

app = FastAPI()

# Максимально разрешающий CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых адресов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------- SQLite (Отзывы) ---------------
DB_PATH = "reviews.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row
with conn:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            text TEXT NOT NULL,
            rating INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )


class ReviewIn(BaseModel):
    name: str
    text: str
    rating: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = (v or "").strip()
        if not (1 <= len(v) <= 50):
            raise ValueError("name length invalid")
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\s\-]+", v):
            raise ValueError("name has invalid characters")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = (v or "").strip()
        if not (1 <= len(v) <= 1000):
            raise ValueError("text length invalid")
        return v

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: int) -> int:
        if not (1 <= int(v) <= 5):
            raise ValueError("rating must be 1..5")
        return int(v)


@app.post("/reviews")
async def create_review(review: ReviewIn, request: Request):
    check_rate_limit(request)
    # Сохраняем в БД
    created_at = datetime.utcnow().isoformat()
    with conn:
        conn.execute(
            "INSERT INTO reviews (name, text, rating, created_at) VALUES (?, ?, ?, ?)",
            (review.name, review.text, review.rating, created_at),
        )
    # Уведомление в Telegram
    tg_text = f"Новый отзыв от {review.name}: {review.text}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": tg_text}, timeout=10)
    except Exception:
        # Не мешаем успешному ответу, даже если Telegram недоступен
        pass
    return {"status": "success"}


@app.get("/reviews")
async def list_reviews():
    cur = conn.execute(
        "SELECT id, name, text, rating, created_at FROM reviews ORDER BY datetime(created_at) DESC, id DESC"
    )
    rows = [dict(r) for r in cur.fetchall()]
    return rows


@app.delete("/reviews/by-name/{name}")
async def delete_review_by_name(name: str, x_api_key: str | None = Header(default=None)):
    if not ADMIN_API_KEY or x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")
    with conn:
        cur = conn.execute("DELETE FROM reviews WHERE name = ?", (name,))
    return {"deleted": cur.rowcount}


@app.delete("/reviews/{review_id}")
async def delete_review_by_id(review_id: int, x_api_key: str | None = Header(default=None)):
    if not ADMIN_API_KEY or x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")
    with conn:
        cur = conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    return {"deleted": cur.rowcount}
