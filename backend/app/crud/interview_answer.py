from app.crud.base import CRUDBase
from app.models.interview_answer import InterviewAnswer
from app.schemas.interview_answer import InterviewAnswerCreate, InterviewAnswerUpdate


class CRUDInterviewAnswer(CRUDBase[InterviewAnswer, InterviewAnswerCreate, InterviewAnswerUpdate]):
    pass


interview_answer = CRUDInterviewAnswer(InterviewAnswer)
