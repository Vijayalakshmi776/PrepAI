from sqlalchemy.orm import Session

from app.crud.skill_gap import skill_gap as skill_gap_crud
from app.models.skill_gap import SkillGap
from app.schemas.skill_gap import SkillGapCreate, SkillGapUpdate


class SkillGapService:
    def get(self, db: Session, id: str) -> SkillGap | None:
        return skill_gap_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[SkillGap]:
        return skill_gap_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: SkillGapCreate) -> SkillGap:
        return skill_gap_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: SkillGap, obj_in: SkillGapUpdate) -> SkillGap:
        return skill_gap_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> SkillGap | None:
        return skill_gap_crud.remove(db, id)


skill_gap_service = SkillGapService()
