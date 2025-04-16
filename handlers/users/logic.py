from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # ✅ Python 3.9+
# For Python <3.9 use: from pytz import timezone

scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Tashkent"))  # ✅ Set scheduler timezone
WEB_APP_URL = "https://ertalabki-baraka.vercel.app/"

async def send_challenge(bot: Bot, telegram_id: int, title: str, description: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Start", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

    await bot.send_message(
        chat_id=telegram_id,
        text=f"🏁 Topshirig'ingiz:\n<b>{title}</b>\n\n{description}\n\nSiz bu vazifani boshlashingiz kerak!",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def fetch_and_schedule_tasks(bot: Bot):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://baraka30.pythonanywhere.com/api/scheduled-tasks/") as resp:
            tasks = await resp.json()

    tz = ZoneInfo("Asia/Tashkent")  # ✅ Tashkent timezone

    now_tashkent = datetime.now(tz)

    for task in tasks:
        title = task["title"]
        description = task["description"]
        time_start_str = task["time_start"]  # Example: "05:30"
        users = task["users"]

        hour, minute, *_ = map(int, time_start_str.split(":"))

        # ✅ Create run_time in Tashkent timezone
        run_time = now_tashkent.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if run_time < now_tashkent:
            run_time += timedelta(days=1)

        for user in users:
            telegram_id = int(user["telegram_id"])
            job_id = f"{telegram_id}_{title}_{int(run_time.timestamp())}"

            scheduler.add_job(
                send_challenge,
                "date",
                run_date=run_time,
                args=[bot, telegram_id, title, description],
                id=job_id,
                replace_existing=True
            )
