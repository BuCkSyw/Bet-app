from fastapi import FastAPI

from app.router import router as line_provider_router

app = FastAPI()

app.include_router(line_provider_router)
