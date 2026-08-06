from app.crud.base import CRUDBase
from app.models.assessment_question import AssessmentQuestion
from app.schemas.assessment_question import AssessmentQuestionCreate, AssessmentQuestionUpdate


class CRUDAssessmentQuestion(CRUDBase[AssessmentQuestion, AssessmentQuestionCreate, AssessmentQuestionUpdate]):
    pass


assessment_question = CRUDAssessmentQuestion(AssessmentQuestion)
