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



import requests
import json
from datetime import datetime



async def profile_meow(call: CallbackQuery, bot: Bot):
    try:
        http_method = "GET"
        api_url = "https://api.meowsms.app/"
        api_method = "getMe/"
        api_key = "Cn7MffUd3oYxXdSdZgeriWrKAr"
        body = []
        balance = 0
        send_today = 0
        send_all = 0
        headers = {"Authorization": "Bearer " + api_key}

        print("[" + str(datetime.now()) + "] API URL: " + api_url + api_method)
        print("[" + str(datetime.now()) + "] HTTP Method Request: " + http_method)
        print("[" + str(datetime.now()) + "] HTTP Body Request: " + json.dumps(body))

        try:
            response = requests.request(http_method, api_url + api_method, headers=headers, json=body)
            response.raise_for_status()
            print("[" + str(datetime.now()) + "] Status Code: " + str(response.status_code))
            print("[" + str(datetime.now()) + "] Response: " + response.text)
            response_json = response.json()
            balance = response_json.get('balance')
            send_today = response_json.get('sent_today')
            send_all = response_json.get('sent')
        except requests.exceptions.RequestException as e:
            print("[" + str(datetime.now()) + "] Error: " + str(e))

        keys = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'profile_menu')],
            [InlineKeyboardButton(text="Меню 🔙", callback_data=f'back_menu_st_')]
        ])

        await bot.send_message(call.message.chat.id, f"Профиль MEOW 🐈\n"
                                                     f"Баланс: {balance}\n"
                                                     f"Отправлено сегодня: {send_today}\n"
                                                     f"Отправлено за все время: {send_all}\n"
                                                     , reply_markup=keys)
        await bot.delete_message(call.message.chat.id, call.message.message_id)


    except Exception as e:
        print(e)