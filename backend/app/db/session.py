import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

def init_engine():
    db_url = settings.DATABASE_URL
    try:
        eng = create_engine(db_url, future=True, pool_pre_ping=True)
        with eng.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"Connected successfully to primary database ({db_url.split('@')[-1] if '@' in db_url else db_url})")
        return eng
    except Exception as e:
        logger.warning(f"Primary database connection failed: {e}. Falling back to SQLite database.")
        sqlite_url = "sqlite:///./prepai.db"
        eng = create_engine(sqlite_url, connect_args={"check_same_thread": False}, future=True)
        try:
            import app.models  # Ensure all SQLAlchemy models are registered
            from app.db.base import Base
            Base.metadata.create_all(bind=eng)
            logger.info("SQLite database fallback initialized successfully with all tables created.")
        except Exception as create_err:
            logger.error(f"SQLite fallback table creation error: {create_err}")
        return eng

engine = init_engine()

# Ensure migration columns exist on startup if using PostgreSQL
try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE student_profiles ADD COLUMN IF NOT EXISTS interview_difficulty VARCHAR(64) DEFAULT 'Medium';"))
        conn.execute(text("ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS role VARCHAR(128) DEFAULT 'Software Engineer';"))
        conn.execute(text("ALTER TABLE interview_sessions ADD COLUMN IF NOT EXISTS difficulty VARCHAR(64) DEFAULT 'Medium';"))
        conn.commit()
except Exception:
    pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
