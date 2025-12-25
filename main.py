import asyncio
import os
import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from gsheet import append_user_row

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Словарь для хранения состояния пользователей
user_states = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    unique_id = str(uuid.uuid4())

    # Создаем или обновляем состояние пользователя
    user_states[user_id] = {
        "unique_id": unique_id,
        "step": "name",
        "data": {}
    }
    await message.answer("Привет! Как тебя зовут?")

@dp.message()
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state:
        await message.answer("Отправьте /start для начала.")
        return

    step = state["step"]
    text = message.text.strip()

    if step == "name":
        state["data"]["name"] = text
        state["step"] = "city"
        await message.answer("В каком городе ты живёшь?")
    elif step == "city":
        state["data"]["city"] = text
        state["step"] = "birthdate"
        await message.answer("Укажи дату рождения (например, 25.12.2000)")
    elif step == "birthdate":
        state["data"]["birthdate"] = text
        state["step"] = "done"

        # Формируем строку для Google Sheet
        row = [
            state["unique_id"],
            state["data"]["name"],
            state["data"]["city"],
            state["data"]["birthdate"]
        ]
        try:
            append_user_row(row)
            await message.answer("Спасибо! Все данные записаны.")
        except Exception as e:
            await message.answer(f"Ошибка при записи в таблицу: {e}")

        # Удаляем состояние пользователя
        del user_states[user_id]

async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
