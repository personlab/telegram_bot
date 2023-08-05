from aiogram import types


# Кнопки клавиатуры админа
button_text = types.KeyboardButton('Приветствие')
button_link = types.KeyboardButton('Ссылка')
button_go = types.KeyboardButton('Призыв к действию')
button_pay = types.KeyboardButton('Оплата')
button_file_db = types.KeyboardButton('FileBase')
button_load = types.KeyboardButton('/Загрузить')
cancellation = types.KeyboardButton('/Отмена')
button_delete = types.KeyboardButton('/Удалить')
button_back = types.KeyboardButton('🔙 Вернуться назад')
button_set_moderator = types.KeyboardButton('📜🌇 Set Moderator')


button_case_admin = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_load, cancellation, button_delete).add(
    button_text, button_link, button_pay).add(button_go, button_file_db).add(button_back, button_set_moderator)


button_product = types.KeyboardButton('Оплата товара')
button_register_user = types.KeyboardButton('Зарегистрированные')
button_leftovers = types.KeyboardButton('Товары/Остатки')
button_back_moder = types.KeyboardButton('🔙 Назад')

keyboard_base_db = types.ReplyKeyboardMarkup(
    resize_keyboard=True).add(button_product, button_register_user).add(button_back_moder, button_leftovers)




