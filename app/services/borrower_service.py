from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.borrower_repository import BorrowerRepository
from app.schemas.borrower_schema import BorrowerCreate, BorrowerUpdate

repo = BorrowerRepository()

def create_borrower(db: Session, borrower: BorrowerCreate):
    if not borrower.dni or not borrower.dni.strip() or \
       not borrower.full_name or not borrower.full_name.strip() or \
       not borrower.email or not borrower.email.strip() or \
       not borrower.phone or not borrower.phone.strip() or \
       not borrower.department or not borrower.department.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Todos los campos son obligatorios.")

    if repo.get_by_dni(db, borrower.dni):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El DNI ya se encuentra registrado.")

    return repo.create(db, borrower.model_dump())

def get_all_borrowers(db: Session):
    return repo.get_all(db)

def get_borrower_by_id(db: Session, borrower_id: int):
    borrower = repo.get_by_id(db, borrower_id)
    if not borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitante no encontrado.")
    return borrower

def update_borrower(db: Session, borrower_id: int, borrower: BorrowerUpdate):
    if not borrower.dni or not borrower.dni.strip() or \
       not borrower.full_name or not borrower.full_name.strip() or \
       not borrower.email or not borrower.email.strip() or \
       not borrower.phone or not borrower.phone.strip() or \
       not borrower.department or not borrower.department.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Todos los campos son obligatorios.")

    db_borrower = repo.get_by_id(db, borrower_id)
    if not db_borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitante no encontrado.")

    if db_borrower.dni != borrower.dni:
        if repo.get_by_dni(db, borrower.dni):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El DNI ya se encuentra registrado por otro solicitante.")

    return repo.update(db, borrower_id, borrower.model_dump(exclude_unset=True))