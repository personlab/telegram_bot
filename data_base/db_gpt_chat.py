import sqlite3
from create_bot import GOOGLE
from google.oauth2 import service_account
import gspread


class Database:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cur = self.db.cursor()

    def create_users_table(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS usersgpt 
        (user_id INTEGER PRIMARY KEY, available_requests INTEGER, subscription_date TEXT)
        """)

    def load_data_to_google_gpt(self):

        # Получить последнюю зарегистрированную запись
        self.cur.execute('SELECT * FROM usersgpt')
        all_user_pay_shop = self.cur.fetchall()

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file(
            'TestMir/my-project-bot-88845-fac16c8795e1.json',
            scopes=scope)
        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key(f'{GOOGLE}')
        worksheet = spreadsheet.get_worksheet(3)

        for user_pay_shop in all_user_pay_shop:
            data_values = [str(value) for value in user_pay_shop]
            item_name = data_values[0]
            subscription_date = data_values[2]

            # Поиск существующей записи с тем же товаром
            existing_cell = worksheet.find(item_name)
            if existing_cell:
                row_offset = existing_cell.row  # Получаем номер строки с существующей записью
                worksheet.update_cell(row_offset, 3, subscription_date)  # Обновляем значение subscription_date
            else:
                # Создаем новую запись
                worksheet.append_row(data_values)

        print('Данные успешно импортированы в таблицу Google.')
        self.db.commit()
        self.db.close()

    def add_new_user(self, user_id, available_requests=10, subscription_date='None'):
        self.cur.execute("INSERT INTO usersgpt (user_id, available_requests, subscription_date) VALUES (?, ?, ?)",
                        (user_id, available_requests, subscription_date,))
        self.db.commit()

    def get_user(self, user_id):
        user = self.cur.execute("SELECT * FROM usersgpt WHERE user_id = ?", (user_id,)).fetchone()
        return user

    def update_available_requests(self, user_id, available_requests):
        self.cur.execute("UPDATE usersgpt SET available_requests = ? WHERE user_id = ?", (available_requests, user_id,))
        self.db.commit()

    def update_subscription_date(self, user_id, subscription_date):
        self.cur.execute("UPDATE usersgpt SET subscription_date = ? WHERE user_id = ?", (subscription_date, user_id,))
        self.db.commit()

    def get_all_users(self):
        users = self.cur.execute("SELECT * FROM usersgpt").fetchall()
        return users
