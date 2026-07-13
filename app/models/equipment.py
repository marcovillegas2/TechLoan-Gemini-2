from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Text, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    loans = relationship("Loan", back_populates="equipment")