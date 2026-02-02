from sqlalchemy import Column, String, Date, Boolean, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class shift_schedule(Base):
    __tablename__ = "shift_schedule"

    date = Column(Date, primary_key=True)
    cafe_schedule = Column(String, nullable=False)
    day_off = Column(Boolean, nullable=False)
    shift_1 = Column(String, nullable=False)
    shift_2 = Column(String, nullable=False)
    shift_3 = Column(String, nullable=False)
    shift_4 = Column(String, nullable=False)
    shift_5 = Column(String, nullable=False)
    shift_6 = Column(String, nullable=False)
    shift_7 = Column(String, nullable=True)
    shift_8 = Column(String, nullable=True)
    shift_receive = Column(String, nullable=True)
    free_day = Column(String, nullable=True)
    

class ShiftLog(Base):
    __tablename__ = "user_name_bg_1000"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code_name = Column(String)

