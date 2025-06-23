"""
# Kitoblar jadvali yaratish

Ushbu migratsiya dastlabki ma'lumotlar bazasi strukturasini yaratadi.

## Yangi jadvallar:
1. **books** - Kitoblar jadvali
   - `id` (integer, primary key, autoincrement)
   - `title` (string 255, null emas) - Kitob sarlavhasi
   - `author` (string 255, null emas) - Kitob muallifi  
   - `created_at` (datetime, default utcnow) - Yaratilgan vaqt

## Xususiyatlar:
- Barcha ustunlar to'g'ri indekslangan
- Vaqt qiymatlari UTC formatida saqlanadi
- Primary key avtomatik oshib boradi
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ma'lumotlar bazasi strukturasini yaratish"""
    # Books jadvali yaratish
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Indekslar qo'shish
    op.create_index('ix_books_created_at', 'books', ['created_at'])
    op.create_index('ix_books_title', 'books', ['title'])


def downgrade() -> None:
    """Ma'lumotlar bazasi strukturasini o'chirish"""
    op.drop_index('ix_books_title', table_name='books')
    op.drop_index('ix_books_created_at', table_name='books')
    op.drop_table('books')