from fastapi import APIRouter
from services.crud import create_request
from modules.request_classifier import RequestClassifier
from modules.models import CreateRequest, ApiResponse, Message

router = APIRouter()

@router.post("/createRequest")
async def createRequest(request: CreateRequest):
    try:
        text = request.text
        m = RequestClassifier()
        data = m.predict(text)

        messages = [Message(0, text)]
        id = create_request(data[0], data[1], messages, 0)

        return ApiResponse(True, id)
    except Exception as e:
        return ApiResponse(False, str(e))
