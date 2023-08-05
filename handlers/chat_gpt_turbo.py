# import os
# import openai
# from aiogram.types import InputFile, ContentType
#
# from create_bot import dp, bot, YOOKassa
# from aiogram import types, Dispatcher
# import datetime
#
# from data_base import sqlite_db
# from handlers.client import item3_handler, item6_handler
# from keyboards.client_kb import button_done, button_case_menu
# from keyboards.gpt_kb import markup_Chat_gpt, button_done_gpt_turbo
# from data_base.db_gpt_chat import Database
# import config
#
#
# db = Database(config.db_path)
# db.create_users_table()
#
# openai.api_key = os.getenv('TOKEN_AI')
#
#
# async def get_user_data(user_id):
#     user = db.get_user(user_id)
#     if not user:
#         db.add_new_user(user_id)
#         user = db.get_user(user_id)
#     return user
#
#
# counter = 10
#
#
# async def commands_gpt(message: types.Message):
#     user = await get_user_data(message.from_user.id)
#     await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}!\n\n'
#                                                  f'выберите режим работы /reset')
#     if user[2] == 'None':
#         if user[1] <= 0:
#             await bot.send_message(message.from_user.id, "Ваш лимит запросов исчерпан. Оформите, пожалуйста, подписку.",
#                                    reply_markup=button_done_gpt_turbo)
#         else:
#             await bot.send_message(message.from_user.id, f'Привет! У вас осталось {user[1]} бесплатных запросов.')
#
#
# ## ================================= сброс и выбор =========================================
#
#
# async def reset_mode(message: types.Message):
#     user_id = message.from_user.id
#     user_modes.pop(user_id, None)
#     await send_reset(message)
#
#
# async def send_reset(message: types.Message):
#     # photo = InputFile("tgbot3chat/images/ChatGPT.jpg")
#     # await bot.send_photo(message.chat.id, photo=photo)
#     await bot.send_message(chat_id=message.chat.id, text="Выбор режима:", reply_markup=markup_Chat_gpt)
#
# ## ================================= end сброс и выбор =========================================
#
#
# ## ================================= выбор режимма =========================================
#
#
# user_modes = {}
#
#
# @dp.callback_query_handler(lambda c: c.data in ['chatgpt_on', 'chatgpt_off'])
# async def process_callback(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     user_modes[user_id] = callback_query.data
#
#     if user_modes[user_id] == 'chatgpt_on':
#         chatgpt_on = "✅"
#         chatgpt_off = ""
#     elif user_modes[user_id] == 'chatgpt_off':
#         chatgpt_on = ""
#         chatgpt_off = "✅"
#     else:
#         chatgpt_on = ""
#         chatgpt_off = ""
#
#     # Обновляем разметку кнопок в сообщении
#     markup_Chat_gpt = types.InlineKeyboardMarkup(row_width=2)
#     item1 = types.InlineKeyboardButton(f"Включить {chatgpt_on}", callback_data='chatgpt_on')
#     item2 = types.InlineKeyboardButton(f"Выключить {chatgpt_off}", callback_data='chatgpt_off')
#     markup_Chat_gpt.add(item1, item2)
#
#     await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=markup_Chat_gpt)
#     await bot.answer_callback_query(callback_query.id)
#
# ## ================================= end выбор режимма =========================================
#
# # ============================= status =============================
#
#
# async def send_status(message: types.Message):
#     user_id = message.from_user.id
#     mode = user_modes.get(user_id)
#     if mode is None:
#         await bot.send_message(user_id, "Вы еще не выбрали режим работы.")
#     elif mode == "chatgpt_on":
#         markup_Chat_gpt = types.InlineKeyboardMarkup(row_width=2)
#         item1 = types.InlineKeyboardButton(f"Включить ✅", callback_data='chatgpt_on')
#         item2 = types.InlineKeyboardButton(f"Выключить", callback_data='chatgpt_off')
#         markup_Chat_gpt.add(item1, item2)
#         await bot.send_message(user_id, "В данный момент GPT включен", reply_markup=markup_Chat_gpt)
#     elif mode == "chatgpt_off":
#         markup_Chat_gpt = types.InlineKeyboardMarkup(row_width=2)
#         item1 = types.InlineKeyboardButton(f"Включить", callback_data='chatgpt_on')
#         item2 = types.InlineKeyboardButton(f"Выключить ✅", callback_data='chatgpt_off')
#         markup_Chat_gpt.add(item1, item2)
#         await bot.send_message(user_id, "В данный момент GPT отключен", reply_markup=markup_Chat_gpt)
#
#
# async def send_status_command(message: types.Message):
#     await send_status(message)
#
# # ============================= end status ===========================
#
# # dp.register_message_handler(commands_gpt, commands=['gpt'])
# dp.register_message_handler(reset_mode, commands=['reset'])
# dp.register_message_handler(send_reset, commands=['str'])
# dp.register_message_handler(send_status_command, commands=['status'])
#
#
# def register_handler_chat_gpt_turbo(dp: Dispatcher):
#     dp.register_message_handler(item3_handler, lambda message: message.text == 'Магазин')
#     dp.register_message_handler(item6_handler, lambda message: message.text == '🔙 Вернуться назад')
    # dp.register_callback_query_handler(process_callback, lambda c: c.data in ['chatgpt_on', 'chatgpt_off'])


