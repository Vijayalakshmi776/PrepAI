from sqlalchemy.orm import Session

from app.crud.interview_answer import interview_answer as interview_answer_crud
from app.models.interview_answer import InterviewAnswer
from app.schemas.interview_answer import InterviewAnswerCreate, InterviewAnswerUpdate


class InterviewAnswerService:
    def get(self, db: Session, id: str) -> InterviewAnswer | None:
        return interview_answer_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[InterviewAnswer]:
        return interview_answer_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: InterviewAnswerCreate) -> InterviewAnswer:
        return interview_answer_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: InterviewAnswer, obj_in: InterviewAnswerUpdate) -> InterviewAnswer:
        return interview_answer_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> InterviewAnswer | None:
        return interview_answer_crud.remove(db, id)


interview_answer_service = InterviewAnswerService()
