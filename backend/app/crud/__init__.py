from app.crud.base import CRUDBase
from app.crud.user import CRUDUser, user as user_crud
from app.crud.student_profile import CRUDStudentProfile, student_profile as student_profile_crud
from app.crud.assessment import CRUDAssessment, assessment as assessment_crud
from app.crud.assessment_answer import CRUDAssessmentAnswer, assessment_answer as assessment_answer_crud
from app.crud.assessment_question import CRUDAssessmentQuestion, assessment_question as assessment_question_crud
from app.crud.assessment_result import CRUDAssessmentResult, assessment_result as assessment_result_crud
from app.crud.company import CRUDCompany, company as company_crud
from app.crud.company_interview_pattern import CRUDCompanyInterviewPattern, company_interview_pattern as company_interview_pattern_crud
from app.crud.interview_answer import CRUDInterviewAnswer, interview_answer as interview_answer_crud
from app.crud.interview_feedback import CRUDInterviewFeedback, interview_feedback as interview_feedback_crud
from app.crud.interview_question import CRUDInterviewQuestion, interview_question as interview_question_crud
from app.crud.interview_round import CRUDInterviewRound, interview_round as interview_round_crud
from app.crud.interview_session import CRUDInterviewSession, interview_session as interview_session_crud
from app.crud.question_bank import CRUDQuestionBank, question_bank as question_bank_crud
from app.crud.resume import CRUDResume, resume as resume_crud
from app.crud.resume_analysis import CRUDResumeAnalysis, resume_analysis as resume_analysis_crud
from app.crud.roadmap import CRUDRoadmap, roadmap as roadmap_crud
from app.crud.roadmap_task import CRUDRoadmapTask, roadmap_task as roadmap_task_crud
from app.crud.skill import CRUDSkill, skill as skill_crud
from app.crud.skill_gap import CRUDSkillGap, skill_gap as skill_gap_crud
from app.crud.progress import CRUDProgress, progress as progress_crud
from app.crud.ai_conversation import CRUDAIConversation, ai_conversation as ai_conversation_crud

__all__ = [
    'CRUDBase',
    'CRUDUser',
    'CRUDStudentProfile',
    'CRUDAssessment',
    'CRUDAssessmentQuestion',
    'CRUDAssessmentAnswer',
    'CRUDAssessmentResult',
    'CRUDCompany',
    'CRUDCompanyInterviewPattern',
    'CRUDInterviewSession',
    'CRUDInterviewRound',
    'CRUDInterviewQuestion',
    'CRUDInterviewAnswer',
    'CRUDInterviewFeedback',
    'CRUDQuestionBank',
    'CRUDResume',
    'CRUDResumeAnalysis',
    'CRUDRoadmap',
    'CRUDRoadmapTask',
    'CRUDSkill',
    'CRUDSkillGap',
    'CRUDProgress',
    'CRUDAIConversation',
    'user_crud',
    'student_profile_crud',
    'assessment_crud',
    'assessment_question_crud',
    'assessment_answer_crud',
    'assessment_result_crud',
    'company_crud',
    'interview_session_crud',
    'interview_question_crud',
    'interview_answer_crud',
    'interview_feedback_crud',
    'question_bank_crud',
    'resume_crud',
    'resume_analysis_crud',
    'roadmap_crud',
    'roadmap_task_crud',
    'skill_crud',
    'skill_gap_crud',
    'progress_crud',
    'ai_conversation_crud',
]
