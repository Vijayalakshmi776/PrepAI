from app.crud.base import CRUDBase
from app.models.roadmap import Roadmap
from app.schemas.roadmap import RoadmapCreate, RoadmapUpdate


class CRUDRoadmap(CRUDBase[Roadmap, RoadmapCreate, RoadmapUpdate]):
    pass


roadmap = CRUDRoadmap(Roadmap)
