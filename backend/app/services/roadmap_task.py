from sqlalchemy.orm import Session

from app.crud.roadmap_task import roadmap_task as roadmap_task_crud
from app.models.roadmap_task import RoadmapTask
from app.schemas.roadmap_task import RoadmapTaskCreate, RoadmapTaskUpdate


class RoadmapTaskService:
    def get(self, db: Session, id: str) -> RoadmapTask | None:
        return roadmap_task_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[RoadmapTask]:
        return roadmap_task_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: RoadmapTaskCreate) -> RoadmapTask:
        return roadmap_task_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: RoadmapTask, obj_in: RoadmapTaskUpdate) -> RoadmapTask:
        return roadmap_task_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> RoadmapTask | None:
        return roadmap_task_crud.remove(db, id)


roadmap_task_service = RoadmapTaskService()
