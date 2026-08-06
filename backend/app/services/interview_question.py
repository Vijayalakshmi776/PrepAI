from sqlalchemy.orm import Session

from app.crud.interview_question import interview_question as interview_question_crud
from app.models.interview_question import InterviewQuestion
from app.schemas.interview_question import InterviewQuestionCreate, InterviewQuestionUpdate


class InterviewQuestionService:
    def get(self, db: Session, id: str) -> InterviewQuestion | None:
        return interview_question_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[InterviewQuestion]:
        return interview_question_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: InterviewQuestionCreate) -> InterviewQuestion:
        return interview_question_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: InterviewQuestion, obj_in: InterviewQuestionUpdate) -> InterviewQuestion:
        return interview_question_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> InterviewQuestion | None:
        return interview_question_crud.remove(db, id)


interview_question_service = InterviewQuestionService()
