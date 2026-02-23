from fastapi import APIRouter, Request, Header, BackgroundTasks
from app.services.line_service import handle_webhook

router = APIRouter(prefix="/line")

@router.post("/webhook")
async def webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str = Header(None)
):
    body = await request.body()

    # ส่งไปทำงาน background ทันที
    background_tasks.add_task(
        handle_webhook,
        body.decode("utf-8"),
        x_line_signature
    )

    return {"status": "ok"}
