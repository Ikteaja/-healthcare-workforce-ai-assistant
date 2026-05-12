from fastapi import FastAPI

app = FastAPI(title="Healthcare Workforce AI Assistant")


@app.get("/")
def root():
    return {
        "message": "Healthcare Workforce AI Assistant API is running"
    }
