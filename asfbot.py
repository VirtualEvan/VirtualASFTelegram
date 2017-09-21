from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config

updater = Updater(token=config.get_token())

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is a starting message")


def owner_chat_id(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


def stop(bot, update):
    pass


def block(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Wrong user")


block_handler = MessageHandler(not Filters.chat(156195413), block)
dispatcher.add_handler(block_handler)

start_handler = CommandHandler('start', start)
owner_handler = CommandHandler('ownerchat', owner_chat_id)
stop_handler = CommandHandler('stop', stop)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(owner_handler)
dispatcher.add_handler(stop_handler)

updater.start_polling()
