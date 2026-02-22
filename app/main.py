from fastapi import FastAPI, Response
from app.routers import line, shifts

app = FastAPI(title="Shift Scheduler API")

# 🔗 include routers
app.include_router(line.router)
app.include_router(shifts.router)

# welcome page
@app.get("/")
def root():
    return {"status": "ok"}

# ✅ Endpoint ที่ตอบสั้นและเร็วมาก (ปลุก Render ได้แน่)
@app.api_route("/ping", methods=["GET", "HEAD"])
def ping():
    return Response(content="pong", media_type="text/plain")
