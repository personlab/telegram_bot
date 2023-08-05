from datetime import datetime
import re
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile
from create_bot import bot, PASSWORD_YANDEX_ENV
from data_base import sqlite_db
from data_base.sqlite_db import load_data_to_google_email, load_data_to_google_confirmation
from handlers.other import ChangeEmailStates, EmailConfirmationState
from keyboards.client_kb import make_request_email_button, make_keyboard_98, make_reset_email_button
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


confirmation_code = None


def generate_confirmation_code():
    characters = string.ascii_letters + string.digits
    confirmation_code = ''.join(random.choice(characters) for _ in range(6))
    return confirmation_code


async def send_email_yandex(new_email):
    # Информация об отправителе и получателе
    sender_email = "personlabvip@yandex.ru"
    receiver_email = new_email
    password = PASSWORD_YANDEX_ENV
    smtp_server = "smtp.yandex.com"
    port = 587
    global confirmation_code
    confirmation_code = generate_confirmation_code()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        # Отправить подтверждение пользователю
        codes = (f'<h3 style="color:#2000a0"><b>Введите код в приложении чат-бота:</b></h3><h2 style="color:red"><b>{confirmation_code}</b></h2>'
                 f'<br><br>Пожалуйста, не отвечайте на это сообщение.<br><br>'
                 f'**********<br><br>Это письмо отправлено почтовым сервером mail.yandex.net')
        subject = 'Подтверждение email адреса в чат-боте'
        body = '<h3 style="color:#4000a0">Пожалуйста, подтвердите ваш email адрес.</h3>'

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        html = f"""\
                        <html>
                          <body>
                            <p>{body}</p>
                            <p>{codes}</p>
                          </body>
                        </html>
                        """

        part = MIMEText(html, "html")
        message.attach(part)

        server.sendmail(sender_email, receiver_email, message.as_string())


def get_confirmation_code():
    global confirmation_code
    return confirmation_code


async def process_phone_button_email(callback_query: CallbackQuery):
    photo = InputFile("TestMir/photos/b_telegram_cover.webp")
    await bot.send_photo(callback_query.message.chat.id, photo=photo)
    await bot.send_message(callback_query.from_user.id, '`Нажмите` *Email*, `чтобы добавить или изменить ваш адрес '
                                                        'электронной почты`', reply_markup=make_request_email_button(), parse_mode='Markdown')
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9]+(\.[a-zA-Z0-9_+-]+)*@[a-z]+\.[a-zA-Z]{2,3}$'
    return re.match(pattern, email) is not None


async def handle_email_input(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id

    await ChangeEmailStates.WAITING_FOR_NEW_EMAIL.set()
    await bot.send_message(message.from_user.id, 'Введите *Email Address*:\n\nПример: shop@shop.com '
                                                 '- shop.shop@shop.ru', reply_markup=make_reset_email_button(), parse_mode='Markdown')


async def process_new_email(message: types.Message, state: FSMContext):
    new_email = message.text
    purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    async with state.proxy() as data:
        data['new_email'] = new_email
        user_id = data['user_id']
    # Проверка email адреса с помощью регулярного выражения
    if not is_valid_email(new_email):
        await bot.send_message(message.from_user.id, 'Неверный формат email адреса.\n'
                                                     'Пример: shop@shop.com - shop.shop@shop.ru')
        return
    # Записать email в базу данных
    sqlite_db.cursor_user_register.execute("UPDATE users SET email_address = ?, purchase_date = ? WHERE user_id = ?", (new_email, purchase_date, user_id))
    sqlite_db.base_user_register.commit()

    await send_email_yandex(new_email)
    await EmailConfirmationState.CONFIRMATION.set()

    await message.answer(
        "*Письмо с подтверждением отправлено*.\n\nПожалуйста, проверьте свою почту, также проверьте папку(спам) "
        "и введите полученный код подтверждения.", parse_mode='Markdown')


async def process_email_confirmation(message: types.Message, state: FSMContext):
    confirmation_code = message.text

    # Проверка кода подтверждения
    if confirmation_code != get_confirmation_code():
        await message.answer("❌ Неверный код подтверждения. Пожалуйста, попробуйте еще раз.")
        return

    # Получение сохраненного email адреса
    async with state.proxy() as data:
        new_email = data['new_email']

    # Проверка существования столбца confirmed_email
    columns = sqlite_db.cursor_user_register.execute("PRAGMA table_info(users)").fetchall()
    column_names = [column[1] for column in columns]
    if 'confirmed_email' not in column_names:
        sqlite_db.cursor_user_register.execute("ALTER TABLE users ADD COLUMN confirmed_email INTEGER DEFAULT 0")

    # Обновление базы данных с подтвержденным email адресом
    sqlite_db.cursor_user_register.execute("UPDATE users SET confirmed_email = 1 WHERE email_address = ?", (new_email,))
    sqlite_db.base_user_register.commit()

    await message.answer("Email адрес успешно подтвержден! ✅", reply_markup=make_keyboard_98())
    load_data_to_google_email()
    load_data_to_google_confirmation()
    await state.finish()


async def reset_confirmation_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        new_email = data.get('new_email')
        user_id = data.get('user_id')

    if new_email:
        # Удалить email адрес из базы данных
        sqlite_db.cursor_user_register.execute("UPDATE users SET email_address = NULL WHERE user_id = ?", (user_id,))
        sqlite_db.base_user_register.commit()

    await state.reset_state()
    await message.answer('Подтверждение Email адреса сброшено. Введите *Email* для повторного подтверждения.',
                         parse_mode='Markdown')


def register_handler_email_address(dp: Dispatcher):
    dp.register_message_handler(handle_email_input, commands=['email'])
    dp.register_message_handler(handle_email_input, lambda message: message.text == 'Email', state='*')
    dp.register_message_handler(reset_confirmation_email, lambda message: message.text == 'Сбросить email', state='*')
    dp.register_message_handler(process_new_email, state=ChangeEmailStates.WAITING_FOR_NEW_EMAIL)
    dp.register_message_handler(process_email_confirmation, state=EmailConfirmationState.CONFIRMATION)

