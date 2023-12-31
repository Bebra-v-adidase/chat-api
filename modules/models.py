import json
from time import time
from typing import List
from pydantic import BaseModel

class Message:
    def __init__(self, from_id: int, text: str, date: int = None, name: str = None, avatar: str = None, buttons: List[str] = None):
        self.text = text
        self.from_id = from_id
        self.date = date or int(time())

        if name:
            self.name = name
            self.avatar = avatar
            self.buttons = buttons

class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.__dict__
        return super().default(obj)

class Request:
    def __init__(self, id: int = None, category: int = None, priority: int = 0, messages: List[Message] = None, bot_step: int = 0):
        self.id = id
        self.category = category
        self.priority = priority
        self.bot_step = bot_step
        self.messages = messages or []

class CreateRequestData(BaseModel):
    text: str

class SendMessageData(BaseModel):
    request_id: int
    text: str

class GetHistoryData(BaseModel):
    request_id: int
    start_from: int = None

def ApiResponse(success, data=None):
    return {
        'ok': success,
        'data': data
    }
