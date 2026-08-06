from sqlalchemy.orm import Session

from app.crud.company_interview_pattern import company_interview_pattern as company_interview_pattern_crud
from app.models.company_interview_pattern import CompanyInterviewPattern
from app.schemas.company_interview_pattern import CompanyInterviewPatternCreate, CompanyInterviewPatternUpdate


class CompanyInterviewPatternService:
    def get(self, db: Session, id: str) -> CompanyInterviewPattern | None:
        return company_interview_pattern_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[CompanyInterviewPattern]:
        return company_interview_pattern_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: CompanyInterviewPatternCreate) -> CompanyInterviewPattern:
        return company_interview_pattern_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: CompanyInterviewPattern, obj_in: CompanyInterviewPatternUpdate) -> CompanyInterviewPattern:
        return company_interview_pattern_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> CompanyInterviewPattern | None:
        return company_interview_pattern_crud.remove(db, id)


company_interview_pattern_service = CompanyInterviewPatternService()
