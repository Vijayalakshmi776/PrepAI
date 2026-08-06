from app.services.user import UserService, user_service
from app.services.student_profile import StudentProfileService, student_profile_service
from app.services.company import CompanyService, company_service
from app.services.question_bank import QuestionBankService, question_bank_service
from app.services.resume import ResumeService, resume_service
from app.services.resume_analysis import ResumeAnalysisService, resume_analysis_service
from app.services.progress import ProgressService, progress_service
from app.services.ai_conversation import AIConversationService, ai_conversation_service

__all__ = [
    'UserService',
    'user_service',
    'StudentProfileService',
    'student_profile_service',
    'CompanyService',
    'company_service',
    'QuestionBankService',
    'question_bank_service',
    'ResumeService',
    'resume_service',
    'ResumeAnalysisService',
    'resume_analysis_service',
    'ProgressService',
    'progress_service',
    'AIConversationService',
    'ai_conversation_service',
]
