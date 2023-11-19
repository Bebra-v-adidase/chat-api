from modules.models import Message
from services.crud import CRUD
from time import time
import json

db = CRUD()
answers = json.load(open('data/bot_answers.json'))


class Bot:
    req_id = None

    def __init__(self, req_id):
        self.req_id = req_id

    @staticmethod
    def switch_to_human(messages, id=False, op_msg=None):
        service_msg = Message(2, 'Переключаем на оператора...')
        operator_msg = Message(1, op_msg or 'Вижу Ваш вопрос, скоро отвечу...', int(time() + 5), 'Виталий', '/operator.jpg')
        messages.extend([service_msg, operator_msg])

        if id:
            db.set_req_var(id, 'bot_step', -1)

    @staticmethod
    def check_bot(data, messages, strict=False, id=False):
        if data[0] == 23 or (not strict and data[0] in [15, -1]):
            Bot.switch_to_human(messages, id)
            return False

        return True

    def send(self, text, buttons=None):
        buttons = buttons or ['Позови оператора']
        message = Message(1, text, name='Бот', avatar='/bot.jpg', buttons=buttons)
        return db.push_messages(self.req_id, [message])

    def handle(self, text, cat: int = -1, step: int = 0):
        print(cat, step)
        a = answers.get(str(cat))
        if a and step <= len(a):
            a = a[step]
        else:
            a = ['switch', 'Упс! Пока что я не помочь с этим вопросом']

        print(a)
        if a[0] == 'send':
            self.send(a[1], a[2] if len(a) > 2 else None)
            db.set_req_var(self.req_id, 'bot_step', step + 1)
        elif a[0] == 'switch':
            messages = []
            Bot.switch_to_human(messages, self.req_id, a[1])
            db.push_messages(self.req_id, messages)
