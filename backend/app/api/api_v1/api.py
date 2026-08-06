from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, onboarding

api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(onboarding.router, prefix='/onboarding', tags=['onboarding'])
