from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from app.repositories.loan_repository import LoanRepository
from app.repositories.borrower_repository import BorrowerRepository
from app.schemas.loan_schema import LoanCreate

loan_repo = LoanRepository()
borrower_repo = BorrowerRepository()


def create_loan(db: Session, loan: LoanCreate):
    if loan.due_date <= loan.loan_date:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="La fecha límite debe ser posterior a la fecha de préstamo.")

    borrower = borrower_repo.get_by_id(db, loan.borrower_id)
    if not borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitante no encontrado.")

    if not loan_repo.is_equipment_available(db, loan.equipment_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El equipo no existe o no está disponible.")

    loan_data = loan.model_dump()
    loan_data["status"] = "ACTIVO"
    loan_data["return_date"] = None
    return loan_repo.create(db, loan_data)


def get_all_loans(db: Session):
    return loan_repo.get_all(db)


def get_loan_by_id(db: Session, loan_id: int):
    loan = loan_repo.get_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado.")
    return loan


def return_loan(db: Session, loan_id: int):
    loan = loan_repo.get_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado.")

    if loan_repo.is_loan_returned(db, loan_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El préstamo ya fue devuelto.")

    return loan_repo.register_return(db, loan_id, date.today())


def get_available_equipment(db: Session):
    return loan_repo.get_available_equipment(db)