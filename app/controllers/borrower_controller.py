from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.schemas.borrower_schema import BorrowerCreate, BorrowerUpdate, BorrowerRead
from app.services import borrower_service

router = APIRouter(prefix="/borrowers", tags=["Borrowers"])

@router.post("", response_model=BorrowerRead, status_code=status.HTTP_201_CREATED)
def create_borrower(borrower: BorrowerCreate, db: Session = Depends(get_db)):
    return borrower_service.create_borrower(db, borrower)

@router.get("", response_model=List[BorrowerRead], status_code=status.HTTP_200_OK)
def get_all_borrowers(db: Session = Depends(get_db)):
    return borrower_service.get_all_borrowers(db)

@router.get("/{borrower_id}", response_model=BorrowerRead, status_code=status.HTTP_200_OK)
def get_borrower_by_id(borrower_id: int, db: Session = Depends(get_db)):
    return borrower_service.get_borrower_by_id(db, borrower_id)

@router.put("/{borrower_id}", response_model=BorrowerRead, status_code=status.HTTP_200_OK)
def update_borrower(borrower_id: int, borrower: BorrowerUpdate, db: Session = Depends(get_db)):
    return borrower_service.update_borrower(db, borrower_id, borrower)