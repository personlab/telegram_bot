import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from create_bot import PASSWORD_YANDEX_ENV
from data_base import sqlite_db


async def send_email_yandex_success_pay(receiver_email, item_name, item_data_fore, item_total, purchase_date, discount):
    # Информация об отправителе и получателе
    sender_email = "personlabvip@yandex.ru"
    password = PASSWORD_YANDEX_ENV
    smtp_server = "smtp.yandex.com"
    port = 587
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        # Отправить подтверждение пользователю
        subject = 'Подтверждение покупки'
        body = (f'<h2 style="color:#2000a0"><center>Спасибо за покупку!</center></h2><br><br>'
                f'<h2 style="color:red"><b><center>Вы приобрели {item_name}</center></h2>'
                f'<b><center>Дата покупки: {purchase_date}</center></b>'
                f'<br><h3><center>Стоимость: {item_data_fore} руб.</center></h3>'
                f'<b><center>Ваша скидка: {discount}%</center></b>'
                f'<br><h3><center>Количество: {item_total}</center></b></h3>'
                f'<br><br>Пожалуйста, не отвечайте на это сообщение.<br><br>'
                f'**********<br><br>Это письмо отправлено почтовым сервером mail.yandex.net')

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        html = f"""\
                        <html>
                          <body>
                            <p>{body}</p>
                          </body>
                        </html>
                        """

        part = MIMEText(html, "html")
        message.attach(part)

        server.sendmail(sender_email, receiver_email, message.as_string())


def get_user_email(user_id):
    sqlite_db.cursor_user_register.execute("SELECT email_address FROM users WHERE user_id = ?", (user_id,))
    result = sqlite_db.cursor_user_register.fetchone()
    if result:
        return result[0]
    else:
        return ""

