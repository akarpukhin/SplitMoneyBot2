from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.chat import Chat
import os
from datetime import datetime
import sys
import time
import configs
import logging
from botdb import db_session, engine
from botdb import Base, User, Goal, Event, List
import fundraising 
import info 
import join 
import put 
import event

if not os.path.exists(configs.LOG_FILE):
    os.mkdir(os.path.dirname(configs.LOG_FILE))

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename=configs.LOG_FILE
                    )


def start(bot, update):

    logging.info('Пользователь {} {} нажал /start'.format(
        update.message.from_user.last_name, update.message.from_user.first_name)
    )

    bot.sendMessage(update.message.chat_id, text="Привет! \n Я - SplitMoneyBot! \n\n"
                                                 "Бот, который поможет вам следить"
                                                 "за тратами в поездках\r\n"
                                                 "или следить за вашими целями\r\n"
                                                 "<b>Основные команды:</b>\n"
                                                 "/fundraising\n"
                                                 "/join\n"
                                                 "/info\n"
                                                 "/put\n\n"
                                                 "<b>Events</b>\n"
                                                 "/events\n\n"
                                                 "<b>а так же:</b>\n"
                                                 "/help\n"
                                                 "/exit\n"
                                                 "/reset", parse_mode='HTML')
    return 'Menu'


def f_help(bot, update):
    pass


def stop(bot, update):
    kill_keyboard = ReplyKeyboardRemove()
    bot.sendMessage(
        update.message.chat_id,
        text="До встречи!\r\nМеня можно вызвать командой /start",
        reply_markup=kill_keyboard)
    return ConversationHandler.END


def restart(bot, update):
    bot.send_message(update.message.chat_id, "Bot is restarting...!")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)


main_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        'Menu': [CommandHandler('fundraising', fundraising.start_fund_raising, pass_chat_data=True),
                 CommandHandler('join', join.join),
                 CommandHandler('info', info.info, pass_args=True),
                 CommandHandler('put', put.put),
                 CommandHandler("event", event.event),
                 CommandHandler("help", f_help),
                 CommandHandler("exit", stop)],

        'Choice': [RegexHandler('^(Цель)$', join.choose_goal),
                   RegexHandler('^(Событие)$', join.event_join),
                   RegexHandler('^(Да)$', fundraising.start_fund_raising, pass_chat_data=True),
                   RegexHandler('^(Нет)$', stop)],

        'Join': [RegexHandler('^(Цель\:.*)$', join.join_goal)],

        'FundRaising': [MessageHandler(Filters.text, fundraising.get_name, pass_chat_data=True)],

        'FundRaising_Type': [MessageHandler(Filters.text, fundraising.get_type, pass_chat_data=True)]
    },

    fallbacks=[CommandHandler("exit", stop)]
)


def main():
    Base.metadata.create_all(bind=engine)

    updtr = Updater(configs.TELEGRAM_BOT_KEY)
    updtr.dispatcher.add_handler(main_conversation_handler)

    updtr.dispatcher.add_handler(CommandHandler("r", restart))
    updtr.start_polling()
    updtr.idle()


if __name__ == "__main__":
    logging.info('Bot started')
    main()
()
