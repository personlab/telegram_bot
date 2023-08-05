from aiogram.contrib.middlewares.logging import LoggingMiddleware
from create_bot import dp, bot, logger_name, YOUR_CHAT_ID
from data_base import sqlite_db
import asyncio
from aiohttp import web
import aiohttp
from handlers import client, admin, other, welcome_page, hello_chat_message, number_phone, email_address, discoutns, \
    newsletter_user


async def on_startup(_):
    await bot.send_message(chat_id=YOUR_CHAT_ID, text='Бот запущен')
    await bot.set_webhook(url=f'https://{WEBAPP_HOST}:{WEBAPP_PORT}/webhook')
    sqlite_db.sql_start()
    sqlite_db.sql_start_user_purchases()
    sqlite_db.register_start()


async def on_shutdown(_):
    await bot.send_message(chat_id=YOUR_CHAT_ID, text='Бот остановлен')


async def handle_request(request: web.Request):
    update = await request.json()
    await dp.process_update(update)
    return web.Response()

WEBAPP_HOST = '141.8.192.214'
WEBAPP_PORT = 8443

app = web.Application()
app.router.add_post('/webhook', handle_request)


client.register_handlers_client(dp)
number_phone.register_handler_number_phone(dp)
email_address.register_handler_email_address(dp)
admin.register_handlers_admin(dp)
welcome_page.register_handler_welcome_page(dp)
hello_chat_message.register_handler_hello_chat_message(dp)
discoutns.register_handler_hello_discount(dp)
newsletter_user.register_handler_newsletter_user(dp)
other.register_handlers_other(dp)


async def run_bot():
    async with aiohttp.ClientSession() as session:
        dp.middleware.setup(LoggingMiddleware(logger=logger_name))
        await on_startup(None)  # Вызов функции on_startup вручную
        try:
            await dp.start_polling(reset_webhook=True)
        finally:
            await dp.storage.close()
            await dp.storage.wait_closed()
            await on_shutdown(None)  # Вызов функции on_shutdown вручную

try:
    asyncio.run(run_bot())
except KeyboardInterrupt:
    print("\nБот был остановлен с помощью клавиатуры (Ctrl+C)")
except Exception as e:
    print(f'Ошибка: {e}')



