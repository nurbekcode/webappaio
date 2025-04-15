import handlers, middlewares
from loader import dp, bot
import asyncio
from utils.notify_admins import start, shutdown
from middlewares.mymiddleware import UserCheckMiddleware
from utils.set_botcommands import private_chat_commands
import logging, sys

# Import scheduler
from handlers.users.logic import scheduler, fetch_and_schedule_tasks

async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await private_chat_commands()

        # Register middlewares and startup/shutdown
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        dp.message.middleware(UserCheckMiddleware())

        # 🔁 Run fetch every 5 minutes
        scheduler.add_job(fetch_and_schedule_tasks, "interval", minutes=5, args=[bot])

        # Start the scheduler
        scheduler.start()

        # Start polling
        await dp.start_polling(bot)
    finally:zz
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