# user_contexts = {}
#
#
# @dp.message_handler(lambda message: user_modes.get(message.from_user.id) == 'chatgpt_on')
# async def send(message: types.Message):
#     user = await get_user_data(message.from_user.id)
#     user_id = message.from_user.id
#     mode = user_modes.get(user_id)
#     if message.text.lower() == "/res":
#         user_contexts.pop(user_id, None)
#         await message.answer("❌ Контекст сброшен. Вы можете начать сначала.")
#         return
#
#     if mode == 'chatgpt_on':
#
#         if user_id not in user_contexts:
#             user_contexts[user_id] = [{"role": "system", "content": "You are a helpful assistant."}]
#
#         user_contexts[user_id].append({"role": "user", "content": message.text})
#
#         if user[2] == 'None' and user[1] > 0:
#             processing_message = await message.answer("⏳ Пожалуйста, подождите...")
#             try:
#                 response = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo-0613",
#                     messages=user_contexts[user_id],
#                     temperature=0.5,
#                     max_tokens=1024,
#                 )
#             except openai.error.InvalidRequestError:
#                 await message.answer("⚠️ Произошла ошибка: ваш ответ содержит больше токенов, чем допустимо. "
#                                      "Пожалуйста, сбросьте /res и измените запрос.")
#                 return
#             except openai.error.APIError as e:
#                 await message.answer(f'⚠️ Произошла ошибка: {e}.\n'
#                                      f'Повторите запрос, пожалуйста')
#                 return
#             except openai.error.RateLimitError:
#                 await message.answer(f'Превышел лимит. '
#                                      f'Пожалуйста, повторите запрос позже.')
#                 return
#
#             except openai.error.ServiceUnavailableError:
#                 await message.answer(f'Сервер перегружен, повторите попытку. '
#                                      f'Пожалуйста, сбросьте /res.')
#                 return
#
#             await bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
#             await message.answer(response['choices'][0]['message']['content'])
#             user_contexts[user_id].append(
#                 {"role": "assistant", "content": response['choices'][0]['message']['content']})
#
#             new_requests_count = user[1] - 1
#             db.update_available_requests(user[0], new_requests_count)
#
#         elif user[2] != 'None':
#             subscription_date = datetime.datetime.strptime(user[2], '%Y-%m-%d %H:%M:%S')
#
#             if (datetime.datetime.now() - subscription_date).days >= 30:
#                 db.update_available_requests(user[0], 0)
#                 db.update_subscription_date(user[0], 'None')
#                 user_contexts.pop(user_id, None)
#                 await bot.send_message(message.from_user.id, "Ваша подписка истекла. Оформите, пожалуйста, подписку.",
#                                        reply_markup=button_done_gpt_turbo)
#                 return
#             else:
#                 if message.text.lower() == "/res":
#                     user_contexts.pop(user_id, None)
#                     await message.answer("❌ Контекст сброшен. Вы можете начать сначала.")
#                     return
#
#                 processing_message = await message.answer("⏳ Пожалуйста, подождите...")
#                 try:
#                     response = openai.ChatCompletion.create(
#                         model="gpt-3.5-turbo-0613",
#                         messages=user_contexts[user_id],
#                         temperature=0.5,
#                         max_tokens=1024,
#                     )
#                 except openai.error.InvalidRequestError:
#                     await message.answer("⚠️ Произошла ошибка: ваш ответ содержит больше токенов, чем допустимо. "
#                                          "Пожалуйста, сбросьте /res и измените запрос.")
#                     return
#
#                 except openai.error.APIError as e:
#                     await message.answer(f'⚠️ Произошла ошибка: {e}.\n'
#                                          f'Повторите запрос, пожалуйста')
#                     return
#
#                 except openai.error.RateLimitError:
#                     await message.answer(f'Превышел лимит. '
#                                          f'Пожалуйста, повторите запрос позже.')
#                     return
#
#                 except openai.error.ServiceUnavailableError:
#                     await message.answer(f'Сервер перегружен, повторите попытку. '
#                                          f'Пожалуйста, сбросьте /res.')
#                     return
#
#                 await bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
#
#                 await message.answer(response['choices'][0]['message']['content'])
#                 user_contexts[user_id].append(
#                     {"role": "assistant", "content": response['choices'][0]['message']['content']})
#
#         else:
#             await bot.send_message(message.from_user.id, "Ваш лимит запросов исчерпан. Оформите, пожалуйста, подписку.",
#                                    reply_markup=button_done_gpt_turbo)




