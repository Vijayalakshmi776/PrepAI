import json
import logging
import re
import uuid
from datetime import datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.api_v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.models.student_profile import StudentProfile
from app.models.student_skill import StudentSkill
from app.models.skill import Skill
from app.models.skill_gap import SkillGap
from app.services.resume_analyzer import analyze_resume_content, extract_text_from_pdf

logger = logging.getLogger(__name__)
router = APIRouter()


class BeforeAfterSuggestion(BaseModel):
    original_text: Optional[str] = ""
    improved_text: Optional[str] = ""
    reason: Optional[str] = "Rewrite for higher technical impact"


class JobRoleRecommendation(BaseModel):
    role: str
    match_percentage: float
    matching_skills: list[str]
    missing_skills: list[str]
    reason: str


class ResumeAnalysisDetailResponse(BaseModel):
    id: str
    resume_id: str
    title: str
    created_at: datetime
    readiness_score: float
    role_suitability_score: float
    role_suitability_status: str = "Good Match"
    ats_score: float
    clarity_score: float
    impact_score: float
    skill_alignment_score: float
    summary: str
    detected_skills: list[str]
    matching_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    target_role: str
    target_company: str
    word_count: int
    
    # Category breakdown
    overall_score: float
    keyword_match_score: float
    skills_score: float
    experience_score: float
    project_score: float
    education_score: float
    formatting_score: float

    # Extracted fields
    extracted_name: Optional[str] = None
    extracted_email: Optional[str] = None
    extracted_phone: Optional[str] = None
    extracted_education: list[str]
    extracted_experience: list[str]
    extracted_projects: list[str]
    extracted_technical_skills: list[str]
    extracted_soft_skills: list[str]
    extracted_certifications: list[str]
    extracted_achievements: list[str]
    extracted_links: list[str]

    # Improvements
    missing_keywords: list[str]
    formatting_issues: list[str]
    content_improvements: list[str]
    project_improvements: list[str]
    experience_improvements: list[str]

    before_after_suggestions: list[BeforeAfterSuggestion]
    job_role_recommendations: list[JobRoleRecommendation]
    roles_requiring_preparation: list[JobRoleRecommendation] = []

    role_suitability_explanation: str
    ai_personalization_used: bool
    gemini_used: bool = False
    fallback_used: bool = False


class ResumeSummaryResponse(BaseModel):
    id: str
    resume_id: str
    title: str
    readiness_score: float
    ats_score: float
    created_at: datetime


