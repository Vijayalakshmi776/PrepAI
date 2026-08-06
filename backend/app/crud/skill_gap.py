from app.crud.base import CRUDBase
from app.models.skill_gap import SkillGap
from app.schemas.skill_gap import SkillGapCreate, SkillGapUpdate


class CRUDSkillGap(CRUDBase[SkillGap, SkillGapCreate, SkillGapUpdate]):
    pass


skill_gap = CRUDSkillGap(SkillGap)
