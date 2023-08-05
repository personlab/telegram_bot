import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db
from data_base.db_gpt_chat import Database
from data_base.sqlite_db import sql_get_user_purchases, download_purchases, download_register_users, download_mir_shop, \
    load_user_pay, load_user_shop, get_discount, send_new_product_to_subscribers
from handlers.client import db
from handlers.email_success_pay import send_email_yandex_success_pay, get_user_email
from handlers.other import SomeState, DownloadPhotoState, MyState
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from create_bot import dp, bot, YOOKassa, YOUR_CHAT_ID
from aiogram import Dispatcher, types
from datetime import datetime

from keyboards.admin_kb import keyboard_base_db, button_case_admin
from keyboards.client_kb import button_category, button_text_more_link
import os
import config


moderator_id = YOUR_CHAT_ID  # Заменить на ID текущего модератора


ID = 0


class FSMAdmin(StatesGroup):
    photo = State()
    category = State()
    name = State()
    description = State()
    price = State()
    total = State()


# Получаем ID текущего модератора
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, '*Доступ к административной панели открыт*. 📲💻🛠'
                                                 '', reply_markup=admin_kb.button_case_admin, parse_mode='Markdown')
    await message.delete()


# # **************************** ЗАГРУЗКА ТОВАРА ****************************

async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.answer('Загрузи фото')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as date:
            date['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введите название категории:', reply_markup=button_category())


async def load_category(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as date:
            date['category'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите название товара:', reply_markup=button_case_admin)


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as date:
            date['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите описание:')


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as date:
            date['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажите цену в RUB')


async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as date:
            date['price'] = float(message.text)
        await FSMAdmin.next()
        await message.reply('Укажите количество:')


async def load_total(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as date:
            date['total'] = int(message.text)

        await message.reply('Товар добавлен')
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await send_new_product_to_subscribers()
        load_user_shop()


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    user_id = message.from_user.id
    category = message.successful_payment.invoice_payload.split('_')[1]
    item_name = message.successful_payment.invoice_payload.split('_')[2]
    description = message.successful_payment.invoice_payload.split('_')[3]
    total = message.successful_payment.invoice_payload.split('_')[4]
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subscription_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    price = message.successful_payment.total_amount / 100
    cursor_user_purchases = sqlite_db.cursor_user_purchases
    cursor_user_purchases.execute('INSERT INTO purchases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                  (user_id, category, item_name, description, first_name, last_name, username, purchase_date,
                                   subscription_date, price, total))

    sqlite_db.base_user_purchases.commit()
    if item_name == "ChatGPT":
        db.update_subscription_date(user_id, subscription_date)
        database = Database(config.db_path)
        database.load_data_to_google_gpt()
    load_user_pay()

    # Обновление данных о товаре
    product_data = sqlite_db.get_product_data(item_name)
    if product_data:
        current_total = product_data[5]  # Индекс 5 соответствует столбцу `total`
        new_total = current_total - float(total)
    else:
        print('errore')

    sqlite_db.update_product_data(item_name, new_total)
    load_user_shop()
    # Отправляем уведомление модератору о новой покупке
    await bot.send_message(moderator_id, f'💳 *Новая покупка!*\n👤 ID клиента: {user_id}\n🧑🏻‍🦰🧔🏻‍♂️ Имя клиента: {first_name} {last_name}\n'
                                         f'📦 Категория товара: {category}\n'
                                         f'📦 Товар: {item_name}\n🌐 Пользователь: @{username}\n'
                                         f'🕑 Дата: {purchase_date}\nЦена: {price}')

    await bot.send_message(message.from_user.id, f'Товар {item_name} куплен, спасибо!')


@dp.callback_query_handler(lambda call: call.data.startswith('buy'))
async def process_buy(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    item_name, item_total = call.data.split()[1:4]
    item_total = float(item_total)
    item_data = sqlite_db.get_product_data(item_name)

    category = item_data[1] if item_data else ''
    title = f"{category} - {item_data[2]}" if item_data else ''
    description = item_data[3] if item_data else ''

    discount = get_discount(call.from_user.id)

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=title,
        description=description,
        payload=f'buy_{item_data[1]}_{item_name}_{item_data[3]}_{item_total}',
        provider_token=YOOKassa,
        currency='RUB',
        start_parameter='test_bot',
        prices=[{"label": "Руб", "amount": int((item_data[4] - (item_data[4] * discount)) * 100)}] if item_data else []
    )
    item_data_fore = round((item_data[4] - (item_data[4] * discount)) * 100/100, 2)
    purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Получить адрес электронной почты пользователя из базы данных
    user_id = call.from_user.id
    email_address = get_user_email(user_id)

    # Отправить письмо о покупке на адрес электронной почты пользователя
    await send_email_yandex_success_pay(email_address, item_name, item_data_fore, item_total, purchase_date, discount)


async def file_db_base_download(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, 'Здесь вы можете скачать базу данных оплаченных товаров, '
                                                 'зарегистрированных пользователей и базу данных '
                                                 'товаров с остатками.', reply_markup=keyboard_base_db)


async def back_moderator(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, 'Административная панель', reply_markup=admin_kb.button_case_admin)


# Обновление ID модератора
# @dp.message_handler(commands=['set_moderator'])
async def set_moderator_id(message: types.Message):
    global moderator_id
    moderator_id = message.from_user.id
    await message.reply(f"ID модератора обновлен: {moderator_id}")


# # кнопка удалить
# # @dp.callback_query_handlers(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


# # кнопка удалить
# # @dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[3]} RUB\nКоличество: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')
            ))


