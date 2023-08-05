from datetime import datetime
import re
from aiogram import Dispatcher, types
from aiogram.types import CallbackQuery, Message, ContentType
from create_bot import dp, bot
from data_base import sqlite_db
from data_base.sqlite_db import load_data_to_google
from handlers.other import ChangeNumberStates
from keyboards.client_kb import make_request_contact_button, make_keyboard_98, register_referrals_email, \
    make_reset_phone_button
from aiogram.dispatcher import FSMContext


async def process_phone_button(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Предоставьте доступ к вашим контактам', reply_markup=make_request_contact_button())
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


async def process_phone_button_two(message: types.Message):
    await bot.send_message(message.from_user.id, '*Выберите* изменить или добавить номер '
                                                 'телефона указанный в профиле `telegram`', reply_markup=make_request_contact_button(), parse_mode='Markdown')


async def process_phone_button_three(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, '*Выберите* изменить или добавить номер '
                                                        'телефона указанный в профиле `telegram`', reply_markup=make_request_contact_button(), parse_mode='Markdown')
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


async def process_contact(message: Message):
    phone_number = message.contact.phone_number
    first_name = message.contact.first_name
    user_id = message.from_user.id
    purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sqlite_db.cursor_user_register.execute("UPDATE users SET phone_number = ?, purchase_date = ? WHERE user_id = ?", (phone_number, purchase_date, user_id))
    sqlite_db.base_user_register.commit()

    await bot.send_message(message.from_user.id, 'Данные успешно добавлены!', parse_mode='Markdown')

    await bot.send_message(message.chat.id, f'Номер телефона: {phone_number}\nИмя: {first_name}\n\n'
                                            f'Нужно изменить/добавить Email?', reply_markup=register_referrals_email())

    load_data_to_google()


async def process_change_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id

    await ChangeNumberStates.WAITING_FOR_NEW_NUMBER.set()
    await bot.send_message(message.from_user.id, '*Введите новый номер телефона*:', reply_markup=make_reset_phone_button(), parse_mode='Markdown')


async def process_new_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    async with state.proxy() as data:
        user_id = data['user_id']
    # Проверка номера телефона с помощью регулярного выражения
    if not re.match(r'^\+[\d]+$', phone_number):
        await bot.send_message(message.from_user.id, '❌ Неверный формат номера телефона. Пожалуйста, введите номер в формате "+123456789".')
        return

    sqlite_db.cursor_user_register.execute("UPDATE users SET phone_number = ?, purchase_date = ? WHERE user_id = ?", (phone_number, purchase_date, user_id))
    sqlite_db.base_user_register.commit()

    await bot.send_message(message.from_user.id, 'Номер телефона успешно добавлен! ✅\n\n'
                                                 'Нужно изменить/добавить Email?', reply_markup=register_referrals_email())
    load_data_to_google()
    await state.finish()


async def reset_confirmation_phone(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("*Изменение номера телефона сброшено*.", parse_mode='Markdown')


def register_handler_number_phone(dp: Dispatcher):
    dp.register_message_handler(process_phone_button_two, commands=['call'])
    dp.register_message_handler(process_change_number, lambda message: message.text == 'Изменить номер', state='*')
    dp.register_message_handler(reset_confirmation_phone, lambda message: message.text == 'Сбросить', state='*')
    dp.register_callback_query_handler(process_phone_button, lambda c: c.data == 'phone')
    dp.register_message_handler(process_contact, content_types=ContentType.CONTACT)
    dp.register_message_handler(process_new_number, state=ChangeNumberStates.WAITING_FOR_NEW_NUMBER)
