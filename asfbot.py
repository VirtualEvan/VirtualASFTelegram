import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import requests
import config

updater = Updater(token=config.get_token())

dispatcher = updater.dispatcher


def build_menu(buttons, n_cols,):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu[0]


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is a starting message")


def owner_chat_id(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


# STM
def redeem(bot, update, args):
    params = (
        ('command', 'redeem 1-virtualevan ' + ' '.join(args)),
    )

    response = requests.get('http://127.0.0.1:1242/IPC', params=params)
    bot.send_message(chat_id=update.message.chat_id, text=response.text)


def test(bot, update, args=None):
    show_menu(bot, update, args)


def addlicense(bot, update, args):
    show_menu(bot, update, args)
    # params = (
    #     ('command', 'addlicense ASF ' + ' '.join(args)),
    # )
    #
    # response = requests.get('http://127.0.0.1:1242/IPC', params=params)
    # bot.send_message(chat_id=update.message.chat_id, text=response.text)


def show_menu(bot, update, args=None):
    button_list = [
        [InlineKeyboardButton("VirtualEvan", callback_data=update.message.text.partition(' ')[0][1:] + ' ' + '1-virtualevan' + ' ' + ' '.join(args)),
         InlineKeyboardButton("FidelKarthus", callback_data=update.message.text.partition(' ')[0][1:] + ' ' + '2-fidelkarthus' + ' ' + ' '.join(args))],
        [InlineKeyboardButton("Nikolai", callback_data=update.message.text.partition(' ')[0][1:] + ' ' + '3-nikolai' + ' ' + ' '.join(args)),
         InlineKeyboardButton("Ho Chi Minh", callback_data=update.message.text.partition(' ')[0][1:] + ' ' + '4-hochiminh' + ' ' + ' '.join(args))],
        [InlineKeyboardButton("All of them", callback_data=update.message.text.partition(' ')[0][1:] + ' ' + 'ASF' + ' ' + ' '.join(args))]
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
    bot.send_message(chat_id=update.message.chat_id, text="Which bot?", reply_markup=reply_markup)


def button(bot, update):
    bot.deleteMessage(chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id)

    response = requests.get('http://127.0.0.1:1242/IPC?command=' + update.callback_query.data)
    print(response.text)
    bot.send_message(chat_id=update.callback_query.message.chat_id, text=response.text)


def block(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Wrong user")


block_handler = MessageHandler(~ Filters.chat(156195413), block)
dispatcher.add_handler(block_handler)

# Query handler
query_handler = CallbackQueryHandler(button)
dispatcher.add_handler(query_handler)

# STM handlers
redeem_handler = CommandHandler('redeem', redeem, pass_args=True)
addlicense_handler = CommandHandler('addlicense', addlicense, pass_args=True)

# Bot handlers
start_handler = CommandHandler('start', start)
owner_handler = CommandHandler('ownerchat', owner_chat_id)
stop_handler = CommandHandler('stop', show_menu)

test_handler = CommandHandler('test', test, pass_args=True)
dispatcher.add_handler(test_handler)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(owner_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(redeem_handler)
dispatcher.add_handler(addlicense_handler)

updater.start_polling()

# TODO: FINALIZAR CORRECTAMENTE
