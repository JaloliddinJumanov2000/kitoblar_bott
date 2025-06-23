import os
from dotenv import load_dotenv

load_dotenv()

from os import getenv
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
PG_USER=getenv('POSTGRES_USER')
PG_DB=getenv('POSTGRES_DB')
PG_PASS=getenv('POSTGRES_PASS')
PG_HOST=getenv('POSTGRES_HOST')
PG_PORT=getenv('POSTGRES_PORT')
ADMINS=getenv('ADMINS').split(',')

if __name__=='__main__':
    print(PG_USER)
    print(PG_DB)
    print(PG_PASS)
    print(PG_HOST)
    print(PG_PORT)

WELCOME_TEXT = """
🎉 **Kitoblar Bot**ga xush kelibsiz!

Bu bot kitoblaringizni boshqarish uchun.

**Komandalar:**
• `/add_book "Kitob nomi" "Muallif"` - Kitob qo'shish
• `/books` - Barcha kitoblar
• `/search kalit_so'z` - Qidirish
• `/help` - Yordam

Boshlaylik! 📚
"""

HELP_TEXT = """
📋 **Yordam**

**Asosiy komandalar:**
• `/start` - Botni boshlash
• `/help` - Bu yordam
• `/books` - Kitoblar ro'yxati
• `/add_book` - Kitob qo'shish
• `/search` - Qidirish

**Kitob qo'shish:**
`/add_book "Kitob nomi" "Muallif"`

**Misollar:**
• `/add_book "Dunyoning ishlari" "O'tkir Hoshimov"`
• `/add_book "Mehrobdan chayon" "Abdulla Qodiriy"`

**Qidirish:**
`/search doston`
`/search Alisher`

💡 **Eslatma:** Agar nom yoki muallifda probel bo'lsa, qo'shtirnoq ishlating!
"""

