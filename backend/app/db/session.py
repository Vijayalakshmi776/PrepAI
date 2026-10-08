from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

from sqlalchemy import text

engine = create_engine(settings.DATABASE_URL, future=True, pool_pre_ping=True)

# Ensure new columns exist on startup
try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE student_profiles ADD COLUMN IF NOT EXISTS interview_difficulty VARCHAR(64) DEFAULT 'Medium';"))
        conn.execute(text("ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS role VARCHAR(128) DEFAULT 'Software Engineer';"))
        conn.execute(text("ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS difficulty VARCHAR(64) DEFAULT 'Medium';"))
        conn.commit()
except Exception as e:
    pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
