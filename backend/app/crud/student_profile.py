from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.student_profile import StudentProfile
from app.schemas.student_profile import StudentProfileCreate, StudentProfileUpdate


class CRUDStudentProfile(CRUDBase[StudentProfile, StudentProfileCreate, StudentProfileUpdate]):
    def get_by_user_id(self, db: Session, user_id: str) -> StudentProfile | None:
        return db.query(self.model).filter(self.model.user_id == user_id).first()


student_profile = CRUDStudentProfile(StudentProfile)
