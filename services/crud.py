import json
from modules.db import get_connection
from modules.models import MessageEncoder


def create_request(category: int, priority: int, messages: list, employee_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    messages = json.dumps(messages, cls=MessageEncoder)
    cursor.execute('''
        INSERT INTO requests (category, priority, messages, employee_id)
        VALUES (?, ?, ?, ?)
    ''', (category, priority, messages, employee_id))

    request_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return request_id
