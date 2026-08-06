from sqlalchemy.orm import Session

from app.crud.progress import progress as progress_crud
from app.models.progress import Progress
from app.schemas.progress import ProgressCreate, ProgressUpdate


class ProgressService:
    def get(self, db: Session, id: str) -> Progress | None:
        return progress_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[Progress]:
        return progress_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: ProgressCreate) -> Progress:
        return progress_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: Progress, obj_in: ProgressUpdate) -> Progress:
        return progress_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> Progress | None:
        return progress_crud.remove(db, id)


progress_service = ProgressService()
