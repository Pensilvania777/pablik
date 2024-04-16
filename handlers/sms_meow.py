import os
import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from aiogram.fsm.context import FSMContext
from datetime import datetime
import requests


async def sms_send_meow(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        http_method = "POST"
        api_url = "https://api.meowsms.app/"
        api_method = "sendSMS/"
        api_key = "Cn7MffUd3oYxXdSdZgeriWrKAr"

        headers = {"Authorization": "Bearer " + api_key}
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
                print("Ссылки на вход:", shorthref)
                body = {
                    "number": number,
                    "service": "olxpl",
                    "template": 2,
                    "link": shorthref,
                    "webhook_url": shorthref,
                    "worker_id": 5698549540
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
                    response_json = response.json()

                    last_balance = response_json.get('balance')
                    message_id = response_json.get('message_id')
                    if message_id:
                        with open("message_ids.txt", "a") as file:
                            file.write(str(message_id) + "\n")
                except requests.exceptions.RequestException as e:
                    print("[" + str(datetime.now()) + "] Error: " + str(e))
                    errors_requests_count += 1
        if errors_requests_count >= 1:
            keys = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Повторить отправку 🔁", callback_data=f'sms_send_meow_')],

                [InlineKeyboardButton(text="Меню 🔙", callback_data=f'back_menu_st_')],
            ])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=sending_message.message_id,
                                        text=f"Отправлено: {successful_requests_count} \n"
                                             f"Ошибок: {errors_requests_count}\n"
                                             f"Баланс: {last_balance}", reply_markup=keys)
        elif errors_requests_count == 0:
            keys = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Проверить отправку 📱", callback_data=f'sms_success_')],

                [InlineKeyboardButton(text="Меню 🔙", callback_data=f'back_menu_st_')],
            ])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=sending_message.message_id,
                                        text=f"Отправлено: {successful_requests_count} \n"
                                                         f"Ошибок: {errors_requests_count}\n"
                                                         f"Баланс: {last_balance}", reply_markup=keys)
            os.remove('output.txt')

    except Exception as e:
        print(e)


async def sms_success_meow(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        with open("message_ids.txt", "r") as file:
            message_ids = file.readlines()

        # Удаляем пустые строки и символы новой строки
        message_ids = [message_id.strip() for message_id in message_ids if message_id.strip()]

        http_method = "GET"
        api_url = "https://api.meowsms.app/"
        api_method = "getSMSStatus/"
        api_key = "Cn7MffUd3oYxXdSdZgeriWrKAr"
        headers = {"Authorization": "Bearer " + api_key}
        success_sms = 0
        error_sms = 0
        e = ""
        for message_id in message_ids:
            body = {"message_id": message_id}
            print("[" + str(datetime.now()) + "] API URL: " + api_url + api_method)
            print("[" + str(datetime.now()) + "] HTTP Method Request: " + http_method)
            print("[" + str(datetime.now()) + "] HTTP Body Request: " + json.dumps(body))
            try:
                response = requests.request(http_method, api_url + api_method, headers=headers, json=body)
                response.raise_for_status()
                print("[" + str(datetime.now()) + "] Status Code: " + str(response.status_code))
                print("[" + str(datetime.now()) + "] Response: " + response.text)
                success_sms += 1

            except requests.exceptions.RequestException as e:
                print("[" + str(datetime.now()) + "] Error: " + str(e))
                error_sms += 1
        keys = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Меню 🔙", callback_data=f'back_menu_st_')],
        ])

        await bot.send_message(call.message.chat.id, f"Доставлено смс: {success_sms}\n"
                                                     f"Ошибка при доставке смс: {error_sms}\n"
                                                     f"Последняя ошибка: {str(e)}", reply_markup=keys)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        os.remove("message_ids.txt")


    except Exception as e:
        print(e)
