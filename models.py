"""
Ma'lumotlar bazasi modellari
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Book(Base):
    """Kitob modeli"""
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"
    
    @classmethod
    async def create(cls, session: AsyncSession, title: str, author: str) -> "Book":
        """Yangi kitob yaratish"""
        book = cls(title=title, author=author)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
    
    @classmethod
    async def get_all(cls, session: AsyncSession, limit: int = 50) -> List["Book"]:
        """Barcha kitoblarni olish"""
        query = select(cls).order_by(cls.created_at.desc()).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())
    
    @classmethod
    async def search(cls, session: AsyncSession, keyword: str, limit: int = 20) -> List["Book"]:
        """Kitoblarni qidirish"""
        query = select(cls).filter(
            cls.title.ilike(f"%{keyword}%")
        ).order_by(cls.created_at.desc()).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())
    
    @classmethod
    async def count(cls, session: AsyncSession) -> int:
        """Jami kitoblar sonini olish"""
        query = select(func.count(cls.id))
        result = await session.execute(query)
        return result.scalar() or 0
    
    def to_dict(self) -> dict:
        """Kitobni lug'at shaklida qaytarish"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "created_at": self.created_at.isoformat()
        }