from sqlalchemy.orm import Session

from app.crud.student_profile import student_profile as student_profile_crud
from app.models.student_profile import StudentProfile
from app.schemas.student_profile import StudentProfileCreate, StudentProfileUpdate


class StudentProfileService:
    def get(self, db: Session, id: str) -> StudentProfile | None:
        return student_profile_crud.get(db, id)

    def get_by_user(self, db: Session, user_id: str) -> StudentProfile | None:
        return student_profile_crud.get_by_user_id(db, user_id)

    def create(self, db: Session, obj_in: StudentProfileCreate) -> StudentProfile:
        return student_profile_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: StudentProfile, obj_in: StudentProfileUpdate) -> StudentProfile:
        return student_profile_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> StudentProfile | None:
        return student_profile_crud.remove(db, id)


student_profile_service = StudentProfileService()
