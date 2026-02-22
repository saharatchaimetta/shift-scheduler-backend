from datetime import date
from datetime import date, timedelta
from datetime import datetime, date

from sqlalchemy.orm import Session
from app.models import shift_schedule,ShiftLog

def get_shift_by_date(db: Session, target_date):
    print(f"Fetching shifts for date: {target_date}")
    print(f"Type of target_date: {type(target_date)}")
    return (
        db.query(shift_schedule)
        # .limit(1)
        .filter(shift_schedule.date == target_date)
        # .all()
        .first()
        
    )

# SHIFT_COLS = [
#     "shift_1", "shift_2", "shift_3", "shift_4",
#     "shift_5", "shift_6", "shift_7", "shift_8",
#     "shift_receive", "free_day"
# ]

def get_shift_with_names(db: Session, target_date: date):
    # 1. ดึงข้อมูลเวร
    shift = (
        db.query(shift_schedule)
        .filter(shift_schedule.date == target_date)
        .first()
    )

    if not shift:
        return None

    # 2. ดึงพนักงาน (ครั้งเดียว)
    employees = db.query(ShiftLog).all()
    code_to_name = {e.code_name: e.name for e in employees}

    # 3. helper map
    def map_name(x):
        if x in ["-", None, "All"]:
            return x
        return code_to_name.get(x, x)

    # 4. คืนข้อมูลพร้อมชื่อ
    return {
        "date": shift.date,
        "cafe_schedule": map_name(shift.cafe_schedule),
        "day_off": shift.day_off,

        "shift_1": map_name(shift.shift_1),
        "shift_2": map_name(shift.shift_2),
        "shift_3": map_name(shift.shift_3),
        "shift_4": map_name(shift.shift_4),
        "shift_5": map_name(shift.shift_5),
        "shift_6": map_name(shift.shift_6),
        "shift_7": map_name(shift.shift_7),
        "shift_8": map_name(shift.shift_8),
        "shift_receive": map_name(shift.shift_receive),
        "free_day": map_name(shift.free_day),
    }

def shifts_to_vertical(shift: dict):
    rows = []
    count = sum(1 for v in shift.values() if v != "-")
    print('count_log')
    print(count)
    if shift["day_off"] == True and count == 11:
        # 🔴 วันหยุด → มีผลัด 1–8 เท่านั้น
        SHIFT_LABELS = [
            ("18.00-20.00", "shift_1"),
            ("20.00-22.00", "shift_2"),
            ("22.00-00.00", "shift_3"),
            ("00.00-02.00", "shift_4"),
            ("02.00-04.00", "shift_5"),
            ("04.00-06.00", "shift_6"),
        ]
    if shift["day_off"] == True and count == 10:
        # 🔴 วันหยุด → มีผลัด 1–8 เท่านั้น
        SHIFT_LABELS = [
            ("16.00-18.00", "shift_1"),
            ("18.00-20.00", "shift_2"),
            ("20.00-22.00", "shift_3"),
            ("22.00-00.00", "shift_4"),
            ("00.00-02.00", "shift_5"),
            ("02.00-04.00", "shift_6"),
            ("04.00-06.00", "shift_7"),
        ]
    elif shift["day_off"] == True and count > 10:
        # 🔴 วันหยุด → มีผลัด 1–8 + Cafe
        SHIFT_LABELS = [
            ("14.00-16.00", "shift_1"),
            ("16.00-18.00", "shift_2"),
            ("18.00-20.00", "shift_3"),
            ("20.00-22.00", "shift_4"),
            ("22.00-00.00", "shift_5"),
            ("00.00-02.00", "shift_6"),
            ("02.00-04.00", "shift_7"),
            ("04.00-06.00", "shift_8"),
        ]
    else:
        # 🟢 วันทำงาน → ผลัด 1–6 + เวรรับส่ง + Free Day
        SHIFT_LABELS = [
            ("18.00-20.00", "shift_1"),
            ("20.00-22.00", "shift_2"),
            ("22.00-00.00", "shift_3"),
            ("00.00-02.00", "shift_4"),
            ("02.00-04.00", "shift_5"),
            ("04.00-05.30", "shift_6"),
            ("🚚 เวรรับส่ง", "shift_receive"),
            ("🛑 Free Day", "free_day"),
        ]

    for label, key in SHIFT_LABELS:
        value = shift.get(key)
        if value and value != "-":
            rows.append((label, value))

    # ☕ Cafe แสดงทุกวัน
    # if shift["day_off"] == False:
    rows.append(("☕ Cafe", shift["cafe_schedule"]))
    # else:
    #     rows.append(("04.00-06.00", shift["cafe_schedule"]))

    return rows

