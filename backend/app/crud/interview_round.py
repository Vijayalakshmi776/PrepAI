from app.crud.base import CRUDBase
from app.models.interview_round import InterviewRound
from app.schemas.interview_round import InterviewRoundCreate, InterviewRoundUpdate


class CRUDInterviewRound(CRUDBase[InterviewRound, InterviewRoundCreate, InterviewRoundUpdate]):
    pass


interview_round = CRUDInterviewRound(InterviewRound)
