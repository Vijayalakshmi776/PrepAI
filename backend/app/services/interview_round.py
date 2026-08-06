from sqlalchemy.orm import Session

from app.crud.interview_round import interview_round as interview_round_crud
from app.models.interview_round import InterviewRound
from app.schemas.interview_round import InterviewRoundCreate, InterviewRoundUpdate


class InterviewRoundService:
    def get(self, db: Session, id: str) -> InterviewRound | None:
        return interview_round_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[InterviewRound]:
        return interview_round_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: InterviewRoundCreate) -> InterviewRound:
        return interview_round_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: InterviewRound, obj_in: InterviewRoundUpdate) -> InterviewRound:
        return interview_round_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> InterviewRound | None:
        return interview_round_crud.remove(db, id)


interview_round_service = InterviewRoundService()
