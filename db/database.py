
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
DATA_BASE_URL = "sqlite:///./images.db"
engine = create_engine(DATA_BASE_URL, connect_args={"check_same_thread": False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
