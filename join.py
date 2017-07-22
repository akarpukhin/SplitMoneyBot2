from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from botdb import Goal, User, List
from sqlalchemy import not_
import botdb


def join(bot, update):
    user_name = '{last_name} {first_name}'.format(
                last_name=update.message.from_user.last_name,
                first_name=update.message.from_user.first_name)
    telegram_id = update.message.from_user.id
    user = User.query.filter(User.telegram_id == telegram_id).first()

    if not user:
        user = botdb.User(telegram_id=telegram_id, user_name=user_name)
        botdb.db_session.add(user)
        botdb.db_session.commit()

    keyboard = [['Событие'], ['Цель']]
    choice_keyboard = ReplyKeyboardMarkup(keyboard)
    bot.send_message(
        update.message.chat_id,
        text="Куда вы хотите присоедениться ?",
        reply_markup=choice_keyboard)
    return "Choice"


def choose_goal(bot, update):

    telegram_id = update.message.from_user.id

    subquery = Goal.query.with_entities(Goal.id)\
                         .join(List, List.goal_id == Goal.id)\
                         .join(User, List.user_id == User.id)\
                         .filter(User.telegram_id == telegram_id,
                                 Goal.chat_id == update.message.chat_id)

    goals = Goal.query.filter(
        not_(Goal.id.in_(subquery)),
        User.telegram_id == telegram_id,
        Goal.chat_id == update.message.chat_id
    ).all()

    goal_list = [['Цель: {}'.format(g.goal_name)]
                 for g in goals]

    if not goal_list:
        keyboard = [['Да'], ['Нет']]
        choice_keyboard = ReplyKeyboardMarkup(keyboard)
        text = "Сейчас нет активных целей. Создать ?"
        state = "Choice"

    if len(goal_list) > 1:
        keyboard = goal_list
        choice_keyboard = ReplyKeyboardMarkup(keyboard)
        text = "Выбери цель:"
        state = "Join"

    if len(goal_list) == 1:
        keyboard = goal_list
        choice_keyboard = ReplyKeyboardMarkup(keyboard)
        text = "Вы хотите присоедениться к этой цели ?"
        state = "Join"

    bot.send_message(
        update.message.chat_id,
        text=text,
        reply_markup=choice_keyboard
    )
    return state


def join_goal(bot, update):
    import bot as bot_module
    goal_name = update.message.text
    goal_name = goal_name.split(': ')[1]
    goal = Goal.query.filter_by(is_active=True,
                                goal_name=goal_name,
                                chat_id=update.message.chat.id).first()

    telegram_id = update.message.from_user.id
    user = User.query.filter(User.telegram_id == telegram_id).first()

    goal.users.append(user)
    botdb.db_session.commit()

    return bot_module.start(bot, update)


def event_join(bot, update):
    choice = update.message.text
    remove_choice_keyboard = ReplyKeyboardRemove()
    bot.send_message(
        update.message.chat_id,
        text="Ты выбрал {choice}!".format(choice=choice),
        reply_markup=remove_choice_keyboard
    )
    return "Menu"
