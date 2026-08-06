from app.crud.base import CRUDBase
from app.models.roadmap_task import RoadmapTask
from app.schemas.roadmap_task import RoadmapTaskCreate, RoadmapTaskUpdate


class CRUDRoadmapTask(CRUDBase[RoadmapTask, RoadmapTaskCreate, RoadmapTaskUpdate]):
    pass


roadmap_task = CRUDRoadmapTask(RoadmapTask)
