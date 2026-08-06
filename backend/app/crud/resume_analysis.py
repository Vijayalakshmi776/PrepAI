from app.crud.base import CRUDBase
from app.models.resume_analysis import ResumeAnalysis
from app.schemas.resume_analysis import ResumeAnalysisCreate, ResumeAnalysisUpdate


class CRUDResumeAnalysis(CRUDBase[ResumeAnalysis, ResumeAnalysisCreate, ResumeAnalysisUpdate]):
    pass


resume_analysis = CRUDResumeAnalysis(ResumeAnalysis)
