import sqlite3

from aiogram import types, Dispatcher
from aiogram.types import InputFile, MediaGroup
from aiogram.dispatcher import FSMContext
import datetime
from datetime import datetime

from create_bot import dp, bot, NICKNAME_BOT, YOUR_CHAT_ID
from data_base import sqlite_db
from data_base.sqlite_db import on_user_register, update_user, sql_read, show_categories, load_data_to_google_newsletterl

from handlers.email_address import process_phone_button_email
from handlers.newsletter_user import send_reset_newsletter
from handlers.number_phone import process_phone_button_three
from handlers.other import MyState, DownloadPhotoState, GreetingState, CallToActionState, UpdateLinkState, blockchaine_command_handler
from keyboards.client_kb import (button_case_sale, button_done, keyboard_chat, keyboard_kino, keyboard_auto_moto,
                                 keyboard_job, keyboard_love, keyboard_beautiful, keyboard_style, button_case_menu,
                                 keyboard_support, keyboard_runet, keyboard_digest, keyboard_chat_foto, keyboard_token,
                                 keyboard_reset_back, make_keyboard_98, make_phone_button, make_number_update_calls,
                                 register_referrals_chat_button, register_referrals_email, make_request_setting_button,
                                 make_profile_setting_button_back, make_reset_questions_back_profile_button,
                                 make_reset_questions_back_menu_button, make_request_location_button)
import asyncio
import os
import openai
from keyboards.gpt_kb import markup_Chat_gpt, button_done_gpt_turbo, gpt_button_setting
from data_base.db_gpt_chat import Database
import config


db = Database(config.db_path)
db.create_users_table()

openai.api_key = os.getenv('TOKEN_AI')

moderator_id = YOUR_CHAT_ID  # Заменить на ID текущего модератора


group_together = '[1️⃣ Изучи путеводитель по игре Вместе!](https://t.me/guide_Vmeste)'
group_together_two = '[2️⃣ Получи в подарок криптовалюту](https://t.me/crypto_Vmeste)'
group_together_three = '[3️⃣ Пройди обучение и начинай зарабатывать](http://academia.applovers.ru/lectures)'
group_together_fore = '[4️⃣ Сколько можно заработать за обучение?](https://t.me/payments_Vmeste)'


# ======================================== блок для изменения приветствия ========================================
#
group_link_start = {'text': 'сообщения', 'url': 'https://t.me/testchat999'}
greeting_message_start = 'Привет, {first_name} наш сервис работает для вас 24/7\n\nСледуйте инструкциям из этого [{text}]({url})\n\n'


async def get_user_data(user_id):
    user = db.get_user(user_id)
    if not user:
        db.add_new_user(user_id)
        user = db.get_user(user_id)
    return user


async def commands_gpt(message: types.Message):
    user = await get_user_data(message.from_user.id)
    await bot.send_message(message.from_user.id, f'`Привет {message.from_user.first_name}! OPEN AI`\n\n'
                                                 f'Строят генеративные модели, используя технологию глубокого обучения, '
                                                 f'которая использует большие объемы данных для обучения системы ИИ выполнению задачи.\n\n'
                                                 f'`175B Параметров в модели`\n\n'
                                                 f'`600k+ ГБ текста`\n\n'
                                                 f'`100M+ Активных пользователей`\n\n', reply_markup=gpt_button_setting(), parse_mode='Markdown')
    if user[2] == 'None':
        if user[1] <= 0:
            await bot.send_message(message.from_user.id, "Ваш лимит запросов исчерпан. Оформите, пожалуйста, подписку.",
                                   reply_markup=button_done_gpt_turbo)
        else:
            await bot.send_message(message.from_user.id, f'Привет! У вас осталось {user[1]} бесплатных запросов.')


async def command_start(message: types.Message):
    await message.delete()
    user = await get_user_data(message.from_user.id)
    photo = InputFile("TestMir/photos/b_telegram_cover.webp")
    await bot.send_photo(message.chat.id, photo=photo)
    formatted_greeting = greeting_message_start.format(first_name=message.from_user.first_name, **group_link_start)
    await bot.send_message(message.chat.id, text=formatted_greeting, parse_mode='Markdown')
    if not sqlite_db.user_exists(message.from_user.id):
        start_command = message.text
        user = message.from_user
        user_id = user.id
        first_name = user.first_name
        last_name = user.last_name
        phone_number = None
        email_address = None
        username = user.username
        purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        discount = None
        newsletter = None
        referrer_id = start_command.split("/start=")[-1]
        referrer_id = ''.join(filter(str.isdigit, referrer_id))
        on_user_register(user_id, username, first_name, last_name, phone_number, email_address, purchase_date, discount, newsletter, referrer_id)

        if referrer_id:
            if referrer_id != str(message.from_user.id):
                sqlite_db.add_user(message.from_user.id, username, first_name, last_name, phone_number, email_address, purchase_date, discount, newsletter, referrer_id)
                try:
                    await bot.send_message(referrer_id, f'По вашей ссылке зарегистрировался новый пользователь:\n'
                                                        f'👤 ID пользователя: {user_id}\n🦰🧔🏻‍ Имя: {first_name} {last_name}\n'
                                                        f'🌐 Никнейм: @{username}!')
                except:
                    pass
            else:
                await bot.send_message(message.from_user.id, 'Нельзя регистрироваться по собственной ссылке')
        else:
            sqlite_db.add_user(message.from_user.id, username, first_name, last_name, phone_number, email_address, purchase_date, discount, newsletter)
            await bot.send_message(
                message.from_user.id, 'Пожалуйста, предоставьте ваш номер телефона:', reply_markup=make_phone_button())
    else:
        await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы!')


# ======================================== блок для изменения приветствия ========================================


# @dp.message_handler(commands=['set_greeting'])
async def set_greeting(message: types.Message):
    await message.reply('Введите новое приветствие:')
    await GreetingState.SettingGreeting.set()


# @dp.message_handler(state=GreetingState.SettingGreeting)
async def process_greeting_step(message: types.Message, state: FSMContext):
    global greeting_message_start
    greeting_message_start = '*'+message.text+'*' + ' [{text}]({url})\n\n'
    await message.reply('Приветствие успешно изменено! Посмотрите текущую ссылку:')
    await bot.send_message(message.chat.id, text=f"[{group_link_start['text']}]({group_link_start['url']})", parse_mode='Markdown')
    await state.finish()


# @dp.message_handler(commands=['set_call_to_action'])
async def set_call_to_action(message: types.Message):
    await message.reply('Введите новый текст призыва к действию:')
    await CallToActionState.SettingCallToAction.set()


# @dp.message_handler(state=CallToActionState.SettingCallToAction)
async def process_call_to_action_step(message: types.Message, state: FSMContext):
    global group_link_start
    group_link_start['text'] = message.text
    await message.reply('Призыв к действию успешно изменен!')
    await state.finish()


# @dp.message_handler(commands=['link'])
async def link_to_update(message: types.Message):
    await message.reply('Введите новую ссылку')
    await UpdateLinkState.SettingLink.set()


# @dp.message_handler(state=CallToActionState.SettingCallToAction)
async def process_link_to_update(message: types.Message, state: FSMContext):
    global group_link_start
    if 'https://' in message.text:
        group_link_start['url'] = message.text
        await message.reply('Ссылка успешно изменена!')
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Неверный формат ссылки, начинается с https://')


async def on_chat_member_join_start(message: types.Message):
    chat_id = message.chat.id
    for new_member in message.new_chat_members:
        formatted_greeting = greeting_message_start.format(first_name=new_member.first_name, **group_link_start)
        await bot.send_message(chat_id, text=formatted_greeting, reply_to_message_id=message.message_id,
                               parse_mode='Markdown', reply_markup=register_referrals_chat_button())

# ======================================== конец блока для изменения приветствия =======================================


