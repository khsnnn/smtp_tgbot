import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
import os

# Загружаем данные из .env файла
load_dotenv()

# Чтение конфиденциальных данных из .env
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

# Данные для SMTP
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')

# Функция для отправки email
def send_email(to_email, message):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = to_email
            msg['Subject'] = "telegram SMPT app"
            msg.attach(MIMEText(message, 'plain'))
            server.send_message(msg)
        logging.info(f"Email sent to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return False


# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сброс состояния
    context.user_data.clear()
    await update.message.reply_text("Привет! Введите свой email:")

# Функция для обработки email
async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'email' not in context.user_data:
        user_email = update.message.text
        try:
            # Проверка на корректность email
            validate_email(user_email)
            context.user_data['email'] = user_email  # Сохраняем email
            await update.message.reply_text("Email корректен! Теперь введите текст сообщения.")
        except EmailNotValidError as e:
            await update.message.reply_text(f"Неверный email: {e}")
    else:
        # Если email уже указан, это значит, что пользователь вводит сообщение
        await handle_message(update, context)

# Функция для обработки текста сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'email' in context.user_data and 'message_sent' not in context.user_data:
        message_text = update.message.text
        user_email = context.user_data['email']

        if send_email(user_email, message_text):
            await update.message.reply_text(f"Сообщение успешно отправлено на {user_email}.")
            context.user_data['message_sent'] = True  # Помечаем, что сообщение отправлено
        else:
            await update.message.reply_text("Ошибка при отправке сообщения. Попробуйте снова.")
    else:
        await update.message.reply_text("Сначала введите свой email!")

# Главная функция для запуска бота
def main():
    # Создаём приложение
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler('start', start))

    # Обработчик сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))

    # Запуск бота
    app.run_polling()

if __name__ == '__main__':
    main()
