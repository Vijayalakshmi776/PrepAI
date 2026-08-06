from sqlalchemy.orm import Session

from app.crud.company import company as company_crud
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    def get(self, db: Session, id: str) -> Company | None:
        return company_crud.get(db, id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[Company]:
        return company_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: CompanyCreate) -> Company:
        return company_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: Company, obj_in: CompanyUpdate) -> Company:
        return company_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> Company | None:
        return company_crud.remove(db, id)


company_service = CompanyService()
