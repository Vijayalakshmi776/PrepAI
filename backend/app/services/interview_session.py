from sqlalchemy.orm import Session

from app.crud.interview_session import interview_session as interview_session_crud
from app.models.interview_session import InterviewSession
from app.schemas.interview_session import InterviewSessionCreate, InterviewSessionUpdate


class InterviewSessionService:
    def get(self, db: Session, id: str) -> InterviewSession | None:
        return interview_session_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[InterviewSession]:
        return interview_session_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: InterviewSessionCreate) -> InterviewSession:
        return interview_session_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: InterviewSession, obj_in: InterviewSessionUpdate) -> InterviewSession:
        return interview_session_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> InterviewSession | None:
        return interview_session_crud.remove(db, id)


interview_session_service = InterviewSessionService()
