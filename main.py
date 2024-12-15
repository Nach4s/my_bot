import telebot
from config import BOT_TOKEN
from telebot import types
import sqlite3
import logging
from telebot.types import WebAppInfo


bot = telebot.TeleBot(BOT_TOKEN)
name = ''
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('nachos_bot.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Выбор категории курсов', callback_data='choice')
    bt2 = types.InlineKeyboardButton('Помощь', callback_data='help_section')
    bt3 = types.InlineKeyboardButton('Регистрация', callback_data='registration')
    bt4 = types.InlineKeyboardButton('Перейти на веб-страницу', web_app=WebAppInfo(url='https://music.apple.com/library/playlist/p.YJXV7dEIerGlxQ5'))
    markup.row(bt1, bt2)
    markup.row(bt3, bt4)
    bot.send_message(
        message.chat.id,
        f"👋 Привет {message.from_user.first_name}! 👋 Привет! Я ваш образовательный бот, готовый помочь вам учиться и развиваться.\n"
            "🎓 У нас есть курс по программированию на Python. Давайте начнем изучение!\n"
            "👉 Чтобы начать, просто нажмите на кнопку ниже и выберите курс по Python!\n",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def greetings(message):
    if message.text.lower() == 'привет':
        bot.reply_to(message, f'Привет!\n'
                              f'Нажмите /start для взаимодействие с ботом')


@bot.message_handler(commands=['registration'])
def registration(message):
    if user_exists(message.chat.id):
        bot.send_message(
            message.chat.id,
            "<u>🚫 Вы уже зарегистрированы!</u>\n\n",
            parse_mode='html')

        return
    else:
        bot.send_message(
            message.chat.id,
            "<u>👋 Привет! Рад тебя видеть!</u>\n\n"
            "Давай я помогу тебе зарегистрироваться, чтобы ты мог начать изучение курса по программированию на Python.\n\n"
            "Пожалуйста, введи свое имя, и мы продолжим!",
            parse_mode='html')
        bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(
        message.chat.id,
        f"<u>🔒 Отлично, {name}!</u> Теперь давай создадим пароль для твоей учетной записи.\n\n"
        "Пожалуйста, введи свой пароль (не менее 6 символов):",
        parse_mode='html')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    if len(str(message.text)) >= 6:
        password = str(message.text)
    else:
        bot.send_message(message.chat.id, "Пароль должен быть не менее 6 символов!")
        bot.register_next_step_handler(message, user_pass)
        return 

    conn = sqlite3.connect('nachos_bot.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name,pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(
        message.chat.id,
        f"<u>🎉 Поздравляю, {name}!</u> Вы успешно зарегистрированы!",
        parse_mode='html', reply_markup=markup)


def user_exists(chat_id):
    try:
        with sqlite3.connect('nachos_bot.sql') as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM users WHERE id = ?", (chat_id,))
            return cur.fetchone() is not None
    except sqlite3.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")
        return False


@bot.message_handler()
def help_section(message):
    bot.send_message(
        message.chat.id,
        "<u>📖 Помощь</u>\n\n"
        "Добро пожаловать в раздел помощи! Здесь вы найдете информацию о том, как использовать нашего образовательного бота и получать максимальную пользу от курса по программированию на Python.\n\n"
        "<b>Основные команды:</b>\n"
        "/start: Начните взаимодействие с ботом и получите доступ к курсу по Python.\n"
        "/course: Просмотрите информацию о курсе \"Основы программирования на Python\".\n"
        "/my_progress: Узнайте о вашем прогрессе в курсе.\n"
        "/feedback: Оставьте отзыв о курсе или уроке.\n"
        "/settings: Настройте свои предпочтения и уведомления.\n\n"
        "<b>Как начать обучение:</b>\n"
        "Нажмите на команду /start.\n"
        "Выберите курс \"Основы программирования на Python\".\n"
        "Нажмите на название урока, чтобы начать обучение.\n\n"
        "<b>Как пройти тест:</b>\n"
        "После завершения каждого урока вам будет предложено пройти тест для проверки знаний. Просто выберите правильный ответ из предложенных вариантов.",
        parse_mode='html')



@bot.message_handler()
def choice(message):
    bot.send_message(
        message.chat.id,
        "📚 У нас доступен только один курс:\n\n"
        "1️⃣ <u>Основы программирования на Python</u>\n\n"
        "🔍 Нажмите на название курса, чтобы начать обучение!",
        parse_mode='html')


@bot.message_handler(content_types=['photo'])
def react(message):
    bot.reply_to(
        message,
        "📸 Спасибо за фото!\n"
        "Теперь давайте вернемся к обучению!"
    )


@bot.message_handler()
def recommendation(message):
    bot.send_message(
        message.chat.id,
        "📚 <u>Выберите категорию курса:</u>\n\n"
        "1️⃣ <u>Программирование</u>\n",
        parse_mode='html')

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == 'users':
        conn = sqlite3.connect('nachos_bot.sql')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        info = ''
        for i in users:
            info += f'Имя: {i[1]}, пароль: {i[2]}\n'

        cur.close()
        conn.close()
        bot.send_message(callback.message.chat.id, info)

    elif callback.data == 'choice':
        choice(callback.message)

    elif callback.data == 'help_section':
        help_section(callback.message)

    elif callback.data == 'registration':
        registration(callback.message)



bot.polling(none_stop=True)