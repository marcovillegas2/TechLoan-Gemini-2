from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.schemas.loan_schema import LoanCreate, LoanRead
from app.schemas.equipment_schema import EquipmentRead
from app.services import loan_service

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.get("/available-equipment", response_model=List[EquipmentRead], status_code=status.HTTP_200_OK)
def get_available_equipment(db: Session = Depends(get_db)):
    return loan_service.get_available_equipment(db)

@router.post("", response_model=LoanRead, status_code=status.HTTP_201_CREATED)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    return loan_service.create_loan(db, loan)

@router.get("", response_model=List[LoanRead], status_code=status.HTTP_200_OK)
def get_all_loans(db: Session = Depends(get_db)):
    return loan_service.get_all_loans(db)

@router.get("/{loan_id}", response_model=LoanRead, status_code=status.HTTP_200_OK)
def get_loan_by_id(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loan_by_id(db, loan_id)

@router.post("/{loan_id}/return", response_model=LoanRead, status_code=status.HTTP_200_OK)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.return_loan(db, loan_id)