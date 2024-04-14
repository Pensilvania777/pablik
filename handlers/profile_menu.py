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

from aiogram import F
from utils.state import Admin

async def menu_profile(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        keys = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Профиль MEOW 🐈", callback_data=f'profile_meow')],
            [InlineKeyboardButton(text="Профиль DEPA 📱", callback_data=f'profile_depa')],

            [InlineKeyboardButton(text="Меню 🔙", callback_data=f'back_menu_st_')],
        ])
        await bot.send_message(call.message.chat.id, f"Выберите профиль:", reply_markup=keys)
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(e)