async def handle_profile(message: types.Message):
    await message.delete()
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    referral_link = f'https://t.me/{NICKNAME_BOT}?start={user_id}'
    update_user(user_id, username)
    sqlite_db.cursor_user_register.execute("SELECT discount FROM users WHERE user_id = ?", (user_id,))
    result = sqlite_db.cursor_user_register.fetchone()
    discount = result[0] if result else None
    # Проверяем наличие пользователя в базе данных подписчиков
    sqlite_db.cursor_user_register.execute('SELECT newsletter FROM users WHERE user_id = ?', (user_id,))
    result = sqlite_db.cursor_user_register.fetchone()
    newsletter = result[0] if result else None
    try:
        # Получить номер телефона из базы данных
        sqlite_db.cursor_user_register.execute("SELECT phone_number FROM users WHERE user_id = ?", (user_id,))
        result = sqlite_db.cursor_user_register.fetchone()
        phone_number = result[0] if result else None
        # Получить email из базы данных
        sqlite_db.cursor_user_register.execute("SELECT email_address FROM users WHERE user_id = ?", (user_id,))
        result = sqlite_db.cursor_user_register.fetchone()
        email_address = result[0] if result else None
    except sqlite3.OperationalError:
        await bot.send_message(message.from_user.id, 'Для доступа к профилю необходимо зарегистрироваться /start\n'
                                                     'Предоставить номер телефона /call\n'
                                                     'Адрес электронной почты /email')
        return

    if phone_number and email_address:
        await bot.send_message(message.from_user.id, f'👤 Ваш ID: {user_id}\n👤 Имя: {first_name} {last_name}\n'
                                                     f'🌐 Никнейм: @{username}\n'
                                                     f'📲 Номер телефона: {phone_number}\n'
                                                     f'📩 Email: {email_address}\n'
                                                     f'🈹 Ваша скидка: {discount}%\nБольше О СКИДКАХ\nУзнать /disc\n\n'
                                                     f'📬 Подписка на рассылки: {newsletter}\n\n'
                                                     f'🔗 Реферальная ссылка: {referral_link}\n'
                                                     f'👥 Количество рефералов: {sqlite_db.count_referals(message.from_user.id)}',
                               reply_markup=make_request_setting_button())
    else:
        await bot.send_message(message.from_user.id, 'Для доступа к профилю необходимо зарегистрироваться /start\n'
                                                     'Предоставить номер телефона /call\n'
                                                     'Адрес электронной почты /email')
        return

    register_referrals = '\nПривет, друг, приглашаю тебя в новый интересный проект.\n'
    text_message_hello = f'\nС уважением, {first_name} {last_name}.\n\n'

    markup_register_button = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='🔝 Telegram',
                                        switch_inline_query='{} {} {}'.format(register_referrals, text_message_hello,
                                                                              referral_link))
    button_whatsapp = types.InlineKeyboardButton(text='🔜 WhatsApp',
                                                 url=f'https://api.whatsapp.com/send?text={register_referrals}{text_message_hello}{referral_link}')
    markup_register_button.add(button, button_whatsapp)

    await bot.send_message(message.from_user.id, f'*Отправьте своему другу пригласительную регистрационную ссылку*:',
                           reply_markup=markup_register_button,
                           parse_mode='Markdown')
    load_data_to_google_newsletterl()


async def settings_phone_email(message: types.Message):
    photo = InputFile("TestMir/photos/settingsss.png")
    await bot.send_photo(message.chat.id, photo=photo)
    await bot.send_message(message.from_user.id, f'`Здесь вы можете изменить свои данные если`', reply_markup=make_profile_setting_button_back(), parse_mode='Markdown')
    await bot.send_message(message.from_user.id, f'*Ваш номер телефона изменился*?', reply_markup=make_number_update_calls(), parse_mode='Markdown')
    await bot.send_message(message.from_user.id, f'*Ваш email address изменился*?', reply_markup=register_referrals_email(), parse_mode='Markdown')
    await send_reset_newsletter(message)


async def item1_handler(message: types.Message):
    await message.delete()
    # координаты местоположения (широта и долгота)
    latitude, longitude = 52.91759031218117, 36.010957755275136
    await bot.send_message(message.from_user.id, '_Мы работаем:_\n\n'
                                                 '`Пн-Сб: 10:00 - 19:00`\n`Вс:    10:00 - 17:00`',
                           parse_mode='Markdown')
    await bot.send_location(message.from_user.id, latitude, longitude)


async def item2_handler(message: types.Message):
    await message.delete()
    request = "*Отправить мою локацию доставщику*."
    await bot.send_message(message.from_user.id, request, reply_markup=make_request_location_button(), parse_mode='Markdown')


