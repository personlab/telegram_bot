from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from create_bot import bot
from keyboards.client_kb import make_keyboard_98
from keyboards.welcome_page_kb import questions_list, create_buttons, inline_keyboard_welcome_page

group_more = '[Узнать больше...](https://mirumir24.ru/)'


async def hello_world(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!\n\n'
                                                 f'`Мы рады приветствовать тебя в нашем проекте, если ты здесь, '
                                                 f'значит ты в поисках лучших возможностей.`\n\n'
                                                 f'*У нас есть для тебя интересное предложение*'
                           , parse_mode='Markdown', reply_markup=inline_keyboard_welcome_page)


async def process_callback_skript_1(callback_query: types.CallbackQuery, current_page=0):
    keyboard_98 = make_keyboard_98()
    await bot.answer_callback_query(callback_query.id)
    buttons_top_welcome_page = create_buttons(current_page)
    await bot.send_message(
        callback_query.from_user.id, f'*МИР - общественный проект. '
                                     f'Его владельцами являются пользователи. Никто, кроме них, не регулирует и не меняет '
                                     f'законы и жизнь государства МИР,  являющегося самоуправляемым, самофинансируемым '
                                     f'и саморазвивающимся феноменом, круглосуточно работающим и эволюционирующим на благо '
                                     f'пользователей.* {group_more}', reply_markup=keyboard_98, parse_mode='Markdown')

    question_photo = open(questions_list[0]['photo'], 'rb')
    question_content = questions_list[0]['content']
    send_photo_message = await bot.send_photo(
        callback_query.from_user.id,
        photo=question_photo,
        caption=f"*{question_content}*",
        parse_mode='Markdown',
        reply_markup=buttons_top_welcome_page
    )
    # сохраняем message_id отправленного фото
    callback_query.message.message_id = send_photo_message.message_id


async def process_callback(callback_query: CallbackQuery):
    direction, current_page = callback_query.data.split('_')
    current_page = int(current_page)

    if direction == "next":
        current_page += 1
    elif direction == "prev":
        current_page -= 1

    # Prevent going out of range
    if current_page < 0:
        current_page = 0
    if current_page >= len(questions_list):
        current_page = len(questions_list) - 1

    await bot.answer_callback_query(callback_query.id)
    question_photo = open(questions_list[current_page]['photo'], 'rb')
    question_content = questions_list[current_page]['content']
    media = types.InputMediaPhoto(question_photo, caption=f"*{question_content}*", parse_mode='Markdown')
    await bot.edit_message_media(
        media=media,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=create_buttons(current_page)
    )


def register_handler_welcome_page(dp: Dispatcher):
    dp.register_message_handler(hello_world, commands=['welcome'])
    dp.register_callback_query_handler(process_callback_skript_1, lambda c: c.data == 'skript_1')
    dp.register_callback_query_handler(process_callback, lambda c: c.data.startswith('next') or c.data.startswith('prev'))





