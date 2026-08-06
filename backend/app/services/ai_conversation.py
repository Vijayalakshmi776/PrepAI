from sqlalchemy.orm import Session

from app.crud.ai_conversation import ai_conversation as ai_conversation_crud
from app.models.ai_conversation import AIConversation
from app.schemas.ai_conversation import AIConversationCreate, AIConversationUpdate


class AIConversationService:
    def get(self, db: Session, id: str) -> AIConversation | None:
        return ai_conversation_crud.get(db, id)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[AIConversation]:
        return ai_conversation_crud.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, obj_in: AIConversationCreate) -> AIConversation:
        return ai_conversation_crud.create(db, obj_in)

    def update(self, db: Session, db_obj: AIConversation, obj_in: AIConversationUpdate) -> AIConversation:
        return ai_conversation_crud.update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str) -> AIConversation | None:
        return ai_conversation_crud.remove(db, id)


ai_conversation_service = AIConversationService()
