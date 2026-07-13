from sqlalchemy.orm import Session
from app.models.loan import Loan
from app.models.equipment import Equipment
from datetime import date


class LoanRepository:
    def create(self, db: Session, loan_data: dict) -> Loan:
        db_loan = Loan(**loan_data)
        db.add(db_loan)

        equipment = db.query(Equipment).filter(Equipment.id == loan_data["equipment_id"]).first()
        if equipment:
            equipment.status = "PRESTADO"

        db.commit()
        db.refresh(db_loan)
        return db_loan

    def get_by_id(self, db: Session, loan_id: int) -> Loan:
        return db.query(Loan).filter(Loan.id == loan_id).first()

    def get_all(self, db: Session):
        return db.query(Loan).all()

    def register_return(self, db: Session, loan_id: int, return_date: date) -> Loan:
        db_loan = self.get_by_id(db, loan_id)
        if db_loan:
            db_loan.status = "DEVUELTO"
            db_loan.return_date = return_date
            equipment = db.query(Equipment).filter(Equipment.id == db_loan.equipment_id).first()
            if equipment:
                equipment.status = "DISPONIBLE"
            db.commit()
            db.refresh(db_loan)
        return db_loan

    def is_equipment_available(self, db: Session, equipment_id: int) -> bool:
        equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
        return equipment is not None and equipment.status == "DISPONIBLE"

    def get_available_equipment(self, db: Session):
        return db.query(Equipment).filter(Equipment.status == "DISPONIBLE").all()

    def is_loan_returned(self, db: Session, loan_id: int) -> bool:
        loan = self.get_by_id(db, loan_id)
        return loan is not None and loan.status == "DEVUELTO"