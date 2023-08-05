from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# =========================== предоставить контакт при регистрации ===========================


def make_phone_button() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    button = types.InlineKeyboardButton(text='Предоставить номер телефона', callback_data='phone')
    keyboard.add(button)
    return keyboard


def make_request_contact_button() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton(text='Предоставить номер', request_contact=True)
    button_change_number = types.KeyboardButton('Изменить номер')
    button_back = types.KeyboardButton('🔙 Back')

    keyboard.add(button_change_number, button).add(button_back)
    return keyboard

# =========================== Профиль ===========================


def make_number_update_calls() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    button_call_update = types.InlineKeyboardButton(text='Изменить номер телефона 📲', callback_data='call_update')
    keyboard.add(button_call_update)
    return keyboard


# ========================================= Создание инлайн-кнопок для редактирования текста в чате


def button_text_more_link() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    item1 = types.InlineKeyboardButton(text='Изменить текст', callback_data='ChatText')
    item2 = types.InlineKeyboardButton(text='Действие', callback_data='MoreLink')
    item3 = types.InlineKeyboardButton(text='Ссылка', callback_data='Link')
    keyboard.add(item1, item2).add(item3)
    return keyboard

# ================= Блок кнопок привязанные к приветственному сообщению при вступлении в чат =================


register_referrals_678 = '\nПривет, друг, приглашаю тебя в новый интересный проект.\n'
link_chat_678 = 'https://t.me/testchat999'


def register_referrals_chat_button() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    button_link_share_678 = types.InlineKeyboardButton(text='Приглашение',
                                                       switch_inline_query='{} {}'.format(register_referrals_678,
                                                                                          link_chat_678))
    button = types.InlineKeyboardButton(text='Моя ссылка', url='https://t.me/SamKebabBot')
    keyboard.add(button, button_link_share_678)
    return keyboard


# =========================== Кнопки категорий ===========================


def button_category() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Одежда')
    button_two = types.KeyboardButton('Обувь')
    button_three = types.KeyboardButton('Куртки')
    button_fore = types.KeyboardButton('Электроника')
    keyboard.add(button, button_two).add(button_three, button_fore)
    return keyboard

# ======================= Кнопка для получения email ============================


def register_referrals_email() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    button = types.InlineKeyboardButton(text='Изменить/добавить email address 📧', callback_data='add_email')
    keyboard.add(button)
    return keyboard


def make_request_email_button() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_change_email = types.KeyboardButton('Email')
    button_back = types.KeyboardButton('🔙 Back')

    keyboard.add(button_back, button_change_email)
    return keyboard

# ================================ кнопки настройки в профиле =============================


def make_request_setting_button() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item5 = types.KeyboardButton('❓ Задать вопрос')
    button_setting = types.KeyboardButton('Настройки')
    button_GPT = types.KeyboardButton('ChatGPT 3.5 Turbo')
    item9 = types.KeyboardButton('🌎️Location')
    button_back = types.KeyboardButton('🔙 Вернуться назад')

    keyboard.add(item5, button_setting, item9).add(button_back, button_GPT)
    return keyboard


def make_profile_setting_button_back() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton('🔙 Back')

    keyboard.add(button_back)
    return keyboard


# ============================ Сброс номера телефона ============================
def make_reset_phone_button() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_reset = types.KeyboardButton('Сбросить')
    button_back = types.KeyboardButton('🔙 Back')

    keyboard.add(button_back, button_reset)
    return keyboard


# ============================ Сброс email ============================
def make_reset_email_button() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_reset = types.KeyboardButton('Сбросить email')
    button_change_email = types.KeyboardButton('Email')
    button_back = types.KeyboardButton('🔙 Back')

    keyboard.add(button_reset, button_change_email).add(button_back)
    return keyboard


# ============================ Сброс номера телефона ============================
def make_back_profile_button() -> types.ReplyKeyboardMarkup:
    button_back = types.KeyboardButton('🔙 Back')
    button_done_bak_profile = ReplyKeyboardMarkup(resize_keyboard=True).add(button_back)

    return button_done_bak_profile


