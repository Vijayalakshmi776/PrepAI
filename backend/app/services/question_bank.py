from sqlalchemy.orm import Session

from app.crud.question_bank import question_bank as question_bank_crud
from app.models.question_bank import QuestionBank
from app.schemas.question_bank import QuestionBankCreate, QuestionBankUpdate


class QuestionBankService:
    def get(self, db: Session, id: str) -> QuestionBank | None:
        return question_bank_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[QuestionBank]:
        return question_bank_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: QuestionBankCreate) -> QuestionBank:
        return question_bank_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: QuestionBank, obj_in: QuestionBankUpdate) -> QuestionBank:
        return question_bank_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> QuestionBank | None:
        return question_bank_crud.remove(db, id)


question_bank_service = QuestionBankService()
