from sqlalchemy.orm import Session

from app.crud.roadmap import roadmap as roadmap_crud
from app.models.roadmap import Roadmap
from app.schemas.roadmap import RoadmapCreate, RoadmapUpdate


class RoadmapService:
    def get(self, db: Session, id: str) -> Roadmap | None:
        return roadmap_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[Roadmap]:
        return roadmap_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: RoadmapCreate) -> Roadmap:
        return roadmap_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: Roadmap, obj_in: RoadmapUpdate) -> Roadmap:
        return roadmap_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> Roadmap | None:
        return roadmap_crud.remove(db, id)


roadmap_service = RoadmapService()
