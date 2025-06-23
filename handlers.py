"""
Bot handlerlari
"""
import logging
from typing import List
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Book

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Start komandasi handler"""
    welcome_text = """
🎉 <b>Kitoblar Bot</b>ga xush kelibsiz!

Bu bot sizning shaxsiy kitoblar kolleksiyangizni boshqarish uchun mo'ljallangan.

📚 <b>Qanday foydalanish:</b>
• /add_book "kitob nomi" "muallif" - Yangi kitob qo'shish
• /books - Barcha kitoblar ro'yxati
• /search kalit_soz - Kitoblarni qidirish
• /help - Yordam

Boshlaymizmi? 🚀
    """
    await message.answer(welcome_text, parse_mode="HTML")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Yordam komandasi"""
    help_text = """
📖 <b>Kitoblar Bot - Yordam</b>

<b>Mavjud komandalar:</b>

🔹 <code>/start</code> - Botni ishga tushirish
🔹 <code>/help</code> - Bu yordam xabari
🔹 <code>/books</code> - Barcha kitoblar ro'yxati
🔹 <code>/add_book "sarlavha" "muallif"</code> - Yangi kitob qo'shish  
🔹 <code>/search kalit_soz</code> - Kitoblarni qidirish

<b>Misollar:</b>
• <code>/add_book "Dunyoning ishlari" "O'tkir Hoshimov"</code>
• <code>/add_book "Saodat Asri" "Abdulla Qodiriy"</code>  
• <code>/search doston</code>
• <code>/search Alisher</code>

❓ Savollaringiz bo'lsa, /help buyrug'ini ishlating.
    """
    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("add_book"))
async def cmd_add_book(message: Message) -> None:
    """Kitob qo'shish komandasi"""
    try:
        # Komandadan keyin kelgan matnni olish
        command_args = message.text.split(maxsplit=1)
        if len(command_args) < 2:
            await message.answer(
                "❌ Noto'g'ri format!\n\n"
                "To'g'ri format: <code>/add_book \"kitob nomi\" \"muallif\"</code>\n"
                "Misol: <code>/add_book \"Dunyoning ishlari\" \"O'tkir Hoshimov\"</code>",
                parse_mode="HTML"
            )
            return
        
        # Qo'shtirnoqlarni qayta ishlash
        args_text = command_args[1]
        
        # Oddiy parsing (qo'shtirnoqlarsiz)
        if '"' not in args_text:
            parts = args_text.split(maxsplit=1)
            if len(parts) < 2:
                await message.answer(
                    "❌ Kitob nomi va muallifni kiriting!\n\n"
                    "Format: <code>/add_book \"kitob nomi\" \"muallif\"</code>",
                    parse_mode="HTML"
                )
                return
            title, author = parts[0], parts[1]
        else:
            # Qo'shtirnoqli parsing
            try:
                parts = []
                current_part = ""
                in_quotes = False
                i = 0
                
                while i < len(args_text):
                    char = args_text[i]
                    if char == '"':
                        if in_quotes:
                            if current_part.strip():
                                parts.append(current_part.strip())
                            current_part = ""
                            in_quotes = False
                        else:
                            in_quotes = True
                    elif in_quotes:
                        current_part += char
                    elif char == ' ' and current_part.strip():
                        parts.append(current_part.strip())
                        current_part = ""
                    elif char != ' ':
                        current_part += char
                    i += 1
                
                if current_part.strip():
                    parts.append(current_part.strip())
                
                if len(parts) < 2:
                    raise ValueError("Kitob nomi va muallif kerak")
                
                title, author = parts[0], parts[1]
                
            except Exception:
                await message.answer(
                    "❌ Noto'g'ri format!\n\n"
                    "To'g'ri format: <code>/add_book \"kitob nomi\" \"muallif\"</code>\n"
                    "Misol: <code>/add_book \"Dunyoning ishlari\" \"O'tkir Hoshimov\"</code>",
                    parse_mode="HTML"
                )
                return
        
        # Ma'lumotlar bazasiga saqlash
        async for session in get_session():
            book = await Book.create(session, title=title, author=author)
            await message.answer(
                f"✅ <b>Kitob muvaffaqiyatli qo'shildi!</b>\n\n"
                f"📖 <b>Nomi:</b> {book.title}\n"
                f"✍️ <b>Muallif:</b> {book.author}\n"
                f"🆔 <b>ID:</b> {book.id}",
                parse_mode="HTML"
            )
            break
            
    except Exception as e:
        logger.error(f"Kitob qo'shishda xato: {e}")
        await message.answer(
            "❌ Kitob qo'shishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
        )


