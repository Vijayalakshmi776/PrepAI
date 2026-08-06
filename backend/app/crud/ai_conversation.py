from app.crud.base import CRUDBase
from app.models.ai_conversation import AIConversation
from app.schemas.ai_conversation import AIConversationCreate, AIConversationUpdate


class CRUDAIConversation(CRUDBase[AIConversation, AIConversationCreate, AIConversationUpdate]):
    pass


ai_conversation = CRUDAIConversation(AIConversation)
