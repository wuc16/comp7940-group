# final project chatbot
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# import configparser
import os
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random


def main():
    # Load your token and create an Updater for your Bot

    # config = configparser.ConfigParser()
    # config.read('config.ini')

    # link to telegram chatbot
    # updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    updater = Updater(token=(os.environ['ACCESS_TOKEN']))

    # link to chatGPT
    # openai.api_key = config['OPENAI']['API']
    openai.api_key = os.environ['OPENAI_API']

    # link to firebase
    cred = credentials.Certificate("./serviceAccount.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.environ['FIREBASE']
    })

    dispatcher = updater.dispatcher
    # global redis1
    # redis1 = redis.Redis(host=(os.environ['HOST']), password=(os.environ['PASSWORD']), port=(os.environ['REDISPORT']))
    # updater = Updater(token=(os.environ['ACCESS_TOKEN_W']), use_context=True)
    # openai.api_key = os.environ['OPENAI_API']

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    updater.dispatcher.add_handler(echo_handler)
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("chat", chat))
    dispatcher.add_handler(CommandHandler("rec", rec))
    dispatcher.add_handler(CommandHandler("cook", cook))
    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context.args))
    # context.bot.send_message(chat_id=update.effective_chat.id, text=generate_text(reply_message))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('"/hello"\tgreeting message''\n"/chat"\tChatGPT\n'
                              '"/rec"\tintroducing cities\n"/cook"\trandom cooking videos')


def hello(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    try:
        logging.info(context.args[0])
        msg = context.args[0]  # /hello keyword <-- this should store the keyword
        update.message.reply_text('Good Day, ' + msg + "!")
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <keyword>')


def chat(update: Update, context: CallbackContext) -> None:
    try:
        test = context.args[0]
        msg = ""
        for str in context.args:
            msg = msg + str + " "
        update.message.reply_text(generate_text(msg))
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /chat <sentence>')


def rec(update: Update, context: CallbackContext) -> None:
    try:
        test = context.args[0]
        msg = ""
        for str in context.args:
            msg = msg + str + " "
        ref = db.reference('cities/' + msg[0:-1])
        data = ref.get()
        if data:
            update.message.reply_text(data['description'] + " You can find more information in the following link. ")
            update.message.reply_text(data['url'])
        else:
            update.message.reply_text('The city is not in the database, try /chat for the details of this city.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /rec <city>')


def cook(update: Update, context: CallbackContext) -> None:
    try:
        ref = db.reference('video/')
        data = ref.get()
        update.message.reply_text('https://www.youtube.com/watch?v=' + data[random.randint(0, 2)])
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /cook')


def generate_text(prompt):
    logging.info(prompt + "in generate_text")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    return message


if __name__ == '__main__':
    main()
