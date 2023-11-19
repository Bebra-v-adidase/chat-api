import json
from time import time
from typing import List
from pydantic import BaseModel

class Message:
    def __init__(self, from_id: int, text: str, date: int = None):
        self.text = text
        self.from_id = from_id
        self.date = date or time()

class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.__dict__
        return super().default(obj)

class Request:
    id: int
    category: str
    priority: int
    messages: List[Message]

class CreateRequest(BaseModel):
    text: str

def ApiResponse(success, data=None):
    return {
        'ok': success,
        'data': data
    }