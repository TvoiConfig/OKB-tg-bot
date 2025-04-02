from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext


questions = [
    {"question": "Сколько лет Даниилу?", "options": ["5", "20", "18", "25"], "answer": "20"},
    {"question":  "В каком городе проходит ОКБ?", "options": ["Батайск", "Воронеж", "Ростов-на-Дону", "Борисоглебск"], "answer": "Ростов-на-Дону"},
]

# Функция старта бота
def start(update: Update, context: CallbackContext) -> None:
    # Инициализация счетчиков для бота
    context.user_data['score'] = 0
    context.user_data['question-index'] = 0