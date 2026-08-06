from app.crud.base import CRUDBase
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate


class CRUDResume(CRUDBase[Resume, ResumeCreate, ResumeUpdate]):
    pass


resume = CRUDResume(Resume)
