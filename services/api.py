from fastapi import APIRouter
from services.crud import CRUD
from modules.models import *
from modules.request_classifier import RequestClassifier

db = CRUD()
router = APIRouter()

@router.post("/createRequest")
async def createRequest(request: CreateRequestData):
    try:
        text = request.text
        m = RequestClassifier()
        data = m.predict(text)

        messages = [Message(0, text)]
        id = db.create_request(data[0], data[1], messages, 0)

        return ApiResponse(True, id)
    except Exception as e:
        return ApiResponse(False, str(e))

@router.post("/sendMessage")
async def createRequest(request: SendMessageData):
    try:
        msg = Message(0, request.text)
        message_id = db.push_message(request.request_id, msg)
        return ApiResponse(True, message_id)
    except Exception as e:
        return ApiResponse(False, str(e))

@router.post("/getHistory")
async def createRequest(request: GetHistoryData):
    try:
        messages = db.get_history(request.request_id)
        return ApiResponse(True, messages)
    except Exception as e:
        return ApiResponse(False, str(e))

