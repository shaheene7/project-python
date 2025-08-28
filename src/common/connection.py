from contextlib import contextmanager
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine(os.getenv("DB_URL"), pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

Base = declarative_base()
