from sqlalchemy.orm import Session

from app.crud.user import user as user_crud
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def get(self, db: Session, id: str) -> User | None:
        return user_crud.get(db, id)

    def get_by_email(self, db: Session, email: str) -> User | None:
        return user_crud.get_by_email(db, email)

    def create(self, db: Session, obj_in: UserCreate) -> User:
        return user_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        return user_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> User | None:
        return user_crud.remove(db, id)


user_service = UserService()
