import aiogram
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import asyncio
import requests
import datetime
from aiogram.utils.exceptions import MessageCantBeDeleted
import traceback

import json, string


class MyState(StatesGroup):
    waiting_for_question = State()


class DownloadPhotoState(StatesGroup):
    waiting_for_photo = State()


class GreetingState(StatesGroup):
    SettingGreeting = State()


class GreetingStateChat(StatesGroup):
    SettingGreetingChat = State()


class CallToActionState(StatesGroup):
    SettingCallToAction = State()


class CallToActionStateChat(StatesGroup):
    SettingCallToActionChat = State()


class UpdateLinkState(StatesGroup):
    SettingLink = State()


class UpdateLinkStateChat(StatesGroup):
    SettingLinkChat = State()


class SomeState(StatesGroup):
    waiting_for_client_id = State()


class RegistrationState(StatesGroup):
    start_done = State()


class ChangeNumberStates(StatesGroup):
    WAITING_FOR_NEW_NUMBER = State()


class ChangeEmailStates(StatesGroup):
     WAITING_FOR_NEW_EMAIL = State()


class EmailConfirmationState(StatesGroup):
    CONFIRMATION = State()


# ============================================ blockchaine =================================
async def blockchaine_command_handler(message: types.Message):
    response = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&include_market_cap=true')
    cryptocurrencies = response.json()

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title_message = await message.answer(f'Топ 10 криптовалют на `{current_time}`', parse_mode='Markdown')

    # Выводим данные о каждой валюте
    messages_to_delete = []
    for currency in cryptocurrencies:
        name = currency['name']
        price = currency['current_price']
        market_cap = currency['market_cap']
        currency_message = await message.answer(f'`{name}:` `{price} USD`\n`Market Cap: {market_cap} USD`', parse_mode='Markdown')
        messages_to_delete.append(currency_message)

    loop = asyncio.get_running_loop()
    loop.call_later(60 * 5, lambda: asyncio.create_task(delete_messages(title_message, messages_to_delete)))  # удалить сообщения через 10 минут


async def delete_messages(title_message: types.Message, messages_to_delete: list):
    try:
        await title_message.delete()
        for message in messages_to_delete:
            await message.delete()
    except MessageCantBeDeleted:
        traceback.print_exc()


async def echo_send(message: types.Message):
    if {index.lower().translate(str.maketrans('', '', string.punctuation)) for index in
        message.text.split(' ')}.intersection(
        set(json.load(open('TestMir/cenzura.json')))
    ) != set():
        await message.reply('Запрещенный контент')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)








