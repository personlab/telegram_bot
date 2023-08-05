import sqlite3
import sqlite3 as sq
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import bot, GOOGLE
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
import gspread

# ======================== создание базы данных для товара магазина ========================


def sql_start():
    global base, cursor
    base = sq.connect('MirShop.db')
    cursor = base.cursor()
    if base:
        print('Shop Data base connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, category TEXT, name TEXT PRIMARY KEY, description TEXT, '
                 'price REAL, total REAL, added_date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    base.commit()

    load_user_shop()


# найти последний добавленный товар
def get_last_product(cursor):
    last_product = cursor.execute('SELECT * FROM menu ORDER BY added_date DESC LIMIT 1').fetchone()
    return last_product


# список всех пользователей, которые подписаны на рассылку
def get_subscribers(cursor_user_register):
    subscribers = cursor_user_register.execute('SELECT * FROM users WHERE newsletter = 1').fetchall()
    return subscribers


# отправить сообщения пользователям о новинках
async def send_new_product_to_subscribers():
    last_product = get_last_product(cursor)
    subscribers = get_subscribers(cursor_user_register)

    if last_product and subscribers:
        img, category, name, description, price, total, added_date = last_product

        # Создание inline ответа с информацией о товаре
        inline_message = f'🆕 Новинка 🆕\n📦 Категория: {category}\n📜 Название: {name}\n📜 Описание: {description}\n💳 Цена: {price} RUB\n📶 Количество: {total}'

        for user in subscribers:
            # Отправка inline ответа с фотографией и информацией о товаре
            await bot.send_photo(user[1], photo=img, caption=inline_message,
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton("Купить", callback_data=f"buy {name} 1")))


# ======================== отправка данных в гугл таблицы ========================


