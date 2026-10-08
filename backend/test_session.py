from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.api.api_v1.endpoints.interview import start_interview_session, StartSessionRequest
from app.models.user import User
import json

def test():
    db = SessionLocal()
    try:
        # Get any user or create one
        user = db.query(User).first()
        if not user:
            user = User(email="test@example.com", hashed_password="pw", full_name="Test User")
            db.add(user)
            db.commit()
            db.refresh(user)
        
        req = StartSessionRequest(
            company_name="Startup",
            role="Software Engineer",
            difficulty="Medium"
        )
        
        # Test creating a session
        res = start_interview_session(payload=req, db=db, current_user=user)
        
        print(f"Total questions: {len(res['questions'])}")
        print(f"Round ID: {res['current_round']}")
        for q in res['questions']:
            print(f"Q: {q['prompt'][:30]}... type: {q['question_type']} options: {q['options']}")
            
    finally:
        db.close()

if __name__ == "__main__":
    test()
