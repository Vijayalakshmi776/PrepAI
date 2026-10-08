from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.api_v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.student_profile import StudentProfile
from app.services.roadmap_generator import (
    generate_personalized_roadmap,
    get_user_roadmap_data,
    toggle_roadmap_task,
)

router = APIRouter()


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    priority: int
    due_date: Optional[str] = None


class SkillGapResponse(BaseModel):
    id: str
    skill_name: str
    gap_description: Optional[str] = None
    priority: int


class ProgressSummary(BaseModel):
    completed_count: int
    total_tasks: int
    completion_percentage: float
    xp_points: int
    streak_days: int
    readiness_score: float = 0.0


class RoadmapDetailResponse(BaseModel):
    roadmap_id: str
    title: str
    summary: Optional[str] = None
    target_company: str
    target_role: str
    current_phase: str
    company_recommendations: list[str]
    tasks: list[TaskResponse]
    skill_gaps: list[SkillGapResponse]
    progress: ProgressSummary


class TaskToggleResponse(BaseModel):
    task_id: str
    title: str
    completed: bool
    progress: ProgressSummary


@router.get('/me', response_model=RoadmapDetailResponse, status_code=status.HTTP_200_OK)
def get_my_roadmap(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve the current user's personalized roadmap, tasks, skill gaps,
    company-specific recommendations, and progress.
    If the user has completed onboarding but has no roadmap, automatically generates one.
    """
    user_id = str(current_user.id)
    data = get_user_roadmap_data(db, user_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Roadmap not found. Please complete onboarding first.',
        )
    return data


@router.post('/generate', response_model=RoadmapDetailResponse, status_code=status.HTTP_200_OK)
def regenerate_roadmap(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Regenerate the personalized placement roadmap based on latest profile data
    and interview performance.
    """
    user_id = str(current_user.id)
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found. Please complete onboarding before generating a roadmap.',
        )
    data = generate_personalized_roadmap(db, user_id, profile)
    return data


@router.patch('/tasks/{task_id}/toggle', response_model=TaskToggleResponse, status_code=status.HTTP_200_OK)
def toggle_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Toggle task completion status (completed: true/false) and update progress and XP points.
    """
    user_id = str(current_user.id)
    try:
        result = toggle_roadmap_task(db, user_id, task_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get('/skill-gaps', response_model=list[SkillGapResponse], status_code=status.HTTP_200_OK)
def get_skill_gaps(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve skill gaps identified for the authenticated user.
    """
    user_id = str(current_user.id)
    roadmap_data = get_user_roadmap_data(db, user_id)
    if not roadmap_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Skill gaps not found. Please complete onboarding.',
        )
    return roadmap_data.get('skill_gaps', [])


@router.get('/progress', response_model=ProgressSummary, status_code=status.HTTP_200_OK)
def get_progress(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve progress metrics for the user's roadmap.
    """
    user_id = str(current_user.id)
    roadmap_data = get_user_roadmap_data(db, user_id)
    if not roadmap_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Progress not found. Please complete onboarding.',
        )
    return roadmap_data.get('progress')
