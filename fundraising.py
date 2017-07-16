from telegram import ReplyKeyboardMarkup
from datetime import datetime, timedelta
import botdb

# типы сборов
goal_type = ['фис.итог', 'фикс. взнос', 'свободный']

# словарик с полями для цели
goal = {'user_list_id': None, 'event_id': None, 'goal_target': 0, 'goal_amount': 0,
        'goal_name': 'empty', 'goal_date': datetime.today() + timedelta(days=10),
        'goal_type': 0}


# точка входа в создание нового сбора средств
def start_fund_raising(bot, update, chat_data):
    bot.sendMessage(update.message.chat_id, text="Отлично! \nВы решили создать новый сбор!\n"
                    "Как мы его назовём?")
    return 'FundRaising'


# получаем имя сбора и переводим на запрос типа
def get_name(bot, update, chat_data):
    goal['name'] = update.message.text
    goal_type_keyboard = [goal_type]
    reply_markup = ReplyKeyboardMarkup(goal_type_keyboard)
    bot.sendMessage(update.message.chat_id,
                    text="Итак, имя цели - %(name)s\nТеперь выберите тип сбора: " % goal,
                    reply_markup=reply_markup)
    return 'FundRaising_Type'


def get_type(bot, update, chat_data):
    goal['goal_type'] = goal_type.index(update.message.text)
    bot.sendMessage(update.message.chat_id, text="Чундно! Тип сбора %s" % goal['goal_type'])
    goal_db = botdb.Goal(goal_name=goal['name'],
                         goal_type=goal['goal_type'],
                         chat_id=update.message.chat.id)
    botdb.db_session.add(goal_db)
    botdb.db_session.commit()
    return 'Menu'
