from fastapi import APIRouter
from app.services.shift_service import *

router = APIRouter()

@router.get("/today")
def today_shift():
    return None
