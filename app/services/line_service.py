import os
from pydoc import text
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from linebot.models import FlexSendMessage
from app.models import shift_schedule,ShiftLog
from datetime import date, timedelta
from app.services.shift_service import shifts_to_vertical,get_shift_with_names
from app.database import SessionLocal
from linebot.models import FlexSendMessage,PostbackEvent
from linebot.models import PostbackEvent
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)    
parser = WebhookParser(LINE_CHANNEL_SECRET)

def build_shift_flex(target_date, shift: dict):
    contents = []
    print('shift_log2')
    print(shift)
    # ===== สถานะวัน =====
    if shift.get("day_off"):
        day_status = {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": "🔴 วันหยุด",
                    "color": "#EF4444",
                    "weight": "bold",
                    "size": "sm"
                }
            ]
        }
    else:
        day_status = {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": "🟢 วันทำงาน",
                    "color": "#22C55E",
                    "weight": "bold",
                    "size": "sm"
                }
            ]
        }

    # ===== ผลัด =====
    for label, value in shifts_to_vertical(shift):
        contents.append({
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": label,
                    "color": "#1B1A1A",
                    "size": "sm",
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": value,
                    "size": "sm",
                    "flex": 7,
                    "wrap": True
                }
            ]
        })

    return FlexSendMessage(
        alt_text=f"เวรวันที่ {target_date.strftime('%d/%m/%Y')}",
        contents={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"📅 เวรวันที่ {target_date.strftime('%d/%m/%Y')}",
                        "weight": "bold",
                        "size": "md"
                    },
                    day_status,        # 👈 เพิ่มตรงนี้
                    {"type": "separator"},
                    *contents
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#22C55E",
                        "action": {
                            "type": "message",
                            "label": "📅 เวรวันนี้",
                            "text": "เวรวันนี้"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "action": {
                            "type": "message",
                            "label": "▶️ เวรพรุ่งนี้",
                            "text": "เวรพรุ่งนี้"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "action": {
                            "type": "datetimepicker",
                            "label": "🗓 เลือกวันที่",
                            "mode": "date",
                            "data": "pick_shift_date"
                        }
                    }
                ]
            }
        }
    )


# def handle_webhook(body: str, signature: str):
#     events = parser.parse(body, signature)

#     for event in events:

#         # ===== กรณีเลือกวันที่จาก datepicker =====
#         if isinstance(event, PostbackEvent):
#             if event.postback.data == "pick_shift_date":
#                 selected_date = event.postback.params.get("date")  # YYYY-MM-DD
#                 target_date = date.fromisoformat(selected_date)

#         # ===== ข้อความปกติ =====
#         elif isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
#             text = event.message.text.strip()

#             if text == "เวรวันนี้":
#                 target_date = date.today()
#             elif text == "เวรพรุ่งนี้":
#                 target_date = date.today() + timedelta(days=1)
#             else:
#                 return

#         # ===== ดึงเวร =====
#         db = SessionLocal()
#         shift = get_shift_with_names(db, target_date)
#         db.close()

#         if not shift:
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text="❌ ไม่พบข้อมูลเวร")
#             )
#             return
#         print(shift)
#         flex = build_shift_flex(target_date, shift)
#         line_bot_api.reply_message(event.reply_token, flex)



def handle_webhook(body: str, signature: str):
    events = parser.parse(body, signature)

    for event in events:
        target_date = None  # ⭐ สำคัญมาก

        # ===== กรณีเลือกวันที่จาก datepicker =====
        if isinstance(event, PostbackEvent):
            if event.postback.data == "pick_shift_date":
                selected_date = event.postback.params.get("date")  # YYYY-MM-DD
                target_date = date.fromisoformat(selected_date)

        # ===== ข้อความปกติ =====
        elif isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            text = event.message.text.strip()

            if text == "เวรวันนี้":
                target_date = date.today()
            elif text == "เวรพรุ่งนี้":
                target_date = date.today() + timedelta(days=1)
            else:
                continue  # ❗ อย่า return

        # ===== ถ้าไม่ใช่คำสั่ง → ข้าม =====
        if not target_date:
            continue

        # ===== ดึงเวร =====
        db = SessionLocal()
        shift = get_shift_with_names(db, target_date)
        db.close()

        if not shift:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="❌ ไม่พบข้อมูลเวร")
            )
            continue

        print(shift)
        flex = build_shift_flex(target_date, shift)
        line_bot_api.reply_message(event.reply_token, flex)
