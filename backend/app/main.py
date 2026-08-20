from fastapi import FastAPI

app = FastAPI(title="AI Job Board API")

@app.get("/")
def root():
    return {"status": "ok", "message": "AI Job Board API running"}
