import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

from gsheet import write_to_a1  # импорт функции записи в Google Sheet

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  # В aiogram 3.5.0 не передаем бот в конструктор


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Как тебя зовут?")


@dp.message()
async def handle_answer(message: types.Message):
    user_text = message.text
    try:
        write_to_a1(user_text)
        await message.answer(f"Спасибо! Я записал: {user_text}")
    except Exception as e:
        await message.answer(f"Ошибка при записи в Google Sheet: {e}")


async def main():
    print("Bot started")
    await dp.start_polling(bot)  # бот передается здесь


if __name__ == "__main__":
    asyncio.run(main())
