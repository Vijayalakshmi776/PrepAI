from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        obj_data = obj_in.model_dump(exclude_none=True)
        password = obj_data.pop('password', None)
        if password is None:
            raise ValueError('Password is required')
        db_obj = self.model(**obj_data, hashed_password=get_password_hash(password))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        obj_data = obj_in.model_dump(exclude_none=True)
        if 'password' in obj_data:
            password = obj_data.pop('password')
            if password is not None:
                obj_data['hashed_password'] = get_password_hash(password)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
