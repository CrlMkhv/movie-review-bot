import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from service.manager import ServiceManager

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()
manager = ServiceManager()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Введи название фильма отзывы о котором ты бы хотел узнать. ")

@dp.message()
async def handle(message: types.Message):
    await message.answer("Ищу отзывы, подожди...")
    result = manager.handle_query(message.text)
    await message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())