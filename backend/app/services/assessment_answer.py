from sqlalchemy.orm import Session

from app.crud.assessment_answer import assessment_answer as assessment_answer_crud
from app.models.assessment_answer import AssessmentAnswer
from app.schemas.assessment_answer import AssessmentAnswerCreate, AssessmentAnswerUpdate


class AssessmentAnswerService:
    def get(self, db: Session, id: str) -> AssessmentAnswer | None:
        return assessment_answer_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[AssessmentAnswer]:
        return assessment_answer_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: AssessmentAnswerCreate) -> AssessmentAnswer:
        return assessment_answer_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: AssessmentAnswer, obj_in: AssessmentAnswerUpdate) -> AssessmentAnswer:
        return assessment_answer_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> AssessmentAnswer | None:
        return assessment_answer_crud.remove(db, id)


assessment_answer_service = AssessmentAnswerService()