# ================================ Вызов клавиатуры для редактирования поста в чат ================================
async def chat_moderator_text(message: types.Message):
    await message.delete()
    user_id = message.from_user.id  # Получаем идентификатор пользователя
    if user_id == moderator_id:  # Сравниваем идентификатор пользователя с идентификатором модератора
        await bot.send_message(
            message.from_user.id, '*Административная панель для редактирования '
                                  'сообщения в чат*.', parse_mode='Markdown', reply_markup=button_text_more_link())
    else:
        await bot.send_message(message.from_user.id, 'У вас нет прав для вызова этой команды')


# ================================ поиск покупки клиента по id ================================
async def pay_command(message: types.Message):
    await message.reply("Пожалуйста, введите ID клиента:")
    await SomeState.waiting_for_client_id.set()


# @dp.message_handler(state=SomeState.waiting_for_client_id)
async def process_client_id(message: types.Message, state: FSMContext):
    client_id = message.text
    # Retrieve user purchases data from the database
    user_purchases = sql_get_user_purchases(client_id)
    if user_purchases:
        # Display the purchase data
        for purchase in user_purchases:
            # Extract the relevant information from the purchase tuple
            user_id, item_name, description, first_name, last_name, username, purchase_date, price, total = purchase
            purchase_info = (f'💳 *Новая покупка!*\n👤 ID клиента: {user_id}\n🧑🏻‍🦰🧔🏻‍♂️ Имя клиента: {first_name} {last_name}\n'
                             f'📦 Товар: {item_name} {description}\n🌐 Пользователь: @{username}\n'
                             f'🕑 Дата: {purchase_date}\nЦена: {price}\nКоличество: {total}')
            await message.reply(purchase_info, parse_mode='Markdown')
    else:
        await message.reply("Клиента с данным ID нет в базе данных.")
    # Reset the state
    await state.finish()


# ================================ Скачивание excel файлов ================================
async def handle_purchases_download(message: types.Message):
    await message.reply('База данных пользователей оплативших товар')
    # Скачивание файла
    download_purchases()
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"pays-{current_datetime}.xlsx"
    with open(f'pays-{current_datetime}.xlsx', 'rb') as file:
        document = types.InputFile(file)
        document.metadata = {'filename': filename}
        await bot.send_document(message.chat.id, document=document)
    os.remove(filename)


async def handle_register_download(message: types.Message):
    await message.reply('База данных зарегистрированных пользователей')
    # Скачивание файла
    download_register_users()
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"users-register-{current_datetime}.xlsx"
    with open(f'users-register-{current_datetime}.xlsx', 'rb') as file:
        document = types.InputFile(file)
        document.metadata = {'filename': filename}
        await bot.send_document(message.chat.id, document=document)
    os.remove(filename)