async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    # Получение имени отправителя, его имя, id, никнейм
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    username = user.username

    message_user = f'Данные отправителя:\nИмя: {first_name}\nID: {user_id}\nНикнейм: @{username}'

    await bot.send_location(moderator_id, latitude, longitude)
    await bot.send_message(moderator_id, message_user)
    await message.reply("Спасибо за предоставленную геолокацию! Ваше местоположение получено.")


# ==================================== Магазин ========================================

async def item3_handler(message: types.Message):
    await message.delete()
    await show_categories(message)
    await bot.send_message(
        message.from_user.id, 'После оплаты выполните действия в инструкции "✅ Подтверждение" '
                              '*Это позволит ускорить процесс доставки товара*', reply_markup=button_done, parse_mode='Markdown')


async def handle_show_category(call):
    category = call.data.split()[1]
    await sql_read(call.message, category)


def startswith_show_category(call: types.CallbackQuery):
    return call.data.startswith('show_category')

# ==================================== end Магазин ========================================


async def item6_handler(message: types.Message):
    await message.delete()
    video = types.InputFile("TestMir/photos/IMG_6775.MP4")
    await bot.send_video(message.chat.id, video=video)
    await bot.send_message(message.from_user.id, 'Выберите раздел', reply_markup=button_case_menu)


