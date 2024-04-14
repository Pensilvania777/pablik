
from aiogram import Bot, Dispatcher, Router, types

from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from config import DEPA_TOKEN
import requests
import json
from datetime import datetime


async def profile_depa(call: CallbackQuery, bot: Bot):
    try:
        http_method = "GET"
        api_url = "https://depa-sms.pro/"
        api_method = "me/"
        api_key = DEPA_TOKEN
        body = []
        balance = 0

        headers = {
            'accept': 'application/json',
            "Authorization": "Bearer " + api_key
        }

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
        except requests.exceptions.RequestException as e:
            print("[" + str(datetime.now()) + "] Error: " + str(e))

        keys = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'profile_menu')],
            [InlineKeyboardButton(text="Меню 🔙", callback_data=f'back_menu_st_')]
        ])

        await bot.send_message(call.message.chat.id, f"Профиль DEPA 📱\n"
                                                     f"Баланс: {balance}\n"
                                                     , reply_markup=keys)
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(e)