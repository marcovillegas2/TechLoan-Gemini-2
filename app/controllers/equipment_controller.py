from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.schemas.equipment_schema import EquipmentCreate, EquipmentUpdate, EquipmentRead
from app.services import equipment_service

router = APIRouter(prefix="/equipment", tags=["Equipment"])

@router.post("", response_model=EquipmentRead, status_code=status.HTTP_201_CREATED)
def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    return equipment_service.create_equipment(db, equipment)

@router.get("", response_model=List[EquipmentRead], status_code=status.HTTP_200_OK)
def get_all_equipment(db: Session = Depends(get_db)):
    return equipment_service.get_all_equipment(db)

@router.get("/{equipment_id}", response_model=EquipmentRead, status_code=status.HTTP_200_OK)
def get_equipment_by_id(equipment_id: int, db: Session = Depends(get_db)):
    return equipment_service.get_equipment_by_id(db, equipment_id)

@router.put("/{equipment_id}", response_model=EquipmentRead, status_code=status.HTTP_200_OK)
def update_equipment(equipment_id: int, equipment: EquipmentUpdate, db: Session = Depends(get_db)):
    return equipment_service.update_equipment(db, equipment_id, equipment)

@router.delete("/{equipment_id}", status_code=status.HTTP_200_OK)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    return equipment_service.delete_equipment(db, equipment_id)