async def menu_support(message: types.Message):
    await message.delete()
    currency_message_5 = await bot.send_message(
        message.from_user.id,
        f'`{message.from_user.first_name}, по вопросам обращайтесь в нашем чате или "❓ Задать вопрос" '
        f'через чат-бот на главном меню`'
        f'', reply_markup=keyboard_support, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def menu_together(message: types.Message):
    await message.delete()
    currency_message_5 = await bot.send_message(
        message.from_user.id, f'`{message.from_user.first_name}, ✅ ИНСТРУКЦИИ ДЛЯ НОВИЧКОВ ИГРЫ ВМЕСТЕ!`\n'
                              f'🌍 Уважаемый новичок игры!  Изучай материалы по ссылкам в указанном порядке.  '
                              f'Получи в подарок криптовалюту + базовую информацию об игре и твоих возможностях для получения доходов.'
                              f' Обучись им и начинай зарабатывать!\n\n{group_together}\n\n{group_together_two}\n\n'
                              f'{group_together_three}\n\n{group_together_fore}'
                              f'', parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def menu_runet(message: types.Message):
    await message.delete()
    photo = InputFile("TestMir/photos/photo_2023-07-09_03-05-16.jpg")
    await bot.send_photo(message.chat.id, photo=photo)
    currency_message_5 = await bot.send_message(
        message.from_user.id, f'{message.from_user.first_name}, каждый день тебя ждет горячая десятка из:\n\n'
                              f'`#НОВОСТИ_И_ОБЩЕСТВО, #ЭКОНОМИКА_И_БИЗНЕС\n#СЕМЬЯ_И_ДОМ, #КРАСОТА_И_ЗДОРОВЬЕ\n'
                              f'#НАУКА_И_ТЕХНИКА, #ЛИЧНОСТЬ_И_ОТНОШЕНИЯ,\n#ИНТЕРЕСНО_И_ПОЛЕЗНО, #ПОЗНАНИЕ\n'
                              f'#РАЗВЛЕЧЕНИЯ, #РАЗНОЕ`', reply_markup=keyboard_runet, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def menu_digest(message: types.Message):
    await message.delete()
    photo = InputFile("TestMir/photos/brain-games-quizzes-puzzles.png")
    await bot.send_photo(message.chat.id, photo=photo)
    currency_message_5 = await bot.send_message(
        message.from_user.id, f'{message.from_user.first_name}, лучшее для тебя со всего мира в одном месте!',
        reply_markup=keyboard_digest, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def menu_token(message: types.Message):
    await message.delete()
    video = types.InputFile("TestMir/photos/token_mir.mp4")
    await bot.send_video(message.chat.id, video=video)
    currency_message_5 = await bot.send_message(
        message.from_user.id, f'{message.from_user.first_name}, отслеживайте курс токенов в канале!',
        reply_markup=keyboard_token, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def item4_handler(message: types.Message):
    await message.delete()
    video = types.InputFile("TestMir/photos/IMG_6775.MP4")
    await bot.send_video(message.chat.id, video=video)
    await bot.send_message(message.from_user.id, 'Выберите тему.', reply_markup=button_case_sale)


async def item5_handler(message: types.Message):
    await message.delete()
    await message.answer("`Опишите свой вопрос`", reply_markup=make_reset_questions_back_profile_button(), parse_mode='Markdown')
    await MyState.waiting_for_question.set()


# @dp.message_handler(lambda message: message.text == '🔙 Сбросить/Вернуться назад', state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    # Сбрасываем состояние
    await state.reset_state()
    # Отправляем сообщение об отмене операции
    await message.answer("Операция отменена.")


async def muvie(message: types.Message):
    await message.delete()
    photo = InputFile("TestMir/photos/mouvi_original.jpg")
    await bot.send_photo(message.chat.id, photo=photo)
    currency_message_5 = await bot.send_message(
        message.from_user.id, f'`🎬 Кино и сериалы из авторитетных источников для тебя {message.from_user.first_name}`'
                              f'', reply_markup=keyboard_kino, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def auto_moto(message: types.Message):
    await message.delete()
    photo = InputFile("TestMir/photos/auto_moto.jpg")
    await bot.send_photo(message.chat.id, photo=photo)
    currency_message_5 = await bot.send_message(
        message.from_user.id,
        f'`🚛 Горячие новости мира Авто и Мото из авторитетных источников для тебя {message.from_user.first_name}`'
        f'', reply_markup=keyboard_auto_moto, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def job_but(message: types.Message):
    await message.delete()
    photo = InputFile("TestMir/photos/photo_2023-07-01_22-20-28.jpg")
    await bot.send_photo(message.chat.id, photo=photo)
    currency_message_5 = await bot.send_message(
        message.from_user.id,
        f'`📌 Работа и Вакансии из авторитетных источников для тебя {message.from_user.first_name}`'
        f'', reply_markup=keyboard_job, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def love(message: types.Message):
    await message.delete()
    photo = InputFile("TestMir/photos/Differences-Between-Love-And-Being-In-Love-Banner.jpg")
    await bot.send_photo(message.chat.id, photo=photo)
    currency_message_5 = await bot.send_message(
        message.from_user.id,
        f'`👩❤️👨 Психология и Отношения из авторитетных источников для тебя {message.from_user.first_name}`'
        f'', reply_markup=keyboard_love, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def beautiful(message: types.Message):
    await message.delete()
    photo = InputFile("TestMir/photos/beautiful.jpg")
    await bot.send_photo(message.chat.id, photo=photo)
    currency_message_5 = await bot.send_message(
        message.from_user.id, f'`💅🏼Красота и уход из авторитетных источников для тебя {message.from_user.first_name}`'
                              f'', reply_markup=keyboard_beautiful, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def style(message: types.Message):
    await message.delete()
    photo = InputFile("TestMir/photos/sop1.jpg")
    await bot.send_photo(message.chat.id, photo=photo)
    currency_message_5 = await bot.send_message(
        message.from_user.id, f'`👗Мода и Стиль из авторитетных источников для тебя {message.from_user.first_name}`'
                              f'', reply_markup=keyboard_style, parse_mode='Markdown')
    sent_message = currency_message_5
    await asyncio.sleep(60 * 5)
    await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)


async def go_back(message: types.Message):
    keyboard_98 = make_keyboard_98()
    await bot.send_message(
        message.from_user.id, f'`Пожалуйста, следуйте инструкциям в нашей группе`', reply_markup=keyboard_chat,
        parse_mode='Markdown'
    )
    address = 'Лучшее для вас со всего мира ✅'
    await bot.send_message(message.from_user.id, address, reply_markup=keyboard_98)


async def button_dones(message: types.Message):
    photos = [InputFile('TestMir/photos/chek_sberbank_online.jpg'),
              InputFile('TestMir/photos/chek.png'), InputFile('TestMir/photos/Снимок экрана 2023-07-11 050022.png')]
    media = MediaGroup()

    for photo in photos:
        media.attach_photo(photo)
    sent_messages = await bot.send_media_group(message.from_user.id, media=media)
    currency_message_7 = await bot.send_message(message.from_user.id,
                                                f'Пример чеков из приложений.\n\n`{message.from_user.first_name}, сделайте скриншот чека с оплатой'
                                                f' в мобильном приложении и чек из телеграм, которрый появится после оплаты.\n\n'
                                                f'Отправьте его в наш чат или загрузите фото в наш чат-бот для этого нажмите '
                                                f'на кнопку` "Загрузить" `после этого выберите фото на своем устройстве '
                                                f'и отправьте. Подписывать фотографии необязательно`',
                                                parse_mode='Markdown', reply_markup=keyboard_chat_foto)
    currency_message_8 = await bot.send_message(message.from_user.id,
                                                f'Хорошего дня, {message.from_user.first_name}!',
                                                parse_mode='Markdown', reply_markup=make_reset_questions_back_menu_button())
    await asyncio.sleep(60 * 5)  # задержка выполнения на 5 минут (300 секунд)
    for msg in sent_messages:
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    sent_messages_del = [currency_message_7, currency_message_8]
    for msg_two in sent_messages_del:
        await bot.delete_message(chat_id=msg_two.chat.id, message_id=msg_two.message_id)


async def delete_message(message: types.Message):
    await message.delete()


async def question_about_benefits_and_support(query: types.CallbackQuery):
    await query.message.delete()
    await query.message.answer("`Опишите свой вопрос`", reply_markup=keyboard_reset_back, parse_mode='Markdown')
    await MyState.waiting_for_question.set()


async def top_coins_handler(query: types.CallbackQuery):
    await blockchaine_command_handler(query.message)
    await query.message.delete()


async def download_command_handler(message: types.Message):
    # Устанавливаем состояние в waiting_for_photo
    await DownloadPhotoState.waiting_for_photo.set()
    # Отправляем сообщение с инструкцией
    await message.answer("Чтобы загрузить фото, пришлите его сюда.")


## ================================= сброс и выбор =========================================


async def reset_mode(message: types.Message):
    user_id = message.from_user.id
    user_modes.pop(user_id, None)
    await send_reset(message)


async def send_reset(message: types.Message):
    # photo = InputFile("tgbot3chat/images/ChatGPT.jpg")
    # await bot.send_photo(message.chat.id, photo=photo)
    await bot.send_message(chat_id=message.chat.id, text="Выбор режима:", reply_markup=markup_Chat_gpt)

## ================================= end сброс и выбор =========================================


## ================================= выбор режимма =========================================


user_modes = {}


@dp.callback_query_handler(lambda c: c.data in ['chatgpt_on', 'chatgpt_off'])
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_modes[user_id] = callback_query.data

    if user_modes[user_id] == 'chatgpt_on':
        chatgpt_on = "✅"
        chatgpt_off = ""
    elif user_modes[user_id] == 'chatgpt_off':
        chatgpt_on = ""
        chatgpt_off = "✅"
    else:
        chatgpt_on = ""
        chatgpt_off = ""

    # Обновляем разметку кнопок в сообщении
    markup_Chat_gpt = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(f"Включить {chatgpt_on}", callback_data='chatgpt_on')
    item2 = types.InlineKeyboardButton(f"Выключить {chatgpt_off}", callback_data='chatgpt_off')
    markup_Chat_gpt.add(item1, item2)

    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=markup_Chat_gpt)
    await bot.answer_callback_query(callback_query.id)

## ================================= end выбор режимма =========================================

# ============================= status =============================


async def send_status(message: types.Message):
    user_id = message.from_user.id
    mode = user_modes.get(user_id)
    if mode is None:
        await bot.send_message(user_id, "Вы еще не выбрали режим работы.")
    elif mode == "chatgpt_on":
        markup_Chat_gpt = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(f"Включить ✅", callback_data='chatgpt_on')
        item2 = types.InlineKeyboardButton(f"Выключить", callback_data='chatgpt_off')
        markup_Chat_gpt.add(item1, item2)
        await bot.send_message(user_id, "В данный момент GPT включен", reply_markup=markup_Chat_gpt)
    elif mode == "chatgpt_off":
        markup_Chat_gpt = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(f"Включить", callback_data='chatgpt_on')
        item2 = types.InlineKeyboardButton(f"Выключить ✅", callback_data='chatgpt_off')
        markup_Chat_gpt.add(item1, item2)
        await bot.send_message(user_id, "В данный момент GPT отключен", reply_markup=markup_Chat_gpt)


async def send_status_command(message: types.Message):
    await send_status(message)

# ============================= end status ===========================


dp.register_message_handler(reset_mode, commands=['reset'])
dp.register_message_handler(reset_mode, lambda message: message.text == 'Режим')
dp.register_message_handler(send_status_command, lambda message: message.text == 'Статус')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(handle_profile, lambda message: message.text == 'Профиль')
    dp.register_message_handler(settings_phone_email, lambda message: message.text == 'Настройки')
    dp.register_callback_query_handler(process_phone_button_three, lambda callback_query: callback_query.data == 'call_update')
    dp.register_callback_query_handler(process_phone_button_email, lambda callback_query: callback_query.data == 'add_email')
    dp.register_message_handler(set_greeting, lambda message: message.text == 'Приветствие')
    dp.register_message_handler(process_greeting_step, state=GreetingState.SettingGreeting)
    dp.register_message_handler(link_to_update, lambda message: message.text == 'Ссылка')
    dp.register_message_handler(process_link_to_update, state=UpdateLinkState.SettingLink)
    dp.register_message_handler(set_call_to_action, lambda message: message.text == 'Призыв к действию')
    dp.register_message_handler(process_call_to_action_step, state=CallToActionState.SettingCallToAction)
    dp.register_message_handler(item1_handler, lambda message: message.text == '🔓Open')
    dp.register_message_handler(item2_handler, lambda message: message.text == '🌎️Location')
    dp.register_message_handler(item3_handler, lambda message: message.text == 'Магазин')
    dp.register_message_handler(item6_handler, lambda message: message.text == 'Menu 🛎')
    dp.register_message_handler(menu_support, lambda message: message.text == 'Льготы и поддержка')
    dp.register_message_handler(menu_together, lambda message: message.text == 'Для новичков')
    dp.register_message_handler(menu_runet, lambda message: message.text == 'Горячая десятка Рунета!')
    dp.register_message_handler(commands_gpt, lambda message: message.text == 'ChatGPT 3.5 Turbo')
    dp.register_message_handler(menu_digest, lambda message: message.text == "User's Digest")
    dp.register_message_handler(menu_token, lambda message: message.text == 'Курсы токенов МИРа')
    dp.register_message_handler(item4_handler, lambda message: message.text == 'Каналы')
    dp.register_message_handler(item5_handler, lambda message: message.text == '❓ Задать вопрос')
    dp.register_message_handler(muvie, lambda message: message.text == 'Кино и сериалы')
    dp.register_message_handler(auto_moto, lambda message: message.text == 'Авто, Мото')
    dp.register_message_handler(job_but, lambda message: message.text == 'Работа и Вакансии')
    dp.register_message_handler(love, lambda message: message.text == 'Психология и Отношения')
    dp.register_message_handler(beautiful, lambda message: message.text == 'Красота и уход')
    dp.register_message_handler(style, lambda message: message.text == 'Мода и Стиль')
    dp.register_message_handler(go_back, lambda message: message.text == '🔙 Вернуться назад')
    dp.register_message_handler(item6_handler, lambda message: message.text == '🔙 Вернуться')
    dp.register_message_handler(button_dones, lambda message: message.text == '✅ Подтверждение')
    dp.register_callback_query_handler(download_command_handler, lambda c: c.data == 'download')
    dp.register_message_handler(cancel_handler, lambda message: message.text == '❌ Сбросить', state='*')
    dp.register_callback_query_handler(question_about_benefits_and_support, lambda query: query.data == 'top_question')
    dp.register_message_handler(handle_profile, lambda message: message.text == '🔙 Back')
    dp.register_callback_query_handler(top_coins_handler, lambda query: query.data == 'top_coins')
    dp.register_callback_query_handler(handle_show_category, startswith_show_category)
    dp.register_message_handler(on_chat_member_join_start, content_types=types.ContentType.NEW_CHAT_MEMBERS)
    dp.register_message_handler(handle_location, content_types=types.ContentType.LOCATION)




user_contexts = {}


@dp.message_handler(lambda message: user_modes.get(message.from_user.id) == 'chatgpt_on')
async def send(message: types.Message):
    user = await get_user_data(message.from_user.id)
    user_id = message.from_user.id
    mode = user_modes.get(user_id)
    if message.text.lower() == "/res":
        user_contexts.pop(user_id, None)
        await message.answer("❌ Контекст сброшен. Вы можете начать сначала.")
        return

    if mode == 'chatgpt_on':

        if user_id not in user_contexts:
            user_contexts[user_id] = [{"role": "system", "content": "You are a helpful assistant."}]

        user_contexts[user_id].append({"role": "user", "content": message.text})

        if user[2] == 'None' and user[1] > 0:
            processing_message = await message.answer("⏳ Пожалуйста, подождите...")
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=user_contexts[user_id],
                    temperature=0.5,
                    max_tokens=1024,
                )
            except openai.error.InvalidRequestError:
                await message.answer("⚠️ Произошла ошибка: ваш ответ содержит больше токенов, чем допустимо. "
                                     "Пожалуйста, сбросьте /res и измените запрос.")
                return
            except openai.error.APIError as e:
                await message.answer(f'⚠️ Произошла ошибка: {e}.\n'
                                     f'Повторите запрос, пожалуйста')
                return
            except openai.error.RateLimitError:
                await message.answer(f'Превышел лимит. '
                                     f'Пожалуйста, повторите запрос позже.')
                return

            except openai.error.ServiceUnavailableError:
                await message.answer(f'Сервер перегружен, повторите попытку. '
                                     f'Пожалуйста, сбросьте /res.')
                return

            await bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
            await message.answer(response['choices'][0]['message']['content'])
            user_contexts[user_id].append(
                {"role": "assistant", "content": response['choices'][0]['message']['content']})

            new_requests_count = user[1] - 1
            db.update_available_requests(user[0], new_requests_count)

        elif user[2] != 'None':
            subscription_date = datetime.strptime(user[2], '%Y-%m-%d %H:%M:%S')

            if (datetime.now() - subscription_date).days >= 30:
                db.update_available_requests(user[0], 0)
                db.update_subscription_date(user[0], 'None')
                user_contexts.pop(user_id, None)
                await bot.send_message(message.from_user.id, "Ваша подписка истекла. Оформите, пожалуйста, подписку.",
                                       reply_markup=button_done_gpt_turbo)
                return
            else:
                if message.text.lower() == "/res":
                    user_contexts.pop(user_id, None)
                    await message.answer("❌ Контекст сброшен. Вы можете начать сначала.")
                    return

                processing_message = await message.answer("⏳ Пожалуйста, подождите...")
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-0613",
                        messages=user_contexts[user_id],
                        temperature=0.5,
                        max_tokens=1024,
                    )
                except openai.error.InvalidRequestError:
                    await message.answer("⚠️ Произошла ошибка: ваш ответ содержит больше токенов, чем допустимо. "
                                         "Пожалуйста, сбросьте /res и измените запрос.")
                    return

                except openai.error.APIError as e:
                    await message.answer(f'⚠️ Произошла ошибка: {e}.\n'
                                         f'Повторите запрос, пожалуйста')
                    return

                except openai.error.RateLimitError:
                    await message.answer(f'Превышел лимит. '
                                         f'Пожалуйста, повторите запрос позже.')
                    return

                except openai.error.ServiceUnavailableError:
                    await message.answer(f'Сервер перегружен, повторите попытку. '
                                         f'Пожалуйста, сбросьте /res.')
                    return

                await bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)

                await message.answer(response['choices'][0]['message']['content'])
                user_contexts[user_id].append(
                    {"role": "assistant", "content": response['choices'][0]['message']['content']})

        else:
            await bot.send_message(message.from_user.id, "Ваш лимит запросов исчерпан. Оформите, пожалуйста, подписку.",
                                   reply_markup=button_done_gpt_turbo)




