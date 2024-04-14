import asyncio
import logging
import sys
import os
import sqlite3
import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from aiogram.fsm.context import FSMContext
from datetime import datetime
import requests
from config import TOKEN
from handlers.menu_return import st_menu

from handlers.link_generation import sms_link, sms_Start
from handlers.sms_meow import sms_send_meow, sms_success_meow
from handlers.sms_depa import sms_send_depa
from handlers.profile_menu import menu_profile
from handlers.profile_meow import profile_meow
from handlers.profile_depa import profile_depa

from aiogram import F
from utils.state import Admin




logging.basicConfig(level=logging.INFO)



async def menu_start(message: Message, bot: Bot):
    try:
        keys = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Профиль 👤", callback_data=f'profile_menu')],
            [InlineKeyboardButton(text="Парсинг 📤", callback_data=f'pars_')],

        ])
        await bot.send_message(message.chat.id, f"Приветствую {message.from_user.first_name}\n"
                                                f"БОТ Авторассылок", reply_markup=keys)
        await bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(e)







async def start():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.message.register(menu_start, CommandStart())
    dp.message.register(sms_link, Admin.number)
    dp.callback_query.register(sms_Start, F.data.startswith("pars_"))
    dp.callback_query.register(sms_send_meow, F.data.startswith("sms_meow_"))
    dp.callback_query.register(sms_send_depa, F.data.startswith("sms_depa_"))
    dp.callback_query.register(st_menu, F.data.startswith("back_menu_st_"))
    dp.callback_query.register(sms_success_meow, F.data.startswith("sms_success_"))
    dp.callback_query.register(menu_profile, F.data.startswith("profile_menu"))
    dp.callback_query.register(profile_meow, F.data.startswith("profile_meow"))
    dp.callback_query.register(profile_depa, F.data.startswith("profile_depa"))




    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
