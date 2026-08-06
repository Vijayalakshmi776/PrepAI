from sqlalchemy.orm import Session

from app.crud.resume_analysis import resume_analysis as resume_analysis_crud
from app.models.resume_analysis import ResumeAnalysis
from app.schemas.resume_analysis import ResumeAnalysisCreate, ResumeAnalysisUpdate


class ResumeAnalysisService:
    def get(self, db: Session, id: str) -> ResumeAnalysis | None:
        return resume_analysis_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[ResumeAnalysis]:
        return resume_analysis_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: ResumeAnalysisCreate) -> ResumeAnalysis:
        return resume_analysis_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: ResumeAnalysis, obj_in: ResumeAnalysisUpdate) -> ResumeAnalysis:
        return resume_analysis_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> ResumeAnalysis | None:
        return resume_analysis_crud.remove(db, id)


resume_analysis_service = ResumeAnalysisService()
