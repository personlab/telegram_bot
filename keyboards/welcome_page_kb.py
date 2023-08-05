from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import os
print(os.getcwd())

questions_list = [
    {
        "photo": "TestMir/team/ElenaPoperedina.jpg",
        "content": "Елена Попередина\n\nПремьер-министр"
    },
    {
        "photo": "TestMir/team/PavelGoncharov.jpg",
        "content": "Павел Гончаров\n\nВице-премьер"
    },
    {
        "photo": "TestMir/team/VadimLibman.jpg",
        "content": "Вадим Либман\n\nМинистр Развития"
    },
    {
        "photo": "TestMir/team/GennadyFurman.jpg",
        "content": "Геннадий Фурман\n\nМинистр Технологий"
    },
    {
        "photo": "TestMir/team/RamilAkhmetshin.jpg",
        "content": "Рамиль Ахметшин\n\nМинистр Юстиции"
    },
    {
        "photo": "TestMir/team/RamisKafiyatov.jpg",
        "content": "Рамис Кафиятов\n\nМинистр Финансов"
    },
    {
        "photo": "TestMir/team/PavelMetelkin.jpg",
        "content": "Павел Метелкин\n\nМинистр Коммерции"
    },
    {
        "photo": "TestMir/team/TalgatCairov.jpg",
        "content": "Талгат Каиров\n\nМинистр Занятости"
    },
    {
        "photo": "TestMir/team/JuliaAlexandrova.jpg",
        "content": "Юлия Александрова\n\nМинистр Информации"
    },
    {
        "photo": "TestMir/team/OlgaAkhmetshina.jpg",
        "content": "Ольга Ахметшина\n\nМинистр Культуры"
    },
    {
        "photo": "TestMir/team/DenisViduto.jpg",
        "content": "Денис Видуто\n\nМинистр Рекреации"
    },
    {
        "photo": "TestMir/team/YanaBondarenko.jpg",
        "content": "Яна Бондаренко\n\nМинистр Здравоохранения"
    },
    {
        "photo": "TestMir/team/IgorDinerstein.jpg",
        "content": "Игорь Динерштейн\n\nМинистр Заботы"
    },
    {
        "photo": "TestMir/team/VladimirFilippov.jpg",
        "content": "Владимир Филиппов\n\nМинистр Образования"
    },
    {
        "photo": "TestMir/team/AlexanderStrelnikov.jpg",
        "content": "Александр Стрельников\n\nМинистр Имущества"
    },
    {
        "photo": "TestMir/team/MariaPetrova.jpg",
        "content": "Мария Петрова\n\nМинистр Благотворительности"
    },
    {
        "photo": "TestMir/team/AlexanderDmitriev.jpg",
        "content": "Александр Дмитриев\n\nМинистр Коммуникаций"
    },
    {
        "photo": "TestMir/team/OlesyaFilimonova.jpg",
        "content": "Олеся Филимонова\n\nМинистр Интеграции"
    },
    {
        "photo": "TestMir/team/YuriZanikov.jpg",
        "content": "Юрий Заников\n\nМинистр Безопасности"
    },
    {
        "photo": "TestMir/team/OksanaTarasova.jpg",
        "content": "Оксана Тарасова\n\nМинистр Внутренних дел"
    }
]


def create_buttons(current_page=0):
    buttons_top_welcome_page = types.InlineKeyboardMarkup(row_width=2)
    buttons = []

    if current_page > 0:
        buttons.append(types.InlineKeyboardButton("🔙 Назад", callback_data=f"prev_{current_page}"))
    if current_page < len(questions_list) - 1:
        buttons.append(types.InlineKeyboardButton("Вперед 🔜", callback_data=f"next_{current_page}"))

    buttons_top_welcome_page.add(*buttons)
    return buttons_top_welcome_page


more = InlineKeyboardButton(text='Познакомься с нашей командой', callback_data='skript_1')
inline_keyboard_welcome_page = InlineKeyboardMarkup().add(more)


