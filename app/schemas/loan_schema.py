from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import date, datetime

class LoanBase(BaseModel):
    equipment_id: int
    borrower_id: int
    loan_date: date
    due_date: date
    return_date: Optional[date] = None
    status: Literal["ACTIVO", "DEVUELTO", "VENCIDO"]

class LoanCreate(LoanBase):
    pass

class LoanUpdate(LoanBase):
    pass

class LoanRead(LoanBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)