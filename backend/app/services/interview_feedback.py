from sqlalchemy.orm import Session

from app.crud.interview_feedback import interview_feedback as interview_feedback_crud
from app.models.interview_feedback import InterviewFeedback
from app.schemas.interview_feedback import InterviewFeedbackCreate, InterviewFeedbackUpdate


class InterviewFeedbackService:
    def get(self, db: Session, id: str) -> InterviewFeedback | None:
        return interview_feedback_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[InterviewFeedback]:
        return interview_feedback_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: InterviewFeedbackCreate) -> InterviewFeedback:
        return interview_feedback_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: InterviewFeedback, obj_in: InterviewFeedbackUpdate) -> InterviewFeedback:
        return interview_feedback_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> InterviewFeedback | None:
        return interview_feedback_crud.remove(db, id)


interview_feedback_service = InterviewFeedbackService()
