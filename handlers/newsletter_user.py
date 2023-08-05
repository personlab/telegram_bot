from aiogram import types, Dispatcher
import typing
from create_bot import bot, dp
from data_base.sqlite_db import update_newsletter_status, get_newsletter_status


user_modes_newsletter = {}


async def send_reset_newsletter(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Вы можете оформить подписку. "
                                                         "Оставайтесь в курсе новинок нашего магазина.", reply_markup=markup_subscribe_newsletter(message.chat.id))


def markup_subscribe_newsletter(user_id: int) -> types.InlineKeyboardMarkup:
    subscribe_status = get_newsletter_status(user_id)
    subscribe_on = "✅" if subscribe_status == 1 else ""
    subscribe_off = "✅" if subscribe_status == 0 else ""

    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    item1 = types.InlineKeyboardButton(f"Подписаться {subscribe_on}", callback_data='subscribe_on')
    item2 = types.InlineKeyboardButton(f"Отписаться {subscribe_off}", callback_data='subscribe_off')
    markup.add(item1, item2)
    return markup


async def process_callback_newsletter(callback_query: types.CallbackQuery):
    global user_modes_newsletter
    user_id = callback_query.from_user.id
    user_modes_newsletter[user_id] = callback_query.data

    if user_modes_newsletter[user_id] == 'subscribe_on':
        update_newsletter_status(user_id, 1)  # обновляем статус подписки в базе данных
    elif user_modes_newsletter[user_id] == 'subscribe_off':
        update_newsletter_status(user_id, 0)  # обновляем статус подписки в базе данных
    else:
        return

    markup_subscribe = markup_subscribe_newsletter(user_id)

    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=markup_subscribe
    )
    await bot.answer_callback_query(callback_query.id)


def register_handler_newsletter_user(dp: Dispatcher):
    dp.register_callback_query_handler(process_callback_newsletter, lambda c: c.data in ['subscribe_on', 'subscribe_off'])




