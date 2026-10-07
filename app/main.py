from fastapi import FastAPI

from app.api.tickets import router as tickets_router
from app.api.ask import router as ask_router


app = FastAPI(
    title="AI Customer Support Intelligence",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "AI Customer Support Intelligence API",
        "status": "running",
    }


app.include_router(tickets_router)
app.include_router(ask_router)