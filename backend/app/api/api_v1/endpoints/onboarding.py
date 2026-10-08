from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from app.api.api_v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.schemas.student_profile import StudentProfileCreate, StudentProfileUpdate, StudentProfileRead
from app.services.student_profile import student_profile_service

router = APIRouter()


class OnboardingRequest(BaseModel):
    user_type: str
    career_goal: str
    company_type: str
    dream_company: str
    target_role: str
    current_level: str
    interview_difficulty: Optional[str] = 'Medium'
    skills: list[str]


class OnboardingResponse(BaseModel):
    status: str
    message: str
    profile_id: Optional[str] = None


@router.post('/', response_model=OnboardingResponse, status_code=status.HTTP_200_OK)
def submit_onboarding(
    request: OnboardingRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> OnboardingResponse:
    """
    Save or update the current user's student profile from onboarding answers.
    The user_id is derived from the JWT — client-supplied user_id is ignored.
    """
    user_id = str(current_user.id)
    existing_profile = student_profile_service.get_by_user(db, user_id)

    if existing_profile:
        profile_update = StudentProfileUpdate(
            career_goal=request.career_goal,
            target_company=request.dream_company,
            target_role=request.target_role,
            current_level=request.current_level,
            interview_difficulty=request.interview_difficulty or 'Medium',
        )
        profile = student_profile_service.update(db, existing_profile, profile_update)
    else:
        profile_create = StudentProfileCreate(
            user_id=user_id,
            career_goal=request.career_goal,
            target_company=request.dream_company,
            target_role=request.target_role,
            current_level=request.current_level,
            interview_difficulty=request.interview_difficulty or 'Medium',
        )
        profile = student_profile_service.create(db, profile_create)

    return OnboardingResponse(
        status='ok',
        message='Onboarding data saved successfully.',
        profile_id=str(profile.id),
    )


@router.get('/me', response_model=StudentProfileRead)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Return the current user's student profile (onboarding data).
    Returns 404 if onboarding has not been completed yet.
    """
    user_id = str(current_user.id)
    profile = student_profile_service.get_by_user(db, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found. Please complete onboarding.',
        )
    return profile