def format_analysis_response(resume: Resume, analysis: ResumeAnalysis) -> ResumeAnalysisDetailResponse:
    """Helper to deserialize stored JSON diagnostic fields into clean response model."""
    recs: list[str] = []
    if analysis.recommendations:
        try:
            recs = json.loads(analysis.recommendations)
        except Exception:
            recs = [analysis.recommendations]

    gaps_data: dict[str, Any] = {}
    if analysis.skill_gaps:
        try:
            gaps_data = json.loads(analysis.skill_gaps)
        except Exception:
            gaps_data = {}

    return ResumeAnalysisDetailResponse(
        id=str(analysis.id),
        resume_id=str(resume.id),
        title=resume.title,
        created_at=analysis.created_at,
        readiness_score=analysis.readiness_score or 0.0,
        role_suitability_score=gaps_data.get("role_suitability_score", analysis.readiness_score or 0.0),
        role_suitability_status=gaps_data.get("role_suitability_status", "Good Match"),
        ats_score=gaps_data.get("ats_score", analysis.readiness_score or 0.0),
        clarity_score=analysis.clarity_score or 0.0,
        impact_score=analysis.impact_score or 0.0,
        skill_alignment_score=analysis.skill_alignment_score or 0.0,
        summary=analysis.summary or "Resume analysis completed.",
        detected_skills=gaps_data.get("detected_skills", []),
        matching_skills=gaps_data.get("matching_skills", []),
        missing_skills=gaps_data.get("missing_skills", []),
        strengths=gaps_data.get("strengths", []),
        weaknesses=gaps_data.get("weaknesses", []),
        recommendations=recs,
        target_role=gaps_data.get("target_role", "Software Engineer"),
        target_company=gaps_data.get("target_company", "Tech Company"),
        word_count=resume.word_count or 0,
        
        overall_score=gaps_data.get("overall_score", analysis.readiness_score or 0.0),
        keyword_match_score=gaps_data.get("keyword_match_score", 0.0),
        skills_score=gaps_data.get("skills_score", 0.0),
        experience_score=gaps_data.get("experience_score", 0.0),
        project_score=gaps_data.get("project_score", 0.0),
        education_score=gaps_data.get("education_score", 0.0),
        formatting_score=gaps_data.get("formatting_score", 0.0),

        extracted_name=gaps_data.get("extracted_name"),
        extracted_email=gaps_data.get("extracted_email"),
        extracted_phone=gaps_data.get("extracted_phone"),
        extracted_education=gaps_data.get("extracted_education", []),
        extracted_experience=gaps_data.get("extracted_experience", []),
        extracted_projects=gaps_data.get("extracted_projects", []),
        extracted_technical_skills=gaps_data.get("extracted_technical_skills", []),
        extracted_soft_skills=gaps_data.get("extracted_soft_skills", []),
        extracted_certifications=gaps_data.get("extracted_certifications", []),
        extracted_achievements=gaps_data.get("extracted_achievements", []),
        extracted_links=gaps_data.get("extracted_links", []),

        missing_keywords=gaps_data.get("missing_keywords", []),
        formatting_issues=gaps_data.get("formatting_issues", []),
        content_improvements=gaps_data.get("content_improvements", []),
        project_improvements=gaps_data.get("project_improvements", []),
        experience_improvements=gaps_data.get("experience_improvements", []),
        
        before_after_suggestions=[
            {
                "original_text": item.get("original_text") or item.get("before") or "",
                "improved_text": item.get("improved_text") or item.get("after") or "",
                "reason": item.get("reason") or "Rewrite for higher technical impact"
            }
            for item in gaps_data.get("before_after_suggestions", [])
            if isinstance(item, dict)
        ],
        job_role_recommendations=gaps_data.get("job_role_recommendations", []),
        roles_requiring_preparation=gaps_data.get("roles_requiring_preparation", []),
        role_suitability_explanation=gaps_data.get("role_suitability_explanation", ""),
        
        ai_personalization_used=gaps_data.get("ai_personalization_used", False),
        gemini_used=gaps_data.get("gemini_used", gaps_data.get("ai_personalization_used", False)),
        fallback_used=gaps_data.get("fallback_used", False)
    )