def load_user_shop():
    conn = sqlite3.connect('MirShop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu')
    all_user_pay_shop = cursor.fetchall()

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('TestMir/my-project-bot-88845-fac16c8795e1.json',
                                                                        scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(f'{GOOGLE}')
    worksheet = spreadsheet.get_worksheet(2)

    for user_pay_shop in all_user_pay_shop:
        data_values = [str(value) for value in user_pay_shop]
        item_name = data_values[2]
        item_total = data_values[5]

        # Поиск существующей записи с тем же товаром
        existing_cell = worksheet.find(item_name)
        if existing_cell:
            row_offset = existing_cell.row  # Получаем номер строки с существующей записью
            worksheet.update_cell(row_offset, 6, item_total)  # Обновляем значение total
        else:
            # Создаем новую запись
            worksheet.append_row(data_values)

    print('Данные успешно импортированы в таблицу Google.')
    conn.commit()
    conn.close()

# ======================== удаление из таблицы товары с нулевым остатком ========================


def delete_from_google_table(item_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('TestMir/my-project-bot-88845-fac16c8795e1.json',
                                                                        scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(f'{GOOGLE}')
    worksheet = spreadsheet.get_worksheet(2)

    existing_cell = worksheet.find(item_name)
    if existing_cell:
        row_offset = existing_cell.row
        worksheet.delete_row(row_offset)

    print('Запись успешно удалена из таблицы Google.')


# ============================== добавление товара в магазин при загрузке через админку =============================
async def sql_add_command(state):
    async with state.proxy() as data:
        # Получаем текущее время
        current_time = datetime.now()
        # Добавляем время в список значений
        data_values = list(data.values()) + [current_time]
        cursor.execute('INSERT INTO menu VALUES (?, ?, ?, ?, ?, ?, ?)', data_values)
        base.commit()


# ================================= Отображение товара  ==================================

async def sql_read(message, category):
    for ret in cursor.execute('SELECT * FROM menu WHERE category = ?', (category,)).fetchall():
        img = ret[0]
        category = ret[1]
        name = ret[2]
        description = ret[3]
        price = ret[4]
        total = ret[5]

        # Создание inline ответа с информацией о товаре
        inline_message = f'Категория: {category}\nНазвание: {name}\nОписание: {description}\nЦена: {price} RUB\nКоличество: {total}'

        # Отправка inline ответа с фотографией и информацией о товаре
        await bot.send_photo(message.chat.id, photo=img, caption=inline_message,
                             reply_markup=InlineKeyboardMarkup().add(
                                 InlineKeyboardButton("Купить", callback_data=f"buy {name} 1")))


# ============================== обновление/удаление товара из магазина если он продан =============================

def update_product_data(item_name, new_total):
    if new_total > 0:
        cursor.execute('UPDATE menu SET total = ? WHERE name = ?', (new_total, item_name))
    else:
        cursor.execute('DELETE FROM menu WHERE name = ?', (item_name,))
        delete_from_google_table(item_name)  # Добавьте эту строку для удаления из таблицы Google
    base.commit()


# ============================== вывод товара и удаление через админку =============================

async def sql_read2():
    return cursor.execute('SELECT * FROM menu').fetchall()


# ============================== кнопка удаления товара из магазина в админке =============================

async def sql_delete_command(data):
    cursor.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()


# ============================== получение данных о товаре применима в process_pay() =============================
def get_product_data(item_name):
    cursor.execute('SELECT * FROM menu WHERE name=?', (item_name,))
    return cursor.fetchone()


# =========================== Кнопки с отображением категорий и количества товаров в них =============================

async def show_categories(message):
    categories = cursor.execute('SELECT category, COUNT(*) FROM menu GROUP BY category').fetchall()
    keyboard = InlineKeyboardMarkup(row_width=2)
    for category, count in categories:
        keyboard.add(InlineKeyboardButton(f'{category} ({count})', callback_data=f'show_category {category}'))
    await bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=keyboard)


# ========================== получение всех остатков по товарам в файл excel ================================

def download_mir_shop():
    # Получение данных из базы данных
    purchases = sql_get_all_mir_shop()
    print(purchases)  # Отладочный вывод
    # Создание DataFrame из полученных данных
    df = pd.DataFrame(purchases, columns=['img', 'category', 'name', 'description', 'price', 'total', 'added_date'])
    # Создание файла Excel
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"MirShop-{current_datetime}.xlsx"
    df.to_excel(filename, index=False)


def sql_get_all_mir_shop():
    return cursor.execute('SELECT * FROM menu').fetchall()

# =================== ****************************************** ==========================


# =================== ****************************************** ==========================


# =================== ****************************************** ==========================


# =================== ****************************************** ==========================


# =================== ****************************************** ==========================


# =================== создание базы данных при регистрации клиента =========================

def register_start():
    global base_user_register, cursor_user_register
    base_user_register = sqlite3.connect('register_users.db', check_same_thread=False)
    cursor_user_register = base_user_register.cursor()

    if base_user_register:
        print('User Register Database connected successfully.')

    cursor_user_register.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        phone_number TEXT DEFAULT NULL,
        email_address TEXT DEFAULT NULL,
        purchase_date DATETIME,
        discount REAL DEFAULT 0,
        newsletter INTEGER DEFAULT 0,
        referrer_id INTEGER
        )''')

    cursor_user_register.execute('PRAGMA synchronous = OFF')


def update_newsletter_status(user_id: int, status: int):
    cursor_user_register.execute("UPDATE users SET newsletter = ? WHERE user_id = ?", (status, user_id))
    base_user_register.commit()


def get_newsletter_status(user_id: int) -> int:
    cursor_user_register.execute(
        """SELECT newsletter FROM users WHERE user_id = ?""",
        (user_id,)
    )
    result = cursor_user_register.fetchone()
    if result is not None:
        return result[0]
    return 0  # Если пользователя еще нет в базе данных, то считаем, что он не подписался



# ======================== отправляем данные о регистрации в google таблицы ========================


def load_data_to_google():
    conn = sqlite3.connect('register_users.db')
    cursor = conn.cursor()
    # Получить последнюю зарегистрированную запись
    cursor.execute('SELECT * FROM users')
    all_user_pay_shop = cursor.fetchall()

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('TestMir/my-project-bot-88845-fac16c8795e1.json', scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(f'{GOOGLE}')
    worksheet = spreadsheet.sheet1

    for user_pay_shop in all_user_pay_shop:
        data_values = [str(value) for value in user_pay_shop]
        user_id = data_values[1]
        phone_number = data_values[5]

        # Поиск существующей записи с тем же user_id
        existing_cell = worksheet.find(user_id)
        if existing_cell:
            row_offset = existing_cell.row  # Получаем номер строки с существующей записью
            worksheet.update_cell(row_offset, 6, phone_number)  # Обновляем значение phone_number
        else:
            # Создаем новую запись
            worksheet.append_row(data_values)

    print('Данные успешно импортированы в таблицу Google.')
    conn.commit()
    conn.close()


def load_data_to_google_email():
    conn = sqlite3.connect('register_users.db')
    cursor = conn.cursor()
    # Получить последнюю зарегистрированную запись
    cursor.execute('SELECT * FROM users')
    all_user_pay_shop = cursor.fetchall()

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('TestMir/my-project-bot-88845-fac16c8795e1.json', scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(f'{GOOGLE}')
    worksheet = spreadsheet.sheet1

    for user_pay_shop in all_user_pay_shop:
        data_values = [str(value) for value in user_pay_shop]
        user_id = data_values[1]
        email_address = data_values[6]

        # Поиск существующей записи с тем же user_id
        existing_cell = worksheet.find(user_id)
        if existing_cell:
            row_offset = existing_cell.row  # Получаем номер строки с существующей записью
            worksheet.update_cell(row_offset, 7, email_address)  # Обновляем значение email_address
        else:
            # Создаем новую запись
            worksheet.append_row(data_values)

    print('Данные успешно импортированы в таблицу Google.')
    conn.commit()
    conn.close()


def load_data_to_google_newsletterl():
    conn = sqlite3.connect('register_users.db')
    cursor = conn.cursor()
    # Получить последнюю зарегистрированную запись
    cursor.execute('SELECT * FROM users')
    all_user_pay_shop = cursor.fetchall()

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('TestMir/my-project-bot-88845-fac16c8795e1.json', scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(f'{GOOGLE}')
    worksheet = spreadsheet.sheet1

    for user_pay_shop in all_user_pay_shop:
        data_values = [str(value) for value in user_pay_shop]
        user_id = data_values[1]
        newsletter = data_values[9]

        # Поиск существующей записи с тем же user_id
        existing_cell = worksheet.find(user_id)
        if existing_cell:
            row_offset = existing_cell.row  # Получаем номер строки с существующей записью
            worksheet.update_cell(row_offset, 10, newsletter)  # Обновляем значение newsletter
        else:
            # Создаем новую запись
            worksheet.append_row(data_values)

    print('Данные успешно импортированы в таблицу Google.')
    conn.commit()
    conn.close()


def load_data_to_google_confirmation():
    conn = sqlite3.connect('register_users.db')
    cursor = conn.cursor()
    # Получить последнюю зарегистрированную запись
    cursor.execute('SELECT * FROM users')
    all_user_pay_shop = cursor.fetchall()

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('TestMir/my-project-bot-88845-fac16c8795e1.json', scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(f'{GOOGLE}')
    worksheet = spreadsheet.sheet1

    for user_pay_shop in all_user_pay_shop:
        data_values = [str(value) for value in user_pay_shop]
        user_id = data_values[1]
        newsletter = data_values[11]

        # Поиск существующей записи с тем же user_id
        existing_cell = worksheet.find(user_id)
        if existing_cell:
            row_offset = existing_cell.row  # Получаем номер строки с существующей записью
            worksheet.update_cell(row_offset, 12, newsletter)  # Обновляем значение confirmation
        else:
            # Создаем новую запись
            worksheet.append_row(data_values)

    print('Данные успешно импортированы в таблицу Google.')
    conn.commit()
    conn.close()


# ====================== проверяет данные пользователя при регистрации применима command_start() ======================
def user_exists(user_id):
    cursor_user_register.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    result = cursor_user_register.fetchall()
    return bool(len(result))


# ====================== реферальная система ======================
def add_user(user_id, username, first_name, last_name, phone_number, email_address, purchase_date, discount, newsletter, referrer_id=None):
    if user_exists(user_id):
        update_user(user_id, username, referrer_id)
    else:
        with base_user_register:
            if referrer_id is not None:
                cursor_user_register.execute('INSERT INTO users (user_id, username, first_name, last_name, phone_number, email_address, purchase_date, discount, newsletter, referrer_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                             (user_id, username, first_name, last_name, phone_number, email_address, purchase_date, discount, newsletter,  referrer_id))
            else:
                cursor_user_register.execute('INSERT INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)',
                                             (user_id, username, first_name, last_name, ))
        base_user_register.commit()


def on_user_register(user_id, username, first_name, last_name, phone_number, email_address, purchase_date, discount, newsletter, referrer_id=None):
    register_start()
    if not user_exists(user_id):
        add_user(user_id, username, first_name, last_name, phone_number, email_address, purchase_date, discount, newsletter, referrer_id)
    else:
        # Обновление данных пользователя
        update_user(user_id, username, first_name)


def update_user(user_id, username, referrer_id=None):
    if referrer_id is not None:
        cursor_user_register.execute('UPDATE users SET username = ?, referrer_id = ? WHERE user_id = ?',
                                     (username, referrer_id, user_id,))
    else:
        cursor_user_register.execute('UPDATE users SET username = ? WHERE user_id = ?',
                                     (username, user_id,))

    # Получаем количество рефералов для пользователя
    referral_count = count_referals(user_id)

    # Обновляем скидку в зависимости от количества рефералов
    if referral_count >= 5:
        discount = 0.15  # 15% скидка
    elif referral_count >= 3:
        discount = 0.10  # 10% скидка
    elif referral_count >= 1:
        discount = 0.05  # 5% скидка
    else:
        discount = 0  # Без скидки

    cursor_user_register.execute('UPDATE users SET discount = ? WHERE user_id = ?', (discount, user_id,))
    base_user_register.commit()


# ====================== подсчет рефералов (общая сеть) ======================
def count_referals(user_id):
    referred_users = set()
    to_check = [user_id]

    while to_check:
        current_user = to_check.pop()
        referred_users.add(current_user)

        query = 'SELECT user_id FROM users WHERE referrer_id = ?'
        result = cursor_user_register.execute(query, (current_user,)).fetchall()

        for row in result:
            to_check.append(row[0])

    return len(referred_users)


# ====================== получение данных о скидках пользователей. Применима process_buy() ======================
def get_discount(user_id):
    cursor_user_register.execute('SELECT discount FROM users WHERE user_id = ?', (user_id,))
    result = cursor_user_register.fetchone()
    if result:
        return result[0]
    else:
        return 0


# ========================== получение всех зарегистрированных пользователей в файл excel ==============================

def download_register_users():
    purchases = sql_get_all_register_users()
    print(purchases)
    df = pd.DataFrame(purchases, columns=['id', 'user_id', 'username', 'first_name', 'last_name', 'phone_number', 'email_address', 'purchase_date', 'discount', 'newsletter', 'referrer_id', 'confirmed_email'])
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"users-register-{current_datetime}.xlsx"
    df.to_excel(filename, index=False)


def sql_get_all_register_users():
    return cursor_user_register.execute('SELECT * FROM users').fetchall()


# =================== ****************************************** ==========================


# =================== ****************************************** ==========================


# =================== ****************************************** ==========================


# =================== ****************************************** ==========================


# =================== ****************************************** ==========================


# =================== создание базы данных о покупках клиента =========================

def sql_start_user_purchases():
    global base_user_purchases, cursor_user_purchases
    base_user_purchases = sq.connect('UserPay.db')
    cursor_user_purchases = base_user_purchases.cursor()
    if base_user_purchases:
        print('User Pay Data base connected OK')
    cursor_user_purchases.execute(
        'CREATE TABLE IF NOT EXISTS purchases ('
        'user_id INTEGER, category TEXT, item_name TEXT, description TEXT, first_name TEXT, '
        'last_name TEXT, username TEXT, purchase_date TEXT, subscription_date TEXT, price REAL, total REAL)')
    base_user_purchases.commit()
    print('Table purchases created')

    load_user_pay()

# ======================== отправляем данные в google таблицы ========================


def load_user_pay():
    conn = sqlite3.connect('UserPay.db')
    cursor = conn.cursor()

    # # Получаем последнюю запись о покупке
    cursor.execute('SELECT * FROM purchases ORDER BY purchase_date DESC LIMIT 1')
    last_user_pay_data = cursor.fetchone()

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('TestMir/my-project-bot-88845-fac16c8795e1.json',
                                                                        scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(f'{GOOGLE}')
    worksheet = spreadsheet.get_worksheet(1)

    # Получить заголовки столбцов
    header_values = ['user_id', 'category', 'item_name', 'description', 'first_name', 'last_name', 'username', 'purchase_date', 'subscription_date', 'price', 'total']

    # Если есть последняя зарегистрированная запись, добавить ее в таблицу
    if last_user_pay_data:
        data_values = [str(value) for value in last_user_pay_data]
        worksheet.append_row(data_values)
    else:
        # Если нет зарегистрированных записей, добавить только заголовки столбцов
        worksheet.append_row(header_values)

    print('Данные успешно импортированы в таблицу Google.')
    conn.commit()
    conn.close()


def sql_get_user_purchases(user_id):
    return cursor_user_purchases.execute('SELECT * FROM purchases WHERE user_id=?', (user_id,)).fetchall()


# ========================== получение всех пользователей оплативших товар в файл excel ================================

def download_purchases():
    purchases = sql_get_all_purchases()
    print(purchases)
    df = pd.DataFrame(purchases, columns=['user_id', 'category', 'item_name', 'description', 'first_name', 'last_name', 'username', 'purchase_date', 'subscription_date', 'price', 'total'])
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"pays-{current_datetime}.xlsx"
    df.to_excel(filename, index=False)


def sql_get_all_purchases():
    return cursor_user_purchases.execute('SELECT * FROM purchases').fetchall()






