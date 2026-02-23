from fastapi import APIRouter, Request, Header, HTTPException, BackgroundTasks
from app.services.line_service import handle_webhook
from linebot.exceptions import InvalidSignatureError

router = APIRouter(prefix="/line")

@router.post("/webhook")
async def webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str = Header(None)
):
    body = await request.body()

    # ตรวจ signature ก่อน (เร็วมาก)
    try:
        # แค่ validate ไม่ต้องทำงานหนัก
        handle_webhook.__self__.parser.parse(  # ถ้าใช้ linebot SDK แบบ handler
            body.decode("utf-8"),
            x_line_signature
        )
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # ส่งงานไปทำ background
    background_tasks.add_task(
        handle_webhook,
        body.decode("utf-8"),
        x_line_signature
    )

    return {"status": "ok"}
