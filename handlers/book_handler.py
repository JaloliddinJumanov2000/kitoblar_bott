from aiogram import types
from aiogram.filters import Command
from models import Book
from database import get_db
from sqlalchemy import or_


async def add_book_handler(message: types.Message):
    try:
        text = message.text.replace('/add_book', '').strip()

        if not text:
            await message.answer("""
❌ **Noto'g'ri format!**

**To'g'ri format:**
`/add_book "Kitob nomi" "Muallif"`

**Misollar:**
• `/add_book "Dunyoning ishlari" "O'tkir Hoshimov"`
• `/add_book "Mehrobdan chayon" "Abdulla Qodiriy"`
            """, parse_mode="Markdown")
            return

        parts = []
        current = ""
        in_quotes = False

        for char in text:
            if char == '"':
                if in_quotes:
                    if current:
                        parts.append(current)
                        current = ""
                    in_quotes = False
                else:
                    in_quotes = True
            elif char == ' ' and not in_quotes:
                if current:
                    parts.append(current)
                    current = ""
            else:
                current += char

        if current:
            parts.append(current)

        if len(parts) != 2:
            await message.answer("❌ Kitob nomi va muallifi kerak!\n\nMisol: `/add_book \"Kitob nomi\" \"Muallif\"`",
                                 parse_mode="Markdown")
            return

        title, author = parts[0].strip(), parts[1].strip()

        db = get_db()
        try:

            existing = db.query(Book).filter(
                Book.title.ilike(title),
                Book.author.ilike(author)
            ).first()

            if existing:
                await message.answer(f"⚠️ Bu kitob allaqachon mavjud!\n\n📖 **{existing.title}**\n👤 *{existing.author}*")
                return


            new_book = Book(title=title, author=author)
            db.add(new_book)
            db.commit()

            await message.answer(f"""
✅ **Kitob qo'shildi!**

📖 **{new_book.title}**
👤 **{new_book.author}**
🆔 ID: {new_book.id}
            """, parse_mode="Markdown")

        except Exception as e:
            db.rollback()
            await message.answer("❌ Xatolik yuz berdi!")
        finally:
            db.close()

    except Exception as e:
        await message.answer("❌ Komandani tushunmadim!")


async def list_books_handler(message: types.Message):
    """Kitoblar ro'yxati"""
    db = get_db()
    try:
        books = db.query(Book).order_by(Book.title).all()

        if not books:
            await message.answer(
                "📚 Hozircha kitoblar yo'q.\n\nBirinchi kitobni qo'shing:\n`/add_book \"Kitob nomi\" \"Muallif\"`",
                parse_mode="Markdown")
            return

        text = "📚 **Kitoblarim:**\n\n"
        for i, book in enumerate(books, 1):
            text += f"**{i}.** 📖 {book.title}\n👤 *{book.author}*\n\n"

        text += f"📊 **Jami:** {len(books)} ta kitob"

        await message.answer(text, parse_mode="Markdown")

    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi!")
    finally:
        db.close()


async def search_books_handler(message: types.Message):
    """Kitoblarni qidirish"""
    try:
        search_term = message.text.replace('/search', '').strip()

        if not search_term:
            await message.answer("""
🔍 **Qidirish**

**Format:** `/search kalit_so'z`

**Misollar:**
• `/search doston`
• `/search Alisher`
            """, parse_mode="Markdown")
            return

        db = get_db()
        try:
            books = db.query(Book).filter(
                or_(
                    Book.title.ilike(f'%{search_term}%'),
                    Book.author.ilike(f'%{search_term}%')
                )
            ).order_by(Book.title).all()

            if not books:
                await message.answer(
                    f"🔍 **\"{search_term}\" topilmadi**\n\nBoshqa so'z bilan qidiring yoki yangi kitob qo'shing.")
                return

            text = f"🔍 **\"{search_term}\" natijalari:**\n\n"
            for i, book in enumerate(books, 1):
                text += f"**{i}.** 📖 {book.title}\n👤 *{book.author}*\n\n"

            text += f"📊 **Topildi:** {len(books)} ta"

            await message.answer(text, parse_mode="Markdown")

        except Exception as e:
            await message.answer("❌ Qidirishda xatolik!")
        finally:
            db.close()

    except Exception as e:
        await message.answer("❌ Qidirish so'rovini tushunmadim!")
