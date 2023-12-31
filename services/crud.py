import json
from typing import List

from modules.db import get_connection
from modules.models import MessageEncoder, Message


class CRUD:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def create_request(self, category: int, priority: int, messages: list, employee_id: int, bot_step: int):
        messages = json.dumps(messages, cls=MessageEncoder)
        self.cursor.execute('''
            INSERT INTO requests (category, priority, messages, employee_id, bot_step)
            VALUES (?, ?, ?, ?, ?)
        ''', (category, priority, messages, employee_id, bot_step,))

        request_id = self.cursor.lastrowid
        self.conn.commit()

        return request_id

    def push_messages(self, request_id: int, new_m: List[Message]):
        messages = self.get_history(request_id)
        first_id = len(messages)

        messages += new_m
        m_encoded = json.dumps(messages, cls=MessageEncoder)

        self.cursor.execute('''
            UPDATE requests SET messages = ? WHERE id = ?
        ''', (m_encoded, request_id))
        self.conn.commit()

        return first_id

    def get_req(self, request_id: int):
        self.cursor.execute('SELECT bot_step, category FROM requests WHERE id = ?', (request_id,))
        return self.cursor.fetchone()

    def set_req_var(self, request_id: int, var: str, value):
        self.cursor.execute('UPDATE requests SET '+var+' = ? WHERE id = ?', (value, request_id,))
        self.conn.commit()

    def get_history(self, request_id: int):
        self.cursor.execute('SELECT messages FROM requests WHERE id = ?', (request_id,))
        result = self.cursor.fetchone()

        if not result:
            raise 'no such request'

        return json.loads(result[0]) or []
