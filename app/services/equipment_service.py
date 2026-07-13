from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.equipment_repository import EquipmentRepository
from app.schemas.equipment_schema import EquipmentCreate, EquipmentUpdate

repo = EquipmentRepository()

def create_equipment(db: Session, equipment: EquipmentCreate):
    if not equipment.name or not equipment.name.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="El nombre del equipo es obligatorio.")
    if not equipment.category or not equipment.category.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="La categoría del equipo es obligatoria.")
    if equipment.status not in ["DISPONIBLE", "PRESTADO"]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Estado no permitido. Debe ser 'AVAILABLE' o 'LOANED'.")

    existing = repo.get_by_code(db, equipment.code)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El código de equipo ya se encuentra registrado.")

    return repo.create(db, equipment.model_dump())

def get_all_equipment(db: Session):
    return repo.get_all(db)

def get_equipment_by_id(db: Session, equipment_id: int):
    equipment = repo.get_by_id(db, equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado.")
    return equipment

def update_equipment(db: Session, equipment_id: int, equipment: EquipmentUpdate):
    if not equipment.name or not equipment.name.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="El nombre del equipo es obligatorio.")
    if not equipment.category or not equipment.category.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="La categoría del equipo es obligatoria.")
    if equipment.status not in ["DISPONIBLE", "PRESTADO"]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Estado no permitido. Debe ser 'AVAILABLE' o 'LOANED'.")

    db_equipment = repo.get_by_id(db, equipment_id)
    if not db_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado.")

    if equipment.code != db_equipment.code:
        existing = repo.get_by_code(db, equipment.code)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El código de equipo ya se encuentra registrado por otro equipo.")

    return repo.update(db, equipment_id, equipment.model_dump(exclude_unset=True))

def delete_equipment(db: Session, equipment_id: int):
    db_equipment = repo.get_by_id(db, equipment_id)
    if not db_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado.")

    if repo.has_active_loans(db, equipment_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede eliminar el equipo porque tiene préstamos activos.")

    repo.delete(db, equipment_id)
    return {"detail": "Equipo eliminado correctamente."}