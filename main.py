import os
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import asyncio

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GIGACHAT_AUTH_KEY = os.getenv("GIGACHAT_AUTH_KEY")
GIGACHAT_API_URL = os.getenv("GIGACHAT_API_URL")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

async def generate_post_gigachat(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GIGACHAT_AUTH_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GIGACHAT_API_URL, headers=headers, json=payload)
        data = response.json()
        return data["choices"][0]["message"]["content"]

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Напишите /post и тему поста.")

@dp.message(Command("post"))
async def post_handler(message: Message):
    await message.answer("Введите тему поста:")

    @dp.message()
    async def get_topic(topic_message: Message):
        topic = topic_message.text
        prompt = f"Напиши пост для Telegram на тему: {topic}. Добавь эмодзи, заголовок и абзацы."
        post_text = await generate_post_gigachat(prompt)
        await topic_message.answer(post_text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
