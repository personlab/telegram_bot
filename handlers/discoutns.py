from aiogram import types, Dispatcher
from aiogram.types import InputFile
from create_bot import bot


async def discount_history(message: types.Message):
    photo = InputFile("TestMir/photos/creative-black-friday.jpeg")
    await bot.send_photo(message.chat.id, photo=photo)
    await bot.send_message(message.from_user.id, '*Простая арифметика*, *чем больше ваша сеть*, *тем больше ваша скидка*.\n'
                                                 '*Всем зарегистрированным скидка* 5%\n'
                                                 '*Ваша сеть 100 человек*, скидка 15%\n'
                                                 '*Ваша сеть 200 человек*, скидка 20%\n'
                                                 '*Ваша сеть 500 человек*, скидка 30%\n'
                                                 '*Ваша сеть 1000 человек*, скидка 50% *на '
                                                 'все товары и услуги нашего магазина*.', parse_mode='Markdown')


def register_handler_hello_discount(dp: Dispatcher):
    dp.register_message_handler(discount_history, commands=['disc'])
