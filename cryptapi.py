import telebot  # ask - BotName
from requests import Response
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from settings import settings  # на сколько я помню, из этого файла я доставал апи токен к боту
import requests


bot = telebot.TeleBot(settings['token'])


# bot.send_message(message.chat.id, get_ticker(coin1=message.text))
# попытаюсь еще сделать так, чтобы бот мог выводить и без кнопок валюту


def get_ticker(coin1="btc", coin2="usd"):
    response = requests.get(url=f"https://yobit.net/api/3/ticker/{coin1}_{coin2}?ignore_invalid=1").json()
    buy = response[f'{coin1}_usd']['buy']
    sell = response[f'{coin1}_usd']['sell']

    with open("ticker.txt", "w") as file:
        file.write(f'{buy=}\n')
        file.write(f'{sell=}')

    text1 = f'💎{coin1.upper()}💎\n'
    text1 += f'💰 Цена на покупке: {round(buy, 2)}💲\n'
    text1 += f'💰 Цена на продаже: {round(sell, 2)}💲'

    return text1


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Начать!')
    markup.add(btn1)
    text = 'Вы только что присоединились к telegram боту, который выводит актуальную цену купли/продажи криптовалюты'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Начать')
def send_massage(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = KeyboardButton('₿ BTC ₿')
    btn2 = KeyboardButton('♢ ETH ♢')
    btn3 = KeyboardButton('🐶 DOGE 🐶')
    btn11 = KeyboardButton('👨‍💻 Об авторе')
    markup.add(btn1, btn2, btn3)
    markup.add(btn11)
    bot.send_message(message.chat.id, 'Выберите курс криптовалюты для вывода', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == '₿ BTC ₿':
        bot.send_message(message.chat.id, get_ticker(coin1='btc'))
    elif message.text == '♢ ETH ♢':
        bot.send_message(message.chat.id, get_ticker(coin1='eth'))
    elif message.text == '🐶 DOGE 🐶':
        bot.send_message(message.chat.id, get_ticker(coin1='doge'))
    elif message.text == '👨‍💻 Об авторе':
        text_author = '✅ Автор проекта:\n'
        text_author += '💻 Диментий Денивер\n'
        text_author += '✉️ TG: @nar1on'
        bot.send_message(message.chat.id, text_author)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = KeyboardButton('₿ BTC ₿')
        btn2 = KeyboardButton('♢ ETH ♢')
        btn3 = KeyboardButton('🐶 DOGE 🐶')
        btn11 = KeyboardButton('👨‍💻 Об авторе')
        markup.add(btn1, btn2, btn3)
        markup.add(btn11)
        text = 'Я еще не знаю такие валюты, лучше выбери из тех, которые я предлагаю!'
        bot.send_message(message.chat.id, text, reply_markup=markup)


bot.infinity_polling()