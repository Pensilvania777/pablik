import os
import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from aiogram.fsm.context import FSMContext
from datetime import datetime
import requests
from config import DEPA_TOKEN


async def sms_send_depa(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        http_method = "POST"
        api_url = "https://depa-sms.pro/"
        api_method = "send/"
        api_key = DEPA_TOKEN

        headers = {
            'accept': 'application/json',
            "Authorization": "Bearer " + api_key
        }
        successful_requests_count = 0
        errors_requests_count = 0
        sending_message = await bot.send_message(call.message.chat.id, f"Ожидайте отправки смс...\n")
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        with open('output.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                shorthref, numberphone = line.strip().split()
                cleaned_number = ''.join(filter(str.isdigit, numberphone))
                number = int(cleaned_number)
                body = {
                        "phone": number,
                        "country": "poland",
                        "service": "olx",
                        "short_url": "true",
                        "url": shorthref
                }

                print("[" + str(datetime.now()) + "] API URL: " + api_url + api_method)
                print("[" + str(datetime.now()) + "] HTTP Method Request: " + http_method)
                print("[" + str(datetime.now()) + "] HTTP Body Request: " + json.dumps(body))

                try:
                    response = requests.request(http_method, api_url + api_method, headers=headers, json=body)
                    response.raise_for_status()
                    print("[" + str(datetime.now()) + "] Status Code: " + str(response.status_code))
                    print("[" + str(datetime.now()) + "] Response: " + response.text)
                    successful_requests_count += 1
                except requests.exceptions.RequestException as e:
                    print("[" + str(datetime.now()) + "] Error: " + str(e))
                    errors_requests_count += 1
        keys = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Меню 🔙", callback_data=f'back_menu_st_')],
        ])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=sending_message.message_id,
                                    text=f"Отправлено: {successful_requests_count} \n"
                                                     f"Ошибок: {errors_requests_count}\n"
                                                     , reply_markup=keys)
        os.remove('output.txt')

    except Exception as e:
        print(e)