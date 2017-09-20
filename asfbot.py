from telegram.ext import Updater, CommandHandler
import config

updater = Updater(token=config.get_token())

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is a starting message")


def ownerchat(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
