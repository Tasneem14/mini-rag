from fastapi import APIRouter, FastAPI, Depends
from helpers.config import get_settings, Settings

base_router = APIRouter(
prefix = "/api/v1",
tags= ["api_v1"]
)

@base_router.get("/")
async def welcome(Settings: Settings = Depends(get_settings)):
    return {"message": "Welcome to the Mini-RAG", "app_name": Settings.APP_NAME, "app_version": Settings.APP_VERSION}
  