async def handle_mir_shop_download(message: types.Message):
    await message.reply('База данных остатков по товарам')
    # Скачивание файла
    download_mir_shop()
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"MirShop-{current_datetime}.xlsx"
    with open(f'MirShop-{current_datetime}.xlsx', 'rb') as file:
        document = types.InputFile(file)
        document.metadata = {'filename': filename}
        await bot.send_document(message.chat.id, document=document)
    os.remove(filename)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(chat_moderator_text, commands=['textchat'])
    dp.register_message_handler(delete_item, commands='Удалить')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(pay_command, lambda message: message.text == 'Оплата')
    dp.register_message_handler(file_db_base_download, lambda message: message.text == 'FileBase')
    dp.register_message_handler(handle_purchases_download, lambda message: message.text == 'Оплата товара')
    dp.register_message_handler(handle_register_download, lambda message: message.text == 'Зарегистрированные')
    dp.register_message_handler(handle_mir_shop_download, lambda message: message.text == 'Товары/Остатки')
    dp.register_message_handler(back_moderator, lambda message: message.text == '🔙 Назад')
    dp.register_message_handler(set_moderator_id, lambda message: message.text == '📜🌇 Set Moderator')
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_category, state=FSMAdmin.category)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_total, state=FSMAdmin.total)
    dp.register_message_handler(process_client_id, state=SomeState.waiting_for_client_id)


# =============== Отправка фото ===============
# @dp.message_handler(content_types=types.ContentType.PHOTO)
@dp.message_handler(content_types=types.ContentType.PHOTO, state=DownloadPhotoState.waiting_for_photo)
async def handle_photo(message: types.Message, state: FSMContext):
    try:
        # Получение информации о фото
        photo = message.photo[-1]
        file_id = photo.file_id
        file = await bot.get_file(file_id)
        # Загрузка файла фотографии на сервер Telegram
        photo_path = f"photos/{file.file_path}"
        await bot.download_file(file.file_path, photo_path)
        # Открытие файла фотографии
        photo_file = open(photo_path, 'rb')
        # Получение имени отправителя, его имя, id, никнейм
        sender_name = message.from_user.full_name
        sender_id = message.from_user.id
        sender_username = message.from_user.username
        # Создание подписи
        photo_caption = f"Отправитель: {sender_name}\n👤 ID: {sender_id}\n🌐 Никнейм: @{sender_username}"
        # Отправка фото в ваш личный чат с подписью
        # Проверка, является ли отправитель модератором
        if message.text != '❌ Сбросить':
            if sender_id != moderator_id:
                # Отправка фото модератору
                await bot.send_photo(moderator_id, photo_file, caption=photo_caption)
                await message.reply("Фото успешно отправлено модератору. "
                                    "В ближайшее время с вами свяжется наш менеджер.")
                await state.finish()
            else:
                await message.reply("Вы уже являетесь модератором.")
                await state.finish()
    except aiogram.utils.exceptions.ChatIdIsEmpty:
        await message.reply("Модератор не назначен.")
        await state.finish()


# =============== Отправка текста ===============

@dp.message_handler(content_types=types.ContentType.TEXT, state=MyState.waiting_for_question)
async def process_question(message: types.Message, state: FSMContext):
    try:
        # Получаем текст сообщения от клиента
        message_text = message.text
        # Получение данных пользователя
        sender_id = message.from_user.id
        sender_first_name = message.from_user.first_name
        sender_last_name = message.from_user.last_name
        sender_username = message.from_user.username
        # Создание подписи
        caption = f"Отправитель: {sender_first_name} {sender_last_name}\n👤 ID: {sender_id}\n🌐 Никнейм: @{sender_username}\n\nТекст сообщения:"
        if message.text == '❌ Сбросить':
            await message.answer("Операция отменена.")
            await state.finish()
            return

        if sender_id != moderator_id:
            await bot.send_message(moderator_id, text=caption)
            # Отправляем сообщение в ваш личный чат
            await bot.send_message(moderator_id, text=message_text)
            await message.answer("Спасибо за ваш вопрос! Мы свяжемся с вами в ближайшее время.")
            await state.finish()
        else:
            await message.reply("Вы уже являетесь модератором.")
            await state.finish()
    except aiogram.utils.exceptions.ChatIdIsEmpty:
        await message.reply("Модератор не назначен.")
        await state.finish()


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
