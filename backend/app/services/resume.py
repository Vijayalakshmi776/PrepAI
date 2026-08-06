from sqlalchemy.orm import Session

from app.crud.resume import resume as resume_crud
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate


class ResumeService:
    def get(self, db: Session, id: str) -> Resume | None:
        return resume_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[Resume]:
        return resume_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: ResumeCreate) -> Resume:
        return resume_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: Resume, obj_in: ResumeUpdate) -> Resume:
        return resume_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> Resume | None:
        return resume_crud.remove(db, id)


resume_service = ResumeService()
