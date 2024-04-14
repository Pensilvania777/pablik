
from aiogram import Bot, Dispatcher, Router, types

from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from aiogram.fsm.context import FSMContext
import requests
from utils.state import Admin

url = "http://147.45.40.97:6000/createhrefparse"

def read_data_from_file(file_content):
    lines = file_content.getvalue().decode().split('\n')
    data = []
    for line in lines:
        if line.strip():  # Пропускаем пустые строки
            numberphone, hrefparse = line.strip().split(' ')
            print(numberphone, hrefparse)
            data.append({
                "token": "6DCSg1tZexbj33huD3Zj2gmm1h4DzHepD4SgT2pYeMyo85i7UA",
                "chatID": "5698549540",
                "country": "PL",
                "platfroms": "OLX",
                "hrefparse": hrefparse,
                "numberphone": numberphone,
                "fiouser": "Krzysztof Kołtun",
                "addrdelivery": "Leszczu 17 30-376 Krakow"
            })
    return data

async def sms_Start(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        user_id = call.message.chat.id
        keys = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_')],
        ])
        await call.message.answer("Отправьте файл с ссылками и номерами для парсинга", reply_markup=keys)
        await state.set_state(Admin.number)

        await bot.delete_message(user_id, call.message.message_id)
    except Exception as e:
        print(e)


async def sms_link(message: Message, bot: Bot, state: FSMContext):
    try:
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_content = await bot.download_file(file.file_path)

        # Преобразование байтового содержимого файла в строку и удаление символа "|"
        file_content_decoded = file_content.read().decode('utf-8').replace('|', '')

        # Разделение содержимого файла на строки
        params_list = file_content_decoded.split('\n')

        print(params_list)
        count_ok = 0
        count_number_phone_already_use = 0
        count_error_parsing = 0
        await bot.delete_message(message.chat.id, message.message_id - 1)
        sending_message = await bot.send_message(message.chat.id,
                                                 f"Это может занять некоторое время, пожалуйста, подождите...")

        await bot.delete_message(message.chat.id, message.message_id)
        for params_str in params_list:
            # Проверка, содержит ли строка как минимум два значения
            if len(params_str.split()) >= 2:
                # Разделение строки на номер телефона и ссылку
                numberphone, link = params_str.split(' ', 1)

                params = {
                    "token": "6DCSg1tZexbj33huD3Zj2gmm1h4DzHepD4SgT2pYeMyo85i7UA",
                    "chatID": "5698549540",
                    "country": "PL",
                    "platfroms": "OLX",
                    "hrefparse": link.strip(),
                    "numberphone": numberphone.strip(),
                    "fiouser": "Krzysztof Kołtun",
                    "addrdelivery": "Leszczu 17 30-376 Krakow"
                }
                response = requests.post(url, json=params)
                if response.status_code == 200:
                    json_response = response.json()
                    print("Ответ:", json_response)
                    if json_response.get('action') == 'OK':
                        with open('output.txt', 'a') as output_file:
                            numberphone = params['numberphone'][1:]
                            shorthref = json_response.get('shorthref')
                            fulldaomins = json_response.get('fulldaomins')
                            output_file.write(f"{shorthref} {numberphone}\n")
                            count_ok += 1
                    elif json_response.get('action') == 'NUMBER_PHONE_ALREADY_USE':
                        count_number_phone_already_use += 1
                    elif json_response.get('action') == 'ERROR_PARSING':
                        count_error_parsing += 1
                else:
                    print("Ошибка при отправке:", response.status_code)
            else:
                # Если строка не содержит два значения, увеличиваем счетчик ошибок
                count_error_parsing += 1

        print(f"Отправлено: {count_ok}")
        print(f"Номера уже использованы: {count_number_phone_already_use}")
        print(f"Неверная ссылка : {count_error_parsing}")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отправить смс Meow 🐈", callback_data=f'sms_meow_')],
            [InlineKeyboardButton(text="Отправить смс DEPA 📱", callback_data=f'sms_depa_')],

            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_')],
        ])
        keys = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_')],
        ])

        if count_ok > 0:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=sending_message.message_id,
                                        text=f"Короткие ссылки: {count_ok}\n"
                                             f"Номера уже использованы: {count_number_phone_already_use}\n"
                                             f"Неверная ссылка : {count_error_parsing}", reply_markup=keyboard)
        else:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=sending_message.message_id,
                                        text=f"Коротких ссылок нет \n"
                                             f"Номера уже использованы: {count_number_phone_already_use}\n"
                                             f"Неверная ссылка : {count_error_parsing}", reply_markup=keys)

    except Exception as e:
        print(e)