# ============================ Сброс вопроса и возврат в профиль ===========================

def make_reset_questions_back_profile_button() -> types.ReplyKeyboardMarkup:
    button_reset_foto = types.KeyboardButton('❌ Сбросить')
    button_back = types.KeyboardButton('🔙 Back')

    button_done_bak = ReplyKeyboardMarkup(resize_keyboard=True).add(button_reset_foto, button_back)
    return button_done_bak


def make_reset_questions_back_menu_button() -> types.ReplyKeyboardMarkup:
    button_reset_foto = types.KeyboardButton('❌ Сбросить')
    button_back = types.KeyboardButton('🔙 Вернуться назад')

    button_done_bak = ReplyKeyboardMarkup(resize_keyboard=True).add(button_reset_foto, button_back)
    return button_done_bak


# ===================================== Кнопки доставщика ==================================

def make_request_location_button() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    location_button = types.KeyboardButton(text="Отправить", request_location=True)
    button_back = types.KeyboardButton('🔙 Back')

    keyboard.add(button_back, location_button)
    return keyboard

# ================= Кнопки для клиента =================


def make_keyboard_98() -> types.ReplyKeyboardMarkup:
    keyboard_98 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Профиль')
    item2 = types.KeyboardButton('Магазин')
    item3 = types.KeyboardButton('Menu 🛎')
    item4 = types.KeyboardButton('Каналы')
    button_together = KeyboardButton('🔓Open')

    keyboard_98.add(item1).add(item2, item3, item4).add(button_together)

    return keyboard_98

# ================= end Кнопки для клиента =================


















# создаем кнопку "Позвонить"
phone_button = types.InlineKeyboardButton(text='Позвонить 📞📲', url='https://t.me/KiselevOrel')
chat_button = types.InlineKeyboardButton(text='Chat 💬', url='https://t.me/Mebel_v_Orle')
# создаем клавиатуру и добавляем к ней кнопку "Позвонить"
keyboard = types.InlineKeyboardMarkup()
keyboard.add(phone_button, chat_button)

# ================= Кнопка для чата =================
sources_buttons = [
    InlineKeyboardButton('Позвонить 📞📲', url='https://t.me/KiselevOrel'),
    InlineKeyboardButton('Chat 💬', url='https://t.me/Mebel_v_Orle'),
]
inline_kb = InlineKeyboardMarkup(row_width=2).add(*sources_buttons)

keyboard_1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_1.add(types.KeyboardButton(text='Контакты'))
# ================= end Кнопка для чата =================

# # ================= Кнопки для клиента =================
#
#
# def make_keyboard() -> types.ReplyKeyboardMarkup:
#     keyboard_99 = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton('Зарегистрироваться')
#     item2 = types.KeyboardButton('Магазин')
#     item3 = types.KeyboardButton('Menu 🛎')
#     item4 = types.KeyboardButton('Каналы')
#     button_together = KeyboardButton('Для новичков')
#
#     keyboard_99.add(item1).add(item2, item3, item4).add(button_together)
#
#     return keyboard_99
# # ================= end Кнопки для клиента =================

# ================= Кнопки каналов ==================
button_movie = KeyboardButton('Кино и сериалы')
button_auto = KeyboardButton('Авто, Мото')
button_job = KeyboardButton('Работа и Вакансии')
button_love = KeyboardButton('Психология и Отношения')
button_beautiful = KeyboardButton('Красота и уход')
button_style = KeyboardButton('Мода и Стиль')
button_back = KeyboardButton('🔙 Вернуться назад')

button_case_sale = ReplyKeyboardMarkup(
    resize_keyboard=True).add(
    button_movie, button_auto).add(button_job, button_love).add(button_beautiful, button_style).add(button_back)
# ================= end Кнопки каналов ==================

# ================= Кнопки меню ==================
button_privileges = KeyboardButton('Льготы и поддержка')
button_token = KeyboardButton('Курсы токенов МИРа')
button_runet = KeyboardButton('Горячая десятка Рунета!')
button_directory = KeyboardButton("User's Digest")
button_back = KeyboardButton('🔙 Вернуться назад')

button_case_menu = ReplyKeyboardMarkup(
    resize_keyboard=True).add(
    button_privileges).add(button_runet).add(button_token, button_directory).add(button_back)
# ================= end Кнопки меню ==================

# ================= Подтверждение выполнения задания ==================

button_pay = KeyboardButton('✅ Подтверждение')
button_back = KeyboardButton('🔙 Вернуться назад')

button_done = ReplyKeyboardMarkup(resize_keyboard=True).add(button_back, button_pay)

# ================= end Подтверждение выполнения задания ==================

# ================= Инлайн кнопка чата ==================

chat_button = types.InlineKeyboardButton(text='Group of Scorpions 🦂', url='https://t.me/scorpions_vmeste/3')

keyboard_chat = types.InlineKeyboardMarkup()
keyboard_chat.add(chat_button)

# ================= end чат ==================

# ================= Инлайн кнопка для подтверждение выполнения задания ==================

chat_button = types.InlineKeyboardButton(text='Group of Scorpions 🦂', url='https://t.me/scorpions_vmeste/3')
button_download = types.InlineKeyboardButton(text='Загрузить', callback_data='download')

keyboard_chat_foto = types.InlineKeyboardMarkup()
keyboard_chat_foto.add(chat_button, button_download)

# ================= end Инлайн кнопка для подтверждение выполнения задания ==================

# ================= Инлайн кнопка кино ==================

kino_button = types.InlineKeyboardButton(text='Кино и сериалы', url='https://t.me/Kino_i_Serialy_Digest')
keyboard_kino = types.InlineKeyboardMarkup()
keyboard_kino.add(kino_button)

# ================= end кнопка кино ==================
# ================= Инлайн кнопка авто мото ==================

auto_moto_button = types.InlineKeyboardButton(text='Авто, Мото', url='https://t.me/AutoMoto_UD')
keyboard_auto_moto = types.InlineKeyboardMarkup()
keyboard_auto_moto.add(auto_moto_button)

# ================= end авто мото ==================
# ================= Инлайн кнопка Работа и Вакансии ==================

job_button = types.InlineKeyboardButton(text='Работа и Вакансии', url='https://t.me/Rabota_i_Vakansii_digest')
keyboard_job = types.InlineKeyboardMarkup()
keyboard_job.add(job_button)

# ================= end Работа и Вакансии ==================
# ================= Инлайн кнопка Психология и Отношения ==================

love_button = types.InlineKeyboardButton(text='Психология и Отношения', url='https://t.me/Psihologiya_i_Otnosheniya_digest')
keyboard_love = types.InlineKeyboardMarkup()
keyboard_love.add(love_button)

# ================= end Психология и Отношения ==================
# ================= Инлайн кнопка Красота и уход ==================

beautiful_button = types.InlineKeyboardButton(text='Красота и уход', url='https://t.me/Krasota_i_uhod_digest')
keyboard_beautiful = types.InlineKeyboardMarkup()
keyboard_beautiful.add(beautiful_button)

# ================= end Красота и уход ==================
# ================= Инлайн кнопка Красота и уход ==================

style_button = types.InlineKeyboardButton(text='Мода и Стиль', url='https://t.me/Moda_i_style_digest')
keyboard_style = types.InlineKeyboardMarkup()
keyboard_style.add(style_button)

# ================= end Красота и уход ==================
# # ================= Кнопка Сбросить ==================
#
# button_reset_foto = KeyboardButton('❌ Сбросить')
# button_back = KeyboardButton('🔙 Back')
#
# button_done_bak = ReplyKeyboardMarkup(resize_keyboard=True).add(button_reset_foto, button_back)

# ================= Кнопка Сбросить ==================
#
button_reset = KeyboardButton('❌ Сбросить')
button_comeback = KeyboardButton('🔙 Вернуться')

# Создаем клавиатуру и добавляем кнопку
keyboard_reset_back = ReplyKeyboardMarkup(resize_keyboard=True).add(button_reset, button_comeback)


# ================= Инлайн кнопка Льготы и поддержка ==================

kino_button = types.InlineKeyboardButton(text='Льготы и поддержка', url='https://t.me/Soobshestvo_Vmeste')
chat_button = types.InlineKeyboardButton(text='Chat 💬', url='https://t.me/scorpions_vmeste/3')
button_question = types.InlineKeyboardButton(text='❓ Задать вопрос', callback_data='top_question')

keyboard_support = types.InlineKeyboardMarkup()
keyboard_support.add(kino_button).add(chat_button, button_question)

# ================= end кнопка Льготы и поддержка ==================

# ================= Инлайн кнопка Чат игры «Вместе!» ==================

together_button = types.InlineKeyboardButton(text='Для новичков', url='https://t.me/+qBlXwZ5t3gcwMzFi')
keyboard_together = types.InlineKeyboardMarkup()
keyboard_together.add(together_button)

# ================= end кнопка Чат игры «Вместе!» ==================

# ================= Инлайн кнопка ChatGPT 3.5 Turbo ==================

ChatGPT_button = types.InlineKeyboardButton(text='ChatGPT 3.5 Turbo')
keyboard_ChatGPT = types.InlineKeyboardMarkup()
keyboard_ChatGPT.add(ChatGPT_button)



# ================= end кнопка ChatGPT 3.5 Turbo ==================

# ================= Инлайн кнопка Горячая десятка Рунета! ==================

runet_button = types.InlineKeyboardButton(text='Горячая десятка Рунета!', url='https://t.me/+nLW0BY4BYqEzMTYy')
keyboard_runet = types.InlineKeyboardMarkup()
keyboard_runet.add(runet_button)

# ================= end кнопка Горячая десятка Рунета! ==================

# ================= Инлайн кнопка User's Digest ==================

digest_button = types.InlineKeyboardButton(text="User's Digest", url='https://t.me/+jzo0CQ70Z3o5M2Fi')
keyboard_digest = types.InlineKeyboardMarkup()
keyboard_digest.add(digest_button)

# ================= end кнопка User's Digest ==================

# ================= Инлайн кнопка курсов токенов мира ==================

token_button = types.InlineKeyboardButton(text='Курсы токенов МИРа', url='https://t.me/Mirumir24_ru')
button_top = types.InlineKeyboardButton(text='Топ 10 монет', callback_data='top_coins')

keyboard_token = types.InlineKeyboardMarkup()
keyboard_token.add(token_button, button_top)
# ================= end кнопка курсов токенов мира ==================


# =========================================  Создание инлайн-кнопки для отправки в чат привязанный к боту
register_referrals = '\nПривет, друг, приглашаю тебя в новый интересный проект.\n'
link_chat = 'https://t.me/IanaBondarenko'

# =========================================  Создание инлайн-кнопки для отправки в чат привязанный к боту
button_link_share = types.InlineKeyboardButton(text='Пригласить друга в чат', switch_inline_query='{} {}'.format(register_referrals, link_chat))
button_text = types.InlineKeyboardButton(text='Получить реф.ссылку', url='https://t.me/SamKebabBot')
inline_keyboard_677 = InlineKeyboardMarkup(resize_keyboard=True).add(button_text).add(button_link_share)

# ================= Создаем инлайн кнопку "Отправить пригласительную ссылку" =================

# markup = types.InlineKeyboardMarkup()
# button = types.InlineKeyboardButton(text='@SamKebabBot', switch_inline_query='ID & никнейм')
# # button = types.InlineKeyboardButton(text='@SamKebabBot', switch_inline_query_current_chat=' ')
# markup.add(button)

# markup_register_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
# button_telegram = types.KeyboardButton(text='Telegram')
# button_whatsapp = types.KeyboardButton(text='WhatsApp')
# button_viber = types.KeyboardButton(text='Viber')
# markup_register_button.row(button_telegram)
# markup_register_button.row(button_whatsapp, button_viber)
#
# await bot.send_message(message.from_user.id, f'Выберите мессенджер для отправки приглаcительной ссылки:',
#                        reply_markup=markup_register_button)

# ================= end Создаем инлайн кнопку "Зарегистрироваться" =================
