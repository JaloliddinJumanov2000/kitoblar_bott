from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import async_session
from services.user_service import UserService

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: Message):
    async with async_session() as session:
        user = await UserService.get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )

        welcome_text = f"""
👋 Assalomu alaykum, {message.from_user.first_name}!

🤖 Shaxsiy kitoblar kolleksiyangizni boshqarish Botiga xush kelibsiz!

Bu bot orqali siz:
• 📚 Kitoblarni ko'rish
• ✅ Kitoblarni qo'shish
• 🔍 Qidiruv

Quyidagi tugmalar orqali tezkor buyruq yuborishingiz mumkin 👇
        """

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 Kitoblarim", callback_data="kitoblarim")],
            [InlineKeyboardButton(text="✅ Kitob qo'shish", callback_data="add_book")],
            [InlineKeyboardButton(text="🔍 Kitob qidirish", callback_data="search")],
            [InlineKeyboardButton(text="🆘 Yordam", callback_data="help")],
        ])

        await message.answer(welcome_text, reply_markup=keyboard)


@start_router.message(Command("help"))
async def help_handler(message: Message):
    help_text = """
🆘 Yordam

Mavjud buyruqlar:
• /start - Botni ishga tushirish
• /add_book  - Kitob qo'shish
• /search   - Kitob qidirish
• /help - Yordam

Yangi kitob qo'shish:
Format: /add_book "sarlavha" "muallif"
Misol: /add_book "Dunyoning ishlari" "O'tkir Hoshimov"

 Kitoblarni qidirish:
 Format: /search kalit_soz
 Misol: /search Alisher
 
    """

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="start")]
    ])

    await message.answer(help_text, reply_markup=keyboard)

@start_router.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    if callback.data == "kitoblarim":
        await callback.message.answer("📚 Kitoblarim ")
    elif callback.data == "add_book":
        await callback.message.answer("Kitobni qo'shish uchun: /add " )
    elif callback.data == "search":
        await callback.message.answer("Kitoblarni qidirish uchun: /search ")
    elif callback.data == "help":
        await help_handler(callback.message)
    elif callback.data == "start":
        await start_handler(callback.message)

    await callback.answer()
