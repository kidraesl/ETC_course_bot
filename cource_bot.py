import requests
import telebot
from telebot import types

bot = telebot.TeleBot(open('key').read())


def get_course():
    url_etc = 'https://rest.coinapi.io/v1/exchangerate/ETC/RUB'
    url_btc = 'https://rest.coinapi.io/v1/exchangerate/BTC/RUB'
    key = open('cfg').read()
    headers = {'X-CoinAPI-Key' : key}

    response_etc = requests.get(url_etc, headers=headers)
    response_btc = requests.get(url_btc, headers=headers)
    result_etc = response_etc.json()
    result_btc = response_btc.json()

    cours_etc = round(result_etc['rate'], 2)
    cours_btc = round(result_btc['rate'], 2)
    return cours_etc, cours_btc


etc_cource = 0
btc_cource = 0
etc_value = 0


markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton(text='Узнать курс')
btn2 = types.KeyboardButton(text='Что ещё можно сделать?')
markup1.add(btn1, btn2)

markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn3 = types.KeyboardButton(text='Посчитать сколько у меня рублей')
btn4 = types.KeyboardButton(text='В начало')
markup2.add(btn3, btn4)

markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn5 = types.KeyboardButton(text='В начало')
markup3.add(btn5)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text='Привет! Я помогу тебе оперативно узнать курс криптовалюты на текущий '
                                           'момент. За сутки можно сделать всего 50 запросов, так что нажимай '
                                           'на кнопки вдумчиво', reply_markup=markup1)


@bot.message_handler(content_types=['text'])
def text(message):
    global etc_cource, etc_value
    if message.text == 'Узнать курс':
        global etc_cource, btc_cource
        etc_cource, btc_cource = get_course()

        bot.send_message(message.chat.id, text=f'Текущий курс ETC в рублях на сегодня {etc_cource} '
                                               f'Текущий курс BTC сегодня {btc_cource}', reply_markup=markup2)

    elif message.text == 'Посчитать сколько у меня рублей':
        if etc_value == 0:
            bot.send_message(message.chat.id, text='для начала напиши, сколько у тебя эфира', reply_markup=None)
        else:
            rub = etc_value * etc_cource
            bot.send_message(message.chat.id, text=f'твои накопления на сегодня = {rub}', reply_markup=markup3)

    elif message.text == 'В начало':
        bot.send_message(message.chat.id, text='Я всё ещё могу помочь вот с чем:', reply_markup=markup1)

    elif message.text == 'Что ещё можно сделать?':
        bot.send_message(message.chat.id, text='Новые функции находятся в разработке! На данный момент '
                                               'вот что ещё можно сделать: ', reply_markup=markup2)
    elif int(message.text):
        rub = int(message.text) * etc_cource
        etc_value = int(message.text)
        bot.send_message(message.chat.id, text=f'твои накопления на сегодня = {rub}', reply_markup=markup3)


bot.polling()