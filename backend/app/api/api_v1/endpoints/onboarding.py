from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class OnboardingRequest(BaseModel):
    user_id: str
    user_type: str
    career_goal: str
    company_type: str
    dream_company: str
    target_role: str
    current_level: str
    skills: list[str]

class OnboardingResponse(BaseModel):
    status: str
    message: str

@router.post('/', response_model=OnboardingResponse)
def submit_onboarding(request: OnboardingRequest) -> OnboardingResponse:
    return {'status': 'ok', 'message': 'Onboarding data received and will be used to personalize the student journey.'}
