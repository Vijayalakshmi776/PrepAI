from sqlalchemy.orm import Session

from app.crud.assessment_result import assessment_result as assessment_result_crud
from app.models.assessment_result import AssessmentResult
from app.schemas.assessment_result import AssessmentResultCreate, AssessmentResultUpdate


class AssessmentResultService:
    def get(self, db: Session, id: str) -> AssessmentResult | None:
        return assessment_result_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[AssessmentResult]:
        return assessment_result_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: AssessmentResultCreate) -> AssessmentResult:
        return assessment_result_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: AssessmentResult, obj_in: AssessmentResultUpdate) -> AssessmentResult:
        return assessment_result_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> AssessmentResult | None:
        return assessment_result_crud.remove(db, id)


assessment_result_service = AssessmentResultService()