@router.post('/analyze', response_model=ResumeAnalysisDetailResponse, status_code=status.HTTP_201_CREATED)
async def analyze_resume_upload(
    file: UploadFile = File(...),
    target_role: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Upload a PDF resume, extract text, perform AI & ATS assessment against target role/company,
    and persist results in PostgreSQL.
    """
    filename = file.filename or "resume.pdf"
    if not (filename.lower().endswith(".pdf") or file.content_type == "application/pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a PDF file (.pdf).",
        )

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded PDF file is empty.",
        )
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit of 10MB.",
        )

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_bytes)
    words = re.findall(r"\b[\w+#\.]+\b", extracted_text)
    logger.info(
        f"Resume Upload Diagnostic -> Filename: '{filename}', "
        f"Extracted length: {len(extracted_text)}, Word count: {len(words)}"
    )
    if not extracted_text or len(words) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to extract selectable text from this PDF. Please upload a text-based PDF.",
        )

    user_id = str(current_user.id)

    # Retrieve student's profile context for tailored evaluation
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    target_company = profile.target_company if profile and profile.target_company else "Tech Company"
    selected_target_role = target_role if target_role and target_role.strip() else (profile.target_role if profile and profile.target_role else "Software Engineer")
    career_goal = profile.career_goal if profile and profile.career_goal else "Placement"
    current_level = profile.current_level if profile and profile.current_level else "Intermediate"

    # User's declared skills
    student_skills_rows = (
        db.query(Skill.name)
        .join(StudentSkill, StudentSkill.skill_id == Skill.id)
        .filter(StudentSkill.user_id == user_id)
        .all()
    )
    onboarding_skills = [s[0] for s in student_skills_rows]

    # User's identified skill gaps
    skill_gap_rows = (
        db.query(Skill.name)
        .join(SkillGap, SkillGap.skill_id == Skill.id)
        .filter(SkillGap.user_id == user_id)
        .all()
    )
    roadmap_gaps = [g[0] for g in skill_gap_rows]

    # Run AI & ATS assessment engine
    analysis_data = analyze_resume_content(
        resume_text=extracted_text,
        target_role=selected_target_role,
        target_company=target_company,
        career_goal=career_goal,
        current_level=current_level,
        onboarding_skills=onboarding_skills,
        roadmap_skill_gaps=roadmap_gaps,
    )

    # 1. Persist Resume
    resume = Resume(
        id=uuid.uuid4(),
        user_id=user_id,
        title=filename,
        content=extracted_text[:8000],  # Store clean readable content
        file_type="pdf",
        language="en",
        word_count=analysis_data["word_count"],
        keywords=", ".join(analysis_data["detected_skills"][:15]),
    )
    db.add(resume)
    db.flush()

    stored_gaps = {**analysis_data}
    if "recommendations" in stored_gaps:
        del stored_gaps["recommendations"]

    resume_analysis = ResumeAnalysis(
        id=uuid.uuid4(),
        resume_id=resume.id,
        readiness_score=analysis_data.get("readiness_score", 0),
        clarity_score=analysis_data.get("formatting_score", 0),
        impact_score=analysis_data.get("experience_score", 0),
        skill_alignment_score=analysis_data.get("skills_score", 0),
        summary=analysis_data.get("summary", ""),
        recommendations=json.dumps(analysis_data["recommendations"]),
        skill_gaps=json.dumps(stored_gaps),
    )
    db.add(resume_analysis)
    db.commit()
    db.refresh(resume)
    db.refresh(resume_analysis)

    return format_analysis_response(resume, resume_analysis)


@router.get('/latest', response_model=ResumeAnalysisDetailResponse, status_code=status.HTTP_200_OK)
def get_latest_resume_analysis(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve the most recent resume analysis for the authenticated user.
    """
    user_id = str(current_user.id)
    resume = (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
        .first()
    )
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume has been uploaded yet.",
        )

    analysis = (
        db.query(ResumeAnalysis)
        .filter(ResumeAnalysis.resume_id == resume.id)
        .order_by(ResumeAnalysis.created_at.desc())
        .first()
    )
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found for this resume.",
        )

    return format_analysis_response(resume, analysis)


@router.get('/history', response_model=list[ResumeSummaryResponse], status_code=status.HTTP_200_OK)
def get_resume_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve list of past resume uploads and their readiness/ATS scores.
    """
    user_id = str(current_user.id)
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
        .all()
    )

    result: list[ResumeSummaryResponse] = []
    for r in resumes:
        analysis = (
            db.query(ResumeAnalysis)
            .filter(ResumeAnalysis.resume_id == r.id)
            .order_by(ResumeAnalysis.created_at.desc())
            .first()
        )
        if analysis:
            gaps_data = {}
            if analysis.skill_gaps:
                try:
                    gaps_data = json.loads(analysis.skill_gaps)
                except Exception:
                    gaps_data = {}
            result.append(
                ResumeSummaryResponse(
                    id=str(analysis.id),
                    resume_id=str(r.id),
                    title=r.title,
                    readiness_score=analysis.readiness_score or 0.0,
                    ats_score=gaps_data.get("ats_score", analysis.readiness_score or 0.0),
                    created_at=analysis.created_at,
                )
            )

    return result


@router.get('/{resume_id}', response_model=ResumeAnalysisDetailResponse, status_code=status.HTTP_200_OK)
def get_resume_by_id(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieve a specific resume and analysis by ID, enforcing ownership authorization.
    """
    user_id = str(current_user.id)
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    # Authorization Check
    if str(resume.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to access this resume.",
        )

    analysis = (
        db.query(ResumeAnalysis)
        .filter(ResumeAnalysis.resume_id == resume.id)
        .order_by(ResumeAnalysis.created_at.desc())
        .first()
    )
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found for this resume.",
        )

    return format_analysis_response(resume, analysis)


@router.delete('/{resume_id}', status_code=status.HTTP_200_OK)
def delete_resume_by_id(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a resume and cascade delete its analyses.
    """
    user_id = str(current_user.id)
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    if str(resume.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to delete this resume.",
        )

    db.delete(resume)
    db.commit()
    return {"status": "ok", "message": "Resume deleted successfully."}
