from sqlalchemy.orm import Session
from app.models.equipment import Equipment
from app.models.loan import Loan

class EquipmentRepository:
    def create(self, db: Session, equipment_data: dict) -> Equipment:
        db_equipment = Equipment(**equipment_data)
        db.add(db_equipment)
        db.commit()
        db.refresh(db_equipment)
        return db_equipment

    def get_by_id(self, db: Session, equipment_id: int) -> Equipment:
        return db.query(Equipment).filter(Equipment.id == equipment_id).first()

    def get_by_code(self, db: Session, code: str) -> Equipment:
        return db.query(Equipment).filter(Equipment.code == code).first()

    def get_all(self, db: Session):
        return db.query(Equipment).all()

    def update(self, db: Session, equipment_id: int, equipment_data: dict) -> Equipment:
        db_equipment = self.get_by_id(db, equipment_id)
        if db_equipment:
            for key, value in equipment_data.items():
                setattr(db_equipment, key, value)
            db.commit()
            db.refresh(db_equipment)
        return db_equipment

    def delete(self, db: Session, equipment_id: int) -> bool:
        db_equipment = self.get_by_id(db, equipment_id)
        if db_equipment:
            db.delete(db_equipment)
            db.commit()
            return True
        return False

    def has_active_loans(self, db: Session, equipment_id: int) -> bool:
        return (
                db.query(Loan)
                .filter(
                    Loan.equipment_id == equipment_id,
                    Loan.return_date.is_(None)
                )
                .count()
                > 0
        )