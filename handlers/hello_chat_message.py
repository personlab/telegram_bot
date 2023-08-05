from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import bot
from handlers.other import GreetingStateChat, CallToActionStateChat, UpdateLinkStateChat
from keyboards.client_kb import button_text_more_link, register_referrals_chat_button


group_link_call = {'text_two': 'SamKebabBot', 'url_two': 'https://t.me/SamKebabBot'}
greeting_message_call = 'Сегодня в продажу поступил новый товар.\n\nСледуйте за нами [{text_two}]({url_two})\n\n'


async def set_greeting_chat(user_id):
    await bot.send_message(user_id, 'Введите текст для чата:')
    await GreetingStateChat.SettingGreetingChat.set()


async def process_greeting_step_chat(message: types.Message, state: FSMContext):
    global greeting_message_call
    greeting_message_call = '*'+message.text+'*' + ' [{text_two}]({url_two})\n\n'
    await bot.send_message(message.from_user.id, 'Приветствие успешно изменено! Посмотрите текущую ссылку:')
    await bot.send_message(message.chat.id, text=f"[{group_link_call['text_two']}]({group_link_call['url_two']})", parse_mode='Markdown')
    await state.finish()


async def set_call_to_action_chat(user_id):
    await bot.send_message(user_id, 'Введите новый текст призыва к действию:')
    await CallToActionStateChat.SettingCallToActionChat.set()


async def process_call_to_action_step_chat(message: types.Message, state: FSMContext):
    global group_link_call
    group_link_call['text_two'] = message.text
    await bot.send_message(message.from_user.id, 'Призыв к действию успешно изменен!')
    await state.finish()


async def link_to_update_chat(user_id):
    await bot.send_message(user_id, 'Введите новую ссылку:')
    await UpdateLinkStateChat.SettingLinkChat.set()


async def process_link_to_update_chat(message: types.Message, state: FSMContext):
    global group_link_call
    if 'https://' in message.text:
        group_link_call['url_two'] = message.text
        await bot.send_message(message.from_user.id, 'Ссылка успешно изменена!')
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Неверный формат ссылки, начинается с https://')


async def chat_hello_command_call(message: types.Message):
    await message.delete()
    chat_id = message.chat.id
    chat_member = await bot.get_chat_member(chat_id, message.from_user.id)
    if chat_member.status in ['administrator', 'creator']:
        formatted_greeting = greeting_message_call.format(**group_link_call)
        await bot.send_message(chat_id, text=formatted_greeting, parse_mode='Markdown',
                               reply_markup=register_referrals_chat_button())
    else:
        await bot.send_message(chat_id, "Команда вызова только в чатах.")
        formatted_greeting = greeting_message_call.format(**group_link_call)
        await bot.send_message(chat_id, text=formatted_greeting, parse_mode='Markdown',
                               reply_markup=register_referrals_chat_button())


async def set_greeting_chat_call(query: types.CallbackQuery):
    await set_greeting_chat(query.from_user.id)
    await query.message.edit_reply_markup()


async def set_call_to_action_chat_call(query: types.CallbackQuery):
    await set_call_to_action_chat(query.from_user.id)
    await query.message.edit_reply_markup()


async def link_to_update_chat_call(query: types.CallbackQuery):
    await link_to_update_chat(query.from_user.id)
    await query.message.edit_reply_markup()


def register_handler_hello_chat_message(dp: Dispatcher):
    dp.register_message_handler(chat_hello_command_call, commands=['chat_hello'])
    dp.register_callback_query_handler(set_greeting_chat_call, lambda query: query.data == 'ChatText')
    dp.register_message_handler(process_greeting_step_chat, state=GreetingStateChat.SettingGreetingChat)
    dp.register_callback_query_handler(set_call_to_action_chat_call, lambda query: query.data == 'MoreLink')
    dp.register_message_handler(process_call_to_action_step_chat, state=CallToActionStateChat.SettingCallToActionChat)
    dp.register_callback_query_handler(link_to_update_chat_call, lambda query: query.data == 'Link')
    dp.register_message_handler(process_link_to_update_chat, state=UpdateLinkStateChat.SettingLinkChat)
