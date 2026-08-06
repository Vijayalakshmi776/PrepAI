from sqlalchemy.orm import Session

from app.crud.skill import skill as skill_crud
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


class SkillService:
    def get(self, db: Session, id: str) -> Skill | None:
        return skill_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[Skill]:
        return skill_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: SkillCreate) -> Skill:
        return skill_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: Skill, obj_in: SkillUpdate) -> Skill:
        return skill_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> Skill | None:
        return skill_crud.remove(db, id)


skill_service = SkillService()
