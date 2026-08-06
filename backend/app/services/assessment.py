from sqlalchemy.orm import Session

from app.crud.assessment import assessment as assessment_crud
from app.models.assessment import Assessment
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate


class AssessmentService:
    def get(self, db: Session, id: str) -> Assessment | None:
        return assessment_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[Assessment]:
        return assessment_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: AssessmentCreate) -> Assessment:
        return assessment_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: Assessment, obj_in: AssessmentUpdate) -> Assessment:
        return assessment_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> Assessment | None:
        return assessment_crud.remove(db, id)


assessment_service = AssessmentService()
