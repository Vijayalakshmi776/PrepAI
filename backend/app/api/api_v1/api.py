from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, onboarding, interview, roadmap, resume

api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(onboarding.router, prefix='/onboarding', tags=['onboarding'])
api_router.include_router(interview.router, prefix='/interview', tags=['interview'])
api_router.include_router(roadmap.router, prefix='/roadmap', tags=['roadmap'])
api_router.include_router(resume.router, prefix='/resume', tags=['resume'])
