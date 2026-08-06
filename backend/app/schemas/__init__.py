from app.schemas.base import ORMBase
from app.schemas.user import UserBase, UserCreate, UserRead, UserUpdate
from app.schemas.student_profile import StudentProfileBase, StudentProfileCreate, StudentProfileRead, StudentProfileUpdate
from app.schemas.company import CompanyBase, CompanyCreate, CompanyRead, CompanyUpdate
from app.schemas.company_interview_pattern import CompanyInterviewPatternBase, CompanyInterviewPatternCreate, CompanyInterviewPatternRead, CompanyInterviewPatternUpdate
from app.schemas.interview_round import InterviewRoundBase, InterviewRoundCreate, InterviewRoundRead, InterviewRoundUpdate
from app.schemas.question_bank import QuestionBankBase, QuestionBankCreate, QuestionBankRead, QuestionBankUpdate
from app.schemas.resume import ResumeBase, ResumeCreate, ResumeRead, ResumeUpdate
from app.schemas.resume_analysis import ResumeAnalysisBase, ResumeAnalysisCreate, ResumeAnalysisRead, ResumeAnalysisUpdate
from app.schemas.progress import ProgressBase, ProgressCreate, ProgressRead, ProgressUpdate
from app.schemas.ai_conversation import AIConversationBase, AIConversationCreate, AIConversationRead, AIConversationUpdate

__all__ = [
    'ORMBase',
    'UserBase',
    'UserCreate',
    'UserRead',
    'UserUpdate',
    'StudentProfileBase',
    'StudentProfileCreate',
    'StudentProfileRead',
    'StudentProfileUpdate',
    'CompanyBase',
    'CompanyCreate',
    'CompanyRead',
    'CompanyUpdate',
    'CompanyInterviewPatternBase',
    'CompanyInterviewPatternCreate',
    'CompanyInterviewPatternRead',
    'CompanyInterviewPatternUpdate',
    'InterviewRoundBase',
    'InterviewRoundCreate',
    'InterviewRoundRead',
    'InterviewRoundUpdate',
    'QuestionBankBase',
    'QuestionBankCreate',
    'QuestionBankRead',
    'QuestionBankUpdate',
    'ResumeBase',
    'ResumeCreate',
    'ResumeRead',
    'ResumeUpdate',
    'ResumeAnalysisBase',
    'ResumeAnalysisCreate',
    'ResumeAnalysisRead',
    'ResumeAnalysisUpdate',
    'ProgressBase',
    'ProgressCreate',
    'ProgressRead',
    'ProgressUpdate',
    'AIConversationBase',
    'AIConversationCreate',
    'AIConversationRead',
    'AIConversationUpdate',
]
