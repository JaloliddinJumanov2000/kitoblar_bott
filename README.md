# 📚 Kitoblar Bot

Telegram orqali kitoblar kolleksiyasini boshqarish uchun mo'ljallangan bot.

## ✨ Xususiyatlar

- 📖 Kitoblar qo'shish, ro'yxatlash va qidirish
- 🔍 Tez qidiruv imkoniyati
- 📊 Kitoblar statistikasi
- 🗄️ SQLAlchemy ORM yordamida saqlash
- 🔄 Alembic migratsiyalari
- ⚡ Async/await texnologiyasi

## 🚀 O'rnatish

### 1. Loyihani yuklab olish
```bash
git clone <repository-url>
cd kitoblar-bot
```

### 2. Virtual muhit yaratish
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Paketlarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilarini sozlash
```bash
cp .env.example .env
```

`.env` faylini tahrirlang va quyidagi qiymatlarni kiriting:
- `BOT_TOKEN` - Telegram bot tokeningiz
- `DATABASE_URL` - Ma'lumotlar bazasi URL (ixtiyoriy)

### 5. Ma'lumotlar bazasini migratsiya qilish
```bash
alembic upgrade head
```

### 6. Botni ishga tushirish
```bash
python main.py
```

## 💻 Ishlatish

### Bot Komandalar

- `/start` - Botni ishga tushirish
- `/help` - Yordam ma'lumotlari
- `/add_book "kitob nomi" "muallif"` - Yangi kitob qo'shish
- `/books` - Barcha kitoblar ro'yxati
- `/search kalit_soz` - Kitoblarni qidirish

### Misollar

```
/add_book "Dunyoning ishlari" "O'tkir Hoshimov"
/add_book "Saodat Asri" "Abdulla Qodiriy"
/search doston
/search Alisher
```

## 🏗️ Loyiha Strukturasi

```
├── main.py              # Asosiy bot fayli
├── config.py            # Konfiguratsiya sozlamalari
├── database.py          # Ma'lumotlar bazasi sozlamalari
├── models.py            # SQLAlchemy modellari
├── handlers.py          # Bot handlerlari
├── requirements.txt     # Python paketlari
├── alembic.ini          # Alembic konfiguratsiyasi
├── alembic/             # Migratsiya fayllari
│   ├── env.py
│   └── versions/
├── .env.example         # Muhit o'zgaruvchilari namunasi
└── README.md           # Loyiha hujjatlari
```

## 🔧 Rivojlantirish

### Yangi migratsiya yaratish
```bash
alembic revision --autogenerate -m "Tavsif"
```

### Migratsiyalarni qo'llash
```bash
alembic upgrade head
```

### Testlar ishga tushirish
```bash
python -m pytest
```

## 📝 Log Fayllari

Bot ishlaganda `bot.log` faylida barcha loglar saqlanadi.

## 🔒 Xavfsizlik

- Bot tokeningizni hech qachon ommaga oshkor qilmang
- Production muhitida `SQLite` o'rniga `PostgreSQL` ishlatishni tavsiya qilamiz
- `.env` faylini `.gitignore`ga qo'shing

## 🤝 Hissa Qo'shish

1. Loyihani fork qiling
2. Feature branch yarating (`git checkout -b feature/yangi-xususiyat`)
3. O'zgarishlarni commit qiling (`git commit -am 'Yangi xususiyat qo'shildi'`)
4. Branch ni push qiling (`git push origin feature/yangi-xususiyat`)
5. Pull Request yarating

## 📄 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi.

## 📞 Yordam

Savollar yoki muammolar bo'lsa, issue yarating yoki elektron pochta orqali murojaat qiling.