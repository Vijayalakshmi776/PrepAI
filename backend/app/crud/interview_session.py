from app.crud.base import CRUDBase
from app.models.interview_session import InterviewSession
from app.schemas.interview_session import InterviewSessionCreate, InterviewSessionUpdate


class CRUDInterviewSession(CRUDBase[InterviewSession, InterviewSessionCreate, InterviewSessionUpdate]):
    pass


interview_session = CRUDInterviewSession(InterviewSession)
