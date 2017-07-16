from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta


engine = create_engine('sqlite:///botdb.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    user_list_id = Column(Integer)
    is_user_active = Column(Boolean, default=True)

    def __repr__(self):
        return '<Event: {} {}}>'.format(self.id, self.is_user_active)


# таблица с описанием цели:
# user_list_id - ссылка на список пользователей, участвующих в достижении цели
# event_id - ссылка на событие, для которого создали цель - может быть пустой
# goal_target - номинальная сумма, которую хотят собрать для достижения цели
# goal_amount - текущая сумма, которую набрали
# goal_date - дата, к которой хотят выполнить цель

# N.B. taret и amount надо сделать decimal, но это будет позднее!!!

class Goal(Base):
    __tablename__ = 'goal'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    goal_target = Column(Integer)
    goal_amount = Column(Integer)
    goal_name = Column(String(50))
    goal_date = Column(DateTime)
    goal_type = Column(Integer)
    chat_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    users = relationship('User', secondary='list')

    def __init__(self, event_id=None, goal_target=0, goal_amount=0,
                 goal_name='empty', goal_date=datetime.today() + timedelta(days=10),
                 goal_type=0, chat_id=None, is_active=True):
        self.goal_name = goal_name
        self.goal_date = goal_date
        self.goal_target = goal_target
        self.goal_type = goal_type
        self.chat_id = chat_id
        self.is_active = is_active

    def __repr__(self):
        return '<{}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(
            self.id, self.event_id, self.goal_target, self.goal_amount,
            self.goal_name, self.goal_date, self.goal_type, self.chat_id, self.is_active)


class List(Base):
    __tablename__ = 'list'
    id = Column(Integer, primary_key=True)
    goal_id = Column(Integer, ForeignKey('goal.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, goal_id=None, user_id=None):
        self.goal_id = goal_id
        self.user_id = user_id

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.id, self.goal_id, self.user_id)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50))
    telegram_id = Column(Integer)
    goals = relationship('Goal', secondary='list')

    def __init__(self, telegram_id=None, user_name=None):
        self.telegram_id = telegram_id
        self.user_name = user_name

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.id, self.user_name, self.telegram_id)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("База данных успешно создана")
