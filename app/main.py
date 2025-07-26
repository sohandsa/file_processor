from fastapi import FastAPI
from app.routes.upload import router as rfrouter

app = FastAPI()

app.include_router(rfrouter)

@app.get("/")
async def echo():
    return "Hello World"
