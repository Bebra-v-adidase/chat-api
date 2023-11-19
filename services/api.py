from fastapi import APIRouter
from services.crud import CRUD
from modules.models import *
from modules.request_classifier import RequestClassifier
from services.bot import Bot

db = CRUD()
router = APIRouter()
m = RequestClassifier()

@router.post("/createRequest")
async def createRequest(request: CreateRequestData):
    try:
        text = request.text
        data = m.predict(text)

        messages = [Message(0, text)]
        use_bot = Bot.check_bot(data, messages)

        id = db.create_request(data[0], data[1], messages, 0, 0 if use_bot else -1)

        return ApiResponse(True, id)
    except Exception as e:
        return ApiResponse(False, str(e))

@router.post("/sendMessage")
async def sendMessage(request: SendMessageData):
    try:
        text = request.text
        id = request.request_id
        messages = [Message(0, text)]

        switch = False
        use_bot = db.get_req_var(id, 'bot_step')
        if use_bot > 0:
            data = m.predict(text)
            switch = not Bot.check_bot(data, messages, True, id)

        first_id = db.push_messages(request.request_id, messages)

        if not switch:
            bot = Bot(id)

        return ApiResponse(True, first_id + 1)
    except Exception as e:
        return ApiResponse(False, str(e))

@router.post("/getHistory")
async def getHistory(request: GetHistoryData):
    try:
        last_id = int(request.start_from)
        messages = db.get_history(request.request_id)
        return ApiResponse(True, {
            'count': len(messages),
            'items': messages[last_id:]
        })
    except Exception as e:
        return ApiResponse(False, str(e))

