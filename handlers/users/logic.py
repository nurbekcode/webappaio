# scheduler_tasks.py

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()
WEB_APP_URL = "https://ertalabki-baraka.vercel.app/"

async def send_challenge(bot: Bot, telegram_id: int, title: str, description: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Start ✅", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

    await bot.send_message(
        chat_id=telegram_id,
        text=f"🏁 <b>Bugungi topshiriq:</b>\n\n<b>{title}</b>\n\n{description}\n\n⏳ Vaqtingizni bekor ketkazmang, hoziroq boshlang!",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def fetch_and_schedule_tasks(bot: Bot):
    scheduler.remove_all_jobs()  # eski tasklarni tozalaydi

    async with aiohttp.ClientSession() as session:
        async with session.get("https://baraka30.pythonanywhere.com/api/scheduled-tasks/") as resp:
            tasks = await resp.json()

    for task in tasks:
        title = task["title"]
        description = task["description"]
        time_start_str = task["time_start"]
        users = task["users"]

        hour, minute, *_ = map(int, time_start_str.split(":"))

        # UTC bilan ishlash aniqroq bo'ladi
        run_time = datetime.utcnow().replace(hour=hour, minute=minute, second=0, microsecond=0)
        if run_time < datetime.utcnow():
            run_time += timedelta(days=1)

        for user in users:
            telegram_id = int(user["telegram_id"])
            scheduler.add_job(
                send_challenge,
                "date",
                run_date=run_time,
                args=[bot, telegram_id, title, description],
                id=f"{telegram_id}_{title}_{run_time.timestamp()}",
                replace_existing=True
            )