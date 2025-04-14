from loader import dp,bot
from aiogram import types,F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardButton
from utils.misc.subscription import check
from middlewares.mymiddleware import CheckSubscriptionCallback
from api import *
import os
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import hashlib
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import secrets
from datetime import datetime, timedelta


text = (
        "👋 Assalomu alaykum!\n\n"
        "🚀 30 kunlik Challenge botiga xush kelibsiz!\n\n"
        "📌 Har kuni siz tanlagan vazifalarni bajarib, ball to‘playsiz.\n"
        "🎯 Maqsad – har kuni doimiy rivojlanish!\n\n"
        "👇 Quyidagi tugmani bosib, bugungi topshiriqlaringizni ko‘ring:"
    )

start_text_en = '''
The bot is at your service!
'''
subs ='''
Iltimos bot to'liq ishlashi uchun quyidagi kanallarga obuna bo'ling!
'''

@dp.message(CommandStart())
async def start_chat(message: types.Message):
    user = get_user(telegram_id=message.from_user.id)
    language = user.get('language', 'uz') if user != 'Not Found' else 'uz'

    btn = InlineKeyboardBuilder()
    channels = get_all_channels()
    final_status = True

    if channels:
        for channel in channels:
            try:
                status = await check(user_id=message.from_user.id, channel=channel['channel_id'])
            except:
                status = False

            final_status &= status

            if not status:
                try:
                    chat = await bot.get_chat(channel['channel_id'])
                    invite_link = await chat.export_invite_link()
                    btn.row(InlineKeyboardButton(text=f"❌ {chat.title}", url=invite_link))
                except Exception as e:
                    print(e)

        if not final_status:
            btn.button(text='Obunani tekshirish', callback_data=CheckSubscriptionCallback(check=True))
            btn.adjust(1)
            await message.answer(text=subs, reply_markup=btn.as_markup(row_width=1))
            return  # 👉 prevent sending Web App link again

    # ✅ Send only ONCE if subscription passed or no channels
    await message.answer(text=text if language == 'uz' else start_text_en)
    await message.answer(
        "Challengelarni boshlash uchun quyidagi tugmani bosing:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Boshlash", web_app=WebAppInfo(url="https://ertalabki-baraka.vercel.app/"))]
            ]
        )
    )



@dp.callback_query(CheckSubscriptionCallback.filter())
async def test(call:types.CallbackQuery):
    await call.answer(cache_time=60)
    user = get_user(telegram_id=call.from_user.id)
    if user != 'Not Found':
        language = user.get('language', 'uz')
    else:
        language = 'uz'
    k = []
    final_status = False
    user_id = call.from_user.id
    kanallar = get_all_channels()
    for kanal in kanallar:
        try:
            channel = await bot.get_chat(kanal['channel_id'])
        except:
            pass
        try:
            res = await bot.get_chat_member(chat_id=kanal['channel_id'], user_id=user_id)
        except:
            continue
        if res.status == 'member' or res.status == 'administrator' or res.status == 'creator':
            k.append(InlineKeyboardButton(text=f"✅ {channel.title}", url=f"{await channel.export_invite_link()}"))

        else:
            k.append(InlineKeyboardButton(text=f"❌ {channel.title}", url=f"{await channel.export_invite_link()}"))
            final_status = True
    builder = InlineKeyboardBuilder()
    builder.add(*k)
    builder.button(text='Obunani tekshirish', callback_data=CheckSubscriptionCallback(check=True))
    builder.adjust(1)
    if final_status:
        await bot.send_message(chat_id=user_id,
                               text=subs,
                               reply_markup=builder.as_markup())
    else:
        await call.message.answer(start_text_en if language=='en' else start_text_uz)
    await call.message.delete()



