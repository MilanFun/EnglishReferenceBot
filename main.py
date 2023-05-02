import os
import telebot
from telebot import types
from googletrans import Translator
import json

BOT_TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
new_words = {}
tense_rules = ["Present Simple",
               "Present Continuous",
               "Present Perfect",
               "Present Perfect Continuous",
               "Past Simple",
               "Past Continuous",
               "Past Perfect",
               "Past Perfect Continuous",
               "Future Simple",
               "Future Continuous",
               "Future Perfect",
               "Future Perfect Continuous"]


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Translate")
    btn2 = types.KeyboardButton("English Tense Rules")
    btn3 = types.KeyboardButton("Save new word")
    btn4 = types.KeyboardButton("Get list of words")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text="Hello, {0.first_name}! I am a telegram bot that can quickly translate and show cheat "
                          "sheets about English Tense Rules".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Translate":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Back to main")
        markup.add(back)
        bot.send_message(message.chat.id, text="Enter word or sentence", reply_markup=markup)
        bot.register_next_step_handler(message, process_translate_step)
    elif message.text == "English Tense Rules":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Present Simple")
        btn2 = types.KeyboardButton("Present Continuous")
        btn3 = types.KeyboardButton("Present Perfect")
        btn4 = types.KeyboardButton("Past Simple")
        btn5 = types.KeyboardButton("Past Continuous")
        btn6 = types.KeyboardButton("Past Perfect")
        btn7 = types.KeyboardButton("Future Simple")
        btn8 = types.KeyboardButton("Present Simple")
        btn9 = types.KeyboardButton("Future Continuous")
        btn10 = types.KeyboardButton("Future Perfect")
        btn11 = types.KeyboardButton("Present Perfect Continuous")
        btn12 = types.KeyboardButton("Past Perfect Continuous")
        btn13 = types.KeyboardButton("Future Perfect Continuous")
        back = types.KeyboardButton("Back to main")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, back)
        bot.send_message(message.chat.id, text="Choose", reply_markup=markup)
    elif message.text == "Save new word":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Back to main")
        markup.add(back)
        bot.send_message(message.chat.id, text="Enter word and translation: use next format -> word=translation",
                         reply_markup=markup)
        bot.register_next_step_handler(message, process_saving_new_word)
    elif message.text == "Get list of words":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        s = ""
        for k in new_words:
            tmp = k + " = " + new_words[k] + "\n"
            s += tmp
        if len(new_words.keys()) == 0:
            bot.send_message(message.chat.id, text="Empty list" + "\nBack to main", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text=s + "\nBack to main", reply_markup=markup)
    elif message.text == "Back to main":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Translate")
        btn2 = types.KeyboardButton("English Tense Rules")
        btn3 = types.KeyboardButton("Save new word")
        btn4 = types.KeyboardButton("Get list of words")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text="Back to main", reply_markup=markup)
    else:
        if message.text in tense_rules:
            with open("grammar.json", "r") as f:
                file = json.load(f)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Translate")
            btn2 = types.KeyboardButton("English Tense Rules")
            btn3 = types.KeyboardButton("Save new word")
            btn4 = types.KeyboardButton("Get list of words")
            markup.add(btn1, btn2, btn3, btn4)
            string = "Конструкция:\t" + file[message.text][message.text] + "\n" + \
                  "Описание:\t" + file[message.text]["Description"] + "\n" + \
                  "Пример:\t" + file[message.text]["Example"]
            bot.send_message(message.chat.id, text=string + "\n\nBack to main", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text="I'm not programmed for this command...")


def process_translate_step(message):
    try:
        if message.text == 'Back to main':
            func(message)
        else:
            translator = Translator()
            result = translator.translate(message.text, dest='ru')
            bot.reply_to(message, result.text)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Translate")
            btn2 = types.KeyboardButton("English Tense Rules")
            btn3 = types.KeyboardButton("Save new word")
            btn4 = types.KeyboardButton("Get list of words")
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, text="Back to main", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_saving_new_word(message):
    try:
        if message.text == 'Back to main':
            func(message)
        else:
            arr = message.text.split("=")
            new_words[arr[0]] = arr[1]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Translate")
            btn2 = types.KeyboardButton("English Tense Rules")
            btn3 = types.KeyboardButton("Save new word")
            btn4 = types.KeyboardButton("Get list of words")
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, text="Back to main", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, 'oooops')


if __name__ == '__main__':
    bot.infinity_polling()