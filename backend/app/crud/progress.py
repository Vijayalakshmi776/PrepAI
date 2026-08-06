from app.crud.base import CRUDBase
from app.models.progress import Progress
from app.schemas.progress import ProgressCreate, ProgressUpdate


class CRUDProgress(CRUDBase[Progress, ProgressCreate, ProgressUpdate]):
    pass


progress = CRUDProgress(Progress)
