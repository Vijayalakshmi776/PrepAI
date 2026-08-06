from app.crud.base import CRUDBase
from app.models.assessment_result import AssessmentResult
from app.schemas.assessment_result import AssessmentResultCreate, AssessmentResultUpdate


class CRUDAssessmentResult(CRUDBase[AssessmentResult, AssessmentResultCreate, AssessmentResultUpdate]):
    pass


assessment_result = CRUDAssessmentResult(AssessmentResult)
