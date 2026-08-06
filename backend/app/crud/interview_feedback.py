from app.crud.base import CRUDBase
from app.models.interview_feedback import InterviewFeedback
from app.schemas.interview_feedback import InterviewFeedbackCreate, InterviewFeedbackUpdate


class CRUDInterviewFeedback(CRUDBase[InterviewFeedback, InterviewFeedbackCreate, InterviewFeedbackUpdate]):
    pass


interview_feedback = CRUDInterviewFeedback(InterviewFeedback)
