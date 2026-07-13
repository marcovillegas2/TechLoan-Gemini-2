from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class EquipmentBase(BaseModel):
    code: str
    name: str
    category: str
    description: Optional[str] = None
    status: Literal["DISPONIBLE", "PRESTADO"]

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(EquipmentBase):
    pass

class EquipmentRead(EquipmentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)