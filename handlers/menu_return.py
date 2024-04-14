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

from aiogram import F
from aiogram.fsm.state import StatesGroup, State

async def st_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        keys = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Профиль 👤", callback_data=f'profile_menu')],
            [InlineKeyboardButton(text="Парсинг 📤", callback_data=f'pars_')],

        ])
        await bot.send_message(call.message.chat.id, f"Приветствую {call.message.from_user.first_name}\n"
                                                f"БОТ Авторассылок", reply_markup=keys)
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(e)