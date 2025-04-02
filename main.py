from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Список вопросов: каждый вопрос — это словарь с текстом, вариантами и правильным ответом
questions = [
    {"question": "Донинтех лучше всех?", "options": ["Да!", "Нет!", "Возможно..."], "answer": "Да!"},
    {"question": "Какой цвет у неба?", "options": ["Красный", "Синий", "Зеленый", "Желтый"], "answer": "Синий"},
    {"question": "2 + 2 = ?", "options": ["3", "4", "5", "6"], "answer": "4"},
    # Добавь еще вопросы (до 10) в таком же формате
]

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Инициализируем счетчик правильных ответов и индекс текущего вопроса
    context.user_data['score'] = 0
    context.user_data['question_index'] = 0
    # Отправляем первый вопрос
    await send_question(update, context)

# Функция для отправки вопроса
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Берем текущий вопрос из списка
    question_data = questions[context.user_data['question_index']]
    # Создаем кнопки с вариантами ответа
    keyboard = [
        [InlineKeyboardButton(option, callback_data=option) for option in question_data['options']]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем вопрос с кнопками
    if update.message:  # Если это сообщение (например, /start)
        await update.message.reply_text(f"Привет! Давай начнем викторину.\n{question_data['question']}", reply_markup=reply_markup)
    else:  # Если это callback от кнопки
        await update.callback_query.message.reply_text(question_data['question'], reply_markup=reply_markup)

# Функция обработки ответа пользователя
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждаем, что получили ответ
    # Берем текущий вопрос
    question_data = questions[context.user_data['question_index']]
    # Проверяем, правильный ли ответ
    if query.data == question_data['answer']:
        context.user_data['score'] += 1
        await query.edit_message_text(text=f"Правильно! {question_data['question']} — {question_data['answer']}")
    else:
        await query.edit_message_text(text=f"Неправильно. Правильный ответ: {question_data['answer']}")
    
    # Переходим к следующему вопросу
    context.user_data['question_index'] += 1
    if context.user_data['question_index'] < len(questions):
        await send_question(update, context)
    else:
        # Викторина завершена, отправляем прощальное сообщение
        await query.message.reply_text(
            f"Викторина завершена! Твой результат: {context.user_data['score']} из {len(questions)}. Спасибо за участие!"
        )

# Основная функция для запуска бота
def main() -> None:
    # Создаем приложение с помощью ApplicationBuilder
    application = Application.builder().token("TOKEN").build()
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()