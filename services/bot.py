from modules.models import Message
from services.crud import CRUD
from time import time

db = CRUD()


class Bot:
    req_id = None

    def __init__(self, req_id):
        self.req_id = req_id

    @staticmethod
    def switch_to_human(messages, id=False):
        service_msg = Message(2, 'Переключаем на оператора...')
        operator_msg = Message(1, 'Вижу Ваш вопрос, скоро отвечу...', int(time() + 5), 'Виталий', '/operator.jpg')
        messages.extend([service_msg, operator_msg])

        if id:
            db.set_req_var(id, 'bot_step', -1)

    @staticmethod
    def check_bot(data, messages, strict=False, id=False):
        if data[0] in [23, 15] or (not strict and data[0] == -1):
            Bot.switch_to_human(messages, id)
            return False

        return True

    def send(self, text):
        message = Message(1, text, name='Бот', avatar='/bot.jpg')
        return db.push_messages(self.req_id, [message])
