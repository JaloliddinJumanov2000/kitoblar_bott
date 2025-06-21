from aiogram import Router
from aiogram.types import Message

from handlers import start_router

router = Router()

@start_router.message()
async def unknown_message(message: Message):
    await message.answer("Kechirasiz, bu buyruqni tushunmadim. Iltimos, /start yozing.")