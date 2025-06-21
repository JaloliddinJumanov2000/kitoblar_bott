from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("search"))
async def search_handler(message: Message):
    try:
        text = message.text.strip()
        parts = text.split()

        if len(parts) < 2:
            await message.answer("""
🔍 Qidiruv
Format: /search <kalit_soz>
Misollar:
 Format: /search kalit_soz
 Misol: /search Alisher
            """)
            return

    except Exception as e:
        await message.answer(f"❌ Qidiruv xatoligi: {str(e)}")