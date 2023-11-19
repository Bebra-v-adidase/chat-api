from modules.models import Message
from services.crud import CRUD

db = CRUD()


class Bot:
    @staticmethod
    def check_bot(data, messages, strict=False, id=False):
        if data[0] == 23 or (not strict and data[0] == -1):
            messages.append(Message(2, 'Переключаем на оператора...'))
            if id:
                db.set_req_var(id, 'use_bot', False)

            return False

        return True
