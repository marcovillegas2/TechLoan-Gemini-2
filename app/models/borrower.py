from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class Borrower(Base):
    __tablename__ = "borrower"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(Text, unique=True, nullable=False)
    full_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    department = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    loans = relationship("Loan", back_populates="borrower")