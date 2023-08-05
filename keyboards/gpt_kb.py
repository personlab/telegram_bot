from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram import types


markup_Chat_gpt = types.InlineKeyboardMarkup(row_width=2)
item1 = types.InlineKeyboardButton("Включить", callback_data='chatgpt_on')
item2 = types.InlineKeyboardButton("Выключить", callback_data='chatgpt_off')
markup_Chat_gpt.add(item1, item2)


ChatGPT_reset = types.InlineKeyboardButton(text='Режим')
ChatGPT_status = types.InlineKeyboardButton(text='Статус')
button_back = types.KeyboardButton('🔙 Вернуться назад')
button_pay = types.KeyboardButton('Магазин')

button_done_gpt_turbo = ReplyKeyboardMarkup(resize_keyboard=True).add(ChatGPT_reset, ChatGPT_status).add(button_back, button_pay)


def gpt_button_setting() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_change_number = types.KeyboardButton('Режим')
    button_status = types.KeyboardButton('Статус')
    button_back_profile = types.KeyboardButton('🔙 Back')

    keyboard.add(button_back_profile, button_status, button_change_number)
    return keyboard

