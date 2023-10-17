import telebot
import random
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6654809823:AAEPXrVlYzIo9RhJ_9B_MahAIQtqoK_7748",
                      state_storage=state_storage, parse_mode='Markdown')

class PollState(StatesGroup):
    author = State()

class PollState1(StatesGroup):
    keyword = State()

text_poll = "Получить цитату дня"
text_button_1 = "Цитата по автору"
text_button_2 = "Цитата по ключевому слову"


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    ),
    telebot.types.KeyboardButton(
        text_button_1,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2
    )
)

quotes = [ # база цитат дня
    '"Успех - это не конечная станция, это путешествие." - Zig Ziglar',
    '"Счастье - это не что-то готовое. Оно приходит из ваших действий." - Dalai Lama',
    '"Сегодня - это подарок, поэтому он называется настоящим." - Bil Keane'
]

quotes1 = { # Цитата по автору
    "Альберт Эйнштейн": [
        "Воображение важнее знания.",
        "Жизнь как велосипед - чтобы сохранить равновесие, вы должны двигаться.",
        "Наука без религии хромает, религия без науки слепа."
    ],
    "Марк Твен": [
        "Лучший способ предсказать будущее - его изобретать.",
        "Самый успешный человек - тот, кто чувствует себя счастливым.",
        "Научитесь извлекать радость из мелочей, и жизнь будет радовать вас."
    ],
    "Оскар Уайльд": [
        "Все в мире есть воплощение идеи.",
        "Все должно быть в умеренности, даже умеренность.",
        "Лучший способ избежать соблазна - уступить ему."
    ]
}

quotes3 = {
    "Мотивация": [
        "Мотивация - это ключ к достижению ваших целей.",
        "Самое важное - это начать, мотивация придет после.",
        "Мотивация - это то, что вас начинает. Привычка - это то, что вас удерживает."
    ],
    "Счастье": [
        "Счастье - это не конечная станция, это путешествие.",
        "Счастье - это не что-то готовое. Оно приходит из ваших действий.",
        "Сегодня - это подарок, поэтому он называется настоящим."
    ],
    "Успех": [
        "Успех - это не конечная станция, это путешествие.",
        "Самый успешный человек - тот, кто чувствует себя счастливым.",
        "Успех - это способность двигаться от неудачи к неудаче, не потеряв энтузиазм."
    ]
}

@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Какую цитату хотите сегодня?',
        reply_markup=menu_keyboard)
#--------------------------------------------------------------------------------------------------
def get_random_quote():
    return random.choice(quotes)

@bot.message_handler(func=lambda message: message.text == "Получить цитату дня")
def send_random_quote(message):
    random_quote = get_random_quote()
    bot.send_message(message.chat.id, random_quote)
#----------------------------------------------------------------------------------------------------
def get_random_quote_by_author(author): ### Цитата по автору
    if author in quotes1:
        return random.choice(quotes1[author])
    else:
        return "Извините, цитаты этого автора отсутствуют."

@bot.message_handler(func=lambda message: message.text == "Цитата по автору")
def choose_author(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for author in quotes1.keys():
        markup.add(author)
    bot.send_message(message.chat.id, "Выберите автора:", reply_markup=markup)
    bot.set_state(message.from_user.id, PollState.author, message.chat.id)
@bot.message_handler(state=PollState.author)
def send_random_quote_by_author(message):
    author = message.text
    random_quote1 = get_random_quote_by_author(author)
    bot.send_message(message.chat.id, random_quote1)
    bot.delete_state(message.from_user.id, message.chat.id)

#----------------------------------------------------------------------------------------------------
def get_random_quote_by_keyword(keyword):
    if keyword in quotes3:
        return random.choice(quotes3[keyword])
    else:
        return "Извините, цитаты по этому ключевому слову отсутствуют."

@bot.message_handler(func=lambda message: message.text == "Цитата по ключевому слову")
def choose_keyword(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for keyword in quotes3.keys():
        markup.add(keyword)
    bot.send_message(message.chat.id, "Выберите ключевое слово:", reply_markup=markup)
    bot.set_state(message.from_user.id, PollState1.keyword, message.chat.id)

@bot.message_handler(state=PollState1.keyword)
def send_random_quote_by_keyword(message):
    keyword = message.text
    random_quote = get_random_quote_by_keyword(keyword)
    bot.send_message(message.chat.id, random_quote)
    bot.delete_state(message.from_user.id, message.chat.id)
#----------------------------------------------------------------------------

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()