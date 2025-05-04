from fastapi import APIRouter
from app.api.endpoints import translate

api_router = APIRouter()

# Include translation endpoints
api_router.include_router(translate.router, prefix="/translate", tags=["translation"])