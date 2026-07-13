import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Asegurar la existencia del directorio donde residirá la base de datos SQLite
os.makedirs("database", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./database/techloan.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.models.equipment import Equipment
from app.models.borrower import Borrower
from app.models.loan import Loan

Base.metadata.create_all(bind=engine)