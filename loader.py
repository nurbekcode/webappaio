from aiogram import Bot,Dispatcher
from data.config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
bot=Bot(token=BOT_TOKEN)
dp=Dispatcher(storage=MemoryStorage())
