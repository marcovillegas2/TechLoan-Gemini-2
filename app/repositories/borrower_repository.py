from sqlalchemy.orm import Session
from app.models.borrower import Borrower

class BorrowerRepository:
    def create(self, db: Session, borrower_data: dict) -> Borrower:
        db_borrower = Borrower(**borrower_data)
        db.add(db_borrower)
        db.commit()
        db.refresh(db_borrower)
        return db_borrower

    def get_by_id(self, db: Session, borrower_id: int) -> Borrower:
        return db.query(Borrower).filter(Borrower.id == borrower_id).first()

    def get_by_dni(self, db: Session, dni: str) -> Borrower:
        return db.query(Borrower).filter(Borrower.dni == dni).first()

    def get_all(self, db: Session):
        return db.query(Borrower).all()

    def update(self, db: Session, borrower_id: int, borrower_data: dict) -> Borrower:
        db_borrower = self.get_by_id(db, borrower_id)
        if db_borrower:
            for key, value in borrower_data.items():
                setattr(db_borrower, key, value)
            db.commit()
            db.refresh(db_borrower)
        return db_borrower