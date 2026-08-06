from app.crud.base import CRUDBase
from app.models.student_skill import StudentSkill
from app.schemas.student_skill import StudentSkillCreate, StudentSkillUpdate


class CRUDStudentSkill(CRUDBase[StudentSkill, StudentSkillCreate, StudentSkillUpdate]):
    pass


student_skill = CRUDStudentSkill(StudentSkill)
