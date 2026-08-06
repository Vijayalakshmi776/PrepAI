from app.crud.base import CRUDBase
from app.models.assessment_answer import AssessmentAnswer
from app.schemas.assessment_answer import AssessmentAnswerCreate, AssessmentAnswerUpdate


class CRUDAssessmentAnswer(CRUDBase[AssessmentAnswer, AssessmentAnswerCreate, AssessmentAnswerUpdate]):
    pass


assessment_answer = CRUDAssessmentAnswer(AssessmentAnswer)