@router.message(Command("books"))
async def cmd_books(message: Message) -> None:
    """Barcha kitoblar ro'yxati"""
    try:
        async for session in get_session():
            books = await Book.get_all(session, limit=50)
            total_count = await Book.count(session)
            
            if not books:
                await message.answer("📚 Hozircha kitoblar yo'q. Birinchi kitobingizni /add_book yordamida qo'shing!")
                break
            
            # Kitoblar ro'yxatini tayyorlash
            books_text = f"📚 <b>Kitoblar ro'yxati</b> (Jami: {total_count})\n\n"
            
            for i, book in enumerate(books, 1):
                books_text += f"{i}. 📖 <b>{book.title}</b>\n"
                books_text += f"   ✍️ {book.author}\n"
                books_text += f"   🆔 ID: {book.id}\n\n"
                
                # Telegram limitlari uchun
                if len(books_text) > 3500:
                    books_text += "... va boshqalar\n\n"
                    books_text += f"💡 Barcha kitoblarni ko'rish uchun /search buyrug'idan foydalaning."
                    break
            
            await message.answer(books_text, parse_mode="HTML")
            break
            
    except Exception as e:
        logger.error(f"Kitoblar ro'yxatini olishda xato: {e}")
        await message.answer("❌ Kitoblar ro'yxatini olishda xatolik yuz berdi.")


@router.message(Command("search"))
async def cmd_search(message: Message) -> None:
    """Kitoblarni qidirish"""
    try:
        # Qidiruv kalitini olish
        command_args = message.text.split(maxsplit=1)
        if len(command_args) < 2:
            await message.answer(
                "❌ Qidiruv kalitini kiriting!\n\n"
                "Format: <code>/search kalit_soz</code>\n"
                "Misol: <code>/search doston</code>",
                parse_mode="HTML"
            )
            return
        
        keyword = command_args[1].strip()
        
        async for session in get_session():
            books = await Book.search(session, keyword, limit=20)
            
            if not books:
                await message.answer(
                    f"🔍 <b>Qidiruv natijasi:</b>\n\n"
                    f"\"<code>{keyword}</code>\" bo'yicha kitoblar topilmadi.\n\n"
                    f"💡 Boshqa kalit so'z bilan urinib ko'ring.",
                    parse_mode="HTML"
                )
                break
            
            # Natijalarni tayyorlash
            result_text = f"🔍 <b>Qidiruv natijasi:</b> \"{keyword}\"\n\n"
            
            for i, book in enumerate(books, 1):
                result_text += f"{i}. 📖 <b>{book.title}</b>\n"
                result_text += f"   ✍️ {book.author}\n"
                result_text += f"   🆔 ID: {book.id}\n\n"
                
                # Telegram limitlari uchun
                if len(result_text) > 3500:
                    result_text += "... va boshqa natijalar\n"
                    break
            
            result_text += f"📊 Jami topildi: {len(books)} ta kitob"
            
            await message.answer(result_text, parse_mode="HTML")
            break
            
    except Exception as e:
        logger.error(f"Qidirishda xato: {e}")
        await message.answer("❌ Qidirishda xatolik yuz berdi.")


@router.message(F.text)
async def handle_unknown_message(message: Message) -> None:
    """Noma'lum xabarlar uchun handler"""
    await message.answer(
        "❓ Noma'lum buyruq.\n\n"
        "Mavjud buyruqlar ro'yxati uchun /help yozing.",
        parse_mode="HTML"
    )