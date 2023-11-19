import json
from modules.db import get_connection
from modules.models import MessageEncoder, Message


class CRUD:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def create_request(self, category: int, priority: int, messages: list, employee_id: int):
        messages = json.dumps(messages, cls=MessageEncoder)
        self.cursor.execute('''
            INSERT INTO requests (category, priority, messages, employee_id)
            VALUES (?, ?, ?, ?)
        ''', (category, priority, messages, employee_id))

        request_id = self.cursor.lastrowid
        self.conn.commit()

        return request_id

    def push_message(self, request_id: int, msg: Message):
        messages = self.get_history(request_id)
        messages.append(msg)
        m_encoded = json.dumps(messages, cls=MessageEncoder)

        self.cursor.execute('''
            UPDATE requests SET messages = ? WHERE id = ?
        ''', (m_encoded, request_id))
        self.conn.commit()

        return len(messages) - 1

    def get_history(self, request_id: int):
        self.cursor.execute('SELECT messages FROM requests WHERE id = ?', (request_id,))
        result = self.cursor.fetchone()

        if not result:
            raise 'no such request'

        return json.loads(result[0]) or []
