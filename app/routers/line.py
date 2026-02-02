from fastapi import APIRouter, Request, Header, HTTPException
from app.services.line_service import handle_webhook
from linebot.exceptions import InvalidSignatureError

router = APIRouter(prefix="/line")

@router.post("/webhook")
async def webhook(
    request: Request,
    x_line_signature: str = Header(None)
):
    body = await request.body()

    try:
        handle_webhook(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return {"status": "ok"}
