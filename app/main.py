from fastapi import FastAPI

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