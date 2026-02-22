from fastapi import FastAPI
from app.routers import line, shifts

app = FastAPI(title="Shift Scheduler API")

# 🔗 include routers
app.include_router(line.router)
app.include_router(shifts.router)

# welcome page
@app.get("/")
def root():
    return {"status": "ok"}

@app.api_route("/ping", methods=["GET", "HEAD"])
def ping():
    return Response(content='{"ping": "pong"}', media_type="application/json")
