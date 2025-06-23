"""
Telegram Kitoblar Bot - Asosiy fayl
"""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from database import init_db, close_db
from handlers import router


async def main() -> None:
    """Botni ishga tushirish"""
    
    # Konfiguratsiyani tekshirish
    try:
        config.validate()
    except ValueError as e:
        logging.error(f"Konfiguratsiya xatosi: {e}")
        sys.exit(1)
    
    # Logging sozlash
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('bot.log', encoding='utf-8')
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Bot ishga tushirilmoqda...")
    
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    dp.include_router(router)
    
    try:
        # Ma'lumotlar bazasini ishga tushirish
        await init_db()
        logger.info("Ma'lumotlar bazasi tayyor")
        
        # Botni ishga tushirish
        logger.info("Bot ishlamoqda...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Bot ishga tushirishda xato: {e}")
    finally:
        # Tozalash
        await close_db()
        await bot.session.close()
        logger.info("Bot to'xtatildi")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot foydalanuvchi tomonidan to'xtatildi")
    except Exception as e:
        logging.error(f"Kutilmagan xato: {e}")
        sys.exit(1)