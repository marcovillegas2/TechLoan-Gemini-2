from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BorrowerBase(BaseModel):
    dni: str
    full_name: str
    email: str
    phone: str
    department: str

class BorrowerCreate(BorrowerBase):
    pass

class BorrowerUpdate(BorrowerBase):
    pass

class BorrowerRead(BorrowerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)