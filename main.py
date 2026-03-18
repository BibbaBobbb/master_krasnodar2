import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Максимально разрешающий CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых адресов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Order(BaseModel):
    name: str
    phone: str
    text: str = ""  # Необязательное поле


@app.post("/send-order")
async def send_to_tg(order: Order):
    TELEGRAM_TOKEN = "8770766301:AAEOsQKo-HKq7GrADxSTSchgJEOCJAlI9Ko"
    CHAT_ID = "8590584125"

    msg = (
        f"🚀 Новая заявка!\n"
        f"👤 Имя: {order.name}\n"
        f"📞 Тел: {order.phone}\n"
        f"💬 Сообщение: {order.text}"
    )

    # Важно: у Telegram API должен быть префикс /bot
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=15)

    if resp.status_code == 200:
        return {"status": "success"}
    else:
        return {"status": "error", "details": resp.text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
