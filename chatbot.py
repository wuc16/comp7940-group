# lab4 chatbot
# import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# import configparser
import os
import logging
import redis
global redis1


def main():
	
	# Load your token and create an Updater for your Bot

	config = configparser.ConfigParser()
	config.read('config.ini')

	updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
	# updater = Updater(token=(os.environ['ACCESS_TOKEN_W']), use_context=True)
	
	dispatcher = updater.dispatcher
	# global redis1
	# redis1 = redis.Redis(host=(os.environ['HOST']), password=(os.environ['PASSWORD']), port=(os.environ['REDISPORT']))
	# openai.api_key = os.environ['OPENAI_API']
	
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
	# register a dispatcher to handle message: here we register an echo dispatcher
	echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
	updater.dispatcher.add_handler(echo_handler)
	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("add", add))
	dispatcher.add_handler(CommandHandler("help", help_command))
	dispatcher.add_handler(CommandHandler("hello", hello))
	dispatcher.add_handler(CommandHandler("chat", chat))
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
	update.message.reply_text('"/add"\tadd a string to count\n"/hello"\tgreeting message\n"/chat"\tChatGPT')


def add(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /add is issued."""
	try:
		global redis1
		logging.info(context.args[0])
		msg = context.args[0]  # /add keyword <-- this should store the keyword
		redis1.incr(msg)
		update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
	except (IndexError, ValueError):
		update.message.reply_text('Usage: /add <keyword>')


def hello(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /hello is issued."""
	try:
		global redis1
		logging.info(context.args[0])
		msg = context.args[0]  # /hello keyword <-- this should store the keyword
		update.message.reply_text('Good Day, ' + msg + "!")
	except (IndexError, ValueError):
		update.message.reply_text('Usage: /hello <keyword>')


def chat(update: Update, context: CallbackContext) -> None:
	try:
		msg = ""
		for str in context.args:
			msg = msg + str + " "
		update.message.reply_text(generate_text(msg))
	except (IndexError, ValueError):
		update.message.reply_text('Usage: /chat <sentence>')  	

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
