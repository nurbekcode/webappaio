from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()
WEB_APP_URL = "https://ertalabki-baraka.vercel.app/"

# 🔁 Har bir foydalanuvchiga yuboriladigan vazifa
async def send_challenge(bot: Bot, telegram_id: int, title: str, description: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Boshlash", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

    await bot.send_message(
        chat_id=telegram_id,
        text=f"🏁 <b>Bugungi vazifa:</b>\n\n📌 <b>{title}</b>\n\n📝 {description}\n\n⏱ Boshlash uchun tugmani bosing!",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

# 🕒 Yuborish vaqtini aniq hisoblash (agar o‘tib ketgan bo‘lsa, ertangi kunga ko‘chiradi)
def get_next_run_time(hour: int, minute: int) -> datetime:
    now = datetime.now()
    run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if run_time <= now:
        run_time += timedelta(days=1)
    return run_time

# 🔄 API'dan topshiriqlarni olib jadval qilish
async def fetch_and_schedule_tasks(bot: Bot):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://baraka30.pythonanywhere.com/api/scheduled-tasks/") as resp:
                tasks = await resp.json()

        for task in tasks:
            title = task["title"]
            description = task["description"]
            time_start_str = task["time_start"]
            users = task["users"]

            hour, minute = map(int, time_start_str.split(":")[:2])
            run_time = get_next_run_time(hour, minute)

            for user in users:
                telegram_id = int(user["telegram_id"])
                job_id = f"{telegram_id}_{title}_{run_time.strftime('%Y%m%d%H%M')}"
                scheduler.add_job(
                    send_challenge,
                    "date",
                    run_date=run_time,
                    args=[bot, telegram_id, title, description],
                    id=job_id,
                    replace_existing=True  # yangilash imkoniyati
                )
    except Exception as e:
        print(f"❌ Scheduler error: {e}")
