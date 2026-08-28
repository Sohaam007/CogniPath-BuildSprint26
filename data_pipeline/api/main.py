from fastapi import FastAPI

app = FastAPI(title="CogniPath API")

@app.get("/")
def root():
    return {"message": "CogniPath API is running"}
