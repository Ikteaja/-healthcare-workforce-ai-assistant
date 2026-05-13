from fastapi import FastAPI

from backend.api.documents import router as documents_router

app = FastAPI(title="Healthcare Workforce AI Assistant")
app.include_router(documents_router)


@app.get("/")
def root():
    return {
        "message": "Healthcare Workforce AI Assistant API is running"
    }
