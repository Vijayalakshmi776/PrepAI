from sqlalchemy.orm import Session

from app.crud.assessment_question import assessment_question as assessment_question_crud
from app.models.assessment_question import AssessmentQuestion
from app.schemas.assessment_question import AssessmentQuestionCreate, AssessmentQuestionUpdate


class AssessmentQuestionService:
    def get(self, db: Session, id: str) -> AssessmentQuestion | None:
        return assessment_question_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[AssessmentQuestion]:
        return assessment_question_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: AssessmentQuestionCreate) -> AssessmentQuestion:
        return assessment_question_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: AssessmentQuestion, obj_in: AssessmentQuestionUpdate) -> AssessmentQuestion:
        return assessment_question_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> AssessmentQuestion | None:
        return assessment_question_crud.remove(db, id)


assessment_question_service = AssessmentQuestionService()
