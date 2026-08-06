from app.crud.base import CRUDBase
from app.models.interview_question import InterviewQuestion
from app.schemas.interview_question import InterviewQuestionCreate, InterviewQuestionUpdate


class CRUDInterviewQuestion(CRUDBase[InterviewQuestion, InterviewQuestionCreate, InterviewQuestionUpdate]):
    pass


interview_question = CRUDInterviewQuestion(InterviewQuestion)
