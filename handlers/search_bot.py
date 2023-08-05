# from aiogram import types, Dispatcher
# import sqlite3
# from create_bot import bot, dp
#
# # =================================== поиск зарегистрированных по ID ===================================


# async def handle_search_command(message: types.Message):
#     reply_text_one = '`Поиск зарегистрированных пользователей`\n' \
#                  'Нажмите на кнопку и введите ID или никнейм пользователя:'
#
#     markup = types.InlineKeyboardMarkup()
#     button = types.InlineKeyboardButton(text='@SamKebabBot', switch_inline_query_current_chat=' ')
#     markup.add(button)
#
#     await bot.send_message(message.from_user.id, reply_text_one, reply_markup=markup, parse_mode='Markdown')
#
#
# async def search_user(message: types.Message):
#     if message.text.startswith('@SamKebabBot'):
#         query = message.text.replace('@SamKebabBot', '').strip()
#
#         base_user_register = sqlite3.connect('register_users.db', check_same_thread=False)
#         cursor_user_register = base_user_register.cursor()
#
#         cursor_user_register.execute('SELECT * FROM users WHERE user_id = ? OR username = ?', (query, query))
#         result = cursor_user_register.fetchone()
#
#         if result:
#             user_info = f"ID: {result[1]}\nUsername: {result[2]}\nFirst Name: {result[3]}\n" \
#                         f"Last Name: {result[4]}\nPurchase Date: {result[5]}\nReferrer ID: {result[6]}"
#             await message.reply(user_info)
#         else:
#             reply_text = '`Нет результатов`\n' \
#                          'Нажмите на кнопку и введите ID или никнейм пользователя:'
#
#             markup = types.InlineKeyboardMarkup()
#             # button = types.InlineKeyboardButton(
#             # text='@SamKebabBot', switch_inline_query='ID & никнейм') # открывает другой чат
#             button = types.InlineKeyboardButton(text='@SamKebabBot', switch_inline_query_current_chat=' ')
#             markup.add(button)
#
#             await bot.send_message(message.from_user.id, reply_text, reply_markup=markup, parse_mode='Markdown')
#
#
# def register_handler_search_bot(dp: Dispatcher):
#     dp.register_message_handler(handle_search_command, commands=['search'])
#     dp.register_message_handler(search_user)

