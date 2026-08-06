from sqlalchemy.orm import Session

from app.crud.student_skill import student_skill as student_skill_crud
from app.models.student_skill import StudentSkill
from app.schemas.student_skill import StudentSkillCreate, StudentSkillUpdate


class StudentSkillService:
    def get(self, db: Session, id: str) -> StudentSkill | None:
        return student_skill_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[StudentSkill]:
        return student_skill_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: StudentSkillCreate) -> StudentSkill:
        return student_skill_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: StudentSkill, obj_in: StudentSkillUpdate) -> StudentSkill:
        return student_skill_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> StudentSkill | None:
        return student_skill_crud.remove(db, id)


student_skill_service = StudentSkillService()
