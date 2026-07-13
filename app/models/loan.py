from sqlalchemy import Column, Integer, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class Loan(Base):
    __tablename__ = "loan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("borrower.id"), nullable=False)
    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    equipment = relationship("Equipment", back_populates="loans")
    borrower = relationship("Borrower", back_populates="loans")