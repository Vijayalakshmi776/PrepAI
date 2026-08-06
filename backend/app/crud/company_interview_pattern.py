from app.crud.base import CRUDBase
from app.models.company_interview_pattern import CompanyInterviewPattern
from app.schemas.company_interview_pattern import CompanyInterviewPatternCreate, CompanyInterviewPatternUpdate


class CRUDCompanyInterviewPattern(CRUDBase[CompanyInterviewPattern, CompanyInterviewPatternCreate, CompanyInterviewPatternUpdate]):
    pass


company_interview_pattern = CRUDCompanyInterviewPattern(CompanyInterviewPattern)
