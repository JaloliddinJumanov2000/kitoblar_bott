"""
Bot konfiguratsiya sozlamalari
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot konfiguratsiya sinfi"""
    
    # Bot sozlamalari
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Ma'lumotlar bazasi
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./books.db")
    
    # Log daraja
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> None:
        """Konfiguratsiya sozlamalarini tekshirish"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN muhit o'zgaruvchisi o'rnatilmagan!")


# Global konfiguratsiya obyekti
config = Config()