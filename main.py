
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, WELCOME_TEXT, HELP_TEXT
from database import init_database
from handlers import add_book_handler, list_books_handler, search_books_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot va Dispatcher
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylida bo'lishi kerak!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(WELCOME_TEXT, parse_mode="Markdown")


@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(HELP_TEXT, parse_mode="Markdown")


@dp.message(Command("add_book"))
async def add_book_command(message: Message):
    await add_book_handler(message)


@dp.message(Command("books"))
async def books_command(message: Message):
    await list_books_handler(message)


@dp.message(Command("search"))
async def search_command(message: Message):
    await search_books_handler(message)


@dp.message()
async def unknown_handler(message: Message):
    await message.answer("""
❓ **Noma'lum komanda!**

**Mavjud komandalar:**
• `/start` - Boshlash
• `/help` - Yordam
• `/books` - Kitoblar ro'yxati
• `/add_book "nom" "muallif"` - Kitob qo'shish
• `/search kalit_so'z` - Qidirish

Batafsil: `/help`
    """, parse_mode="Markdown")


async def main():
    try:
        init_database()
        logger.info("🚀 Bot ishga tushmoqda...")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"❌ Bot xatoligi: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
