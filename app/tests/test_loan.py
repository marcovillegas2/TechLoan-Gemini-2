import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
from main import app
from database import Base, get_db
import app.controllers.dashboard_controller as dashboard_controller

from app.models.equipment import Equipment
from app.models.borrower import Borrower
from app.models.loan import Loan
from app.controllers.loan_controller import router as loan_router

app.include_router(loan_router)

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def _setup_data(db):
    eq = Equipment(code="EQ-L1", name="Laptop", category="PC", status="DISPONIBLE")
    b = Borrower(dni="111", full_name="User", email="u@t.com", phone="123", department="IT")
    db.add(eq)
    db.add(b)
    db.commit()
    db.refresh(eq)
    db.refresh(b)
    return eq, b

def test_tl1_registrar_prestamo_valido():
    db = TestingSessionLocal()
    eq, b = _setup_data(db)
    db.close()

    today = date.today()
    due = today + timedelta(days=5)

    response = client.post("/loans", json={
        "equipment_id": eq.id, "borrower_id": b.id,
        "loan_date": str(today), "due_date": str(due),
        "return_date": None, "status": "ACTIVO"
    })
    assert response.status_code == 201
    assert response.json()["status"] == "ACTIVO"

def test_tl2_registrar_prestamo_equipo_no_disponible():
    db = TestingSessionLocal()
    eq = Equipment(code="EQ-L2", name="PC", category="PC", status="PRESTADO")
    b = Borrower(dni="222", full_name="User 2", email="u2@t.com", phone="123", department="IT")
    db.add(eq)
    db.add(b)
    db.commit()
    eq_id, b_id = eq.id, b.id
    db.close()

    today = date.today()
    due = today + timedelta(days=5)

    response = client.post("/loans", json={
        "equipment_id": eq_id, "borrower_id": b_id,
        "loan_date": str(today), "due_date": str(due),
        "return_date": None, "status": "ACTIVO"
    })
    assert response.status_code == 409

def test_tl3_registrar_prestamo_borrower_inexistente():
    db = TestingSessionLocal()
    eq = Equipment(code="EQ-L3", name="Mouse", category="Acc", status="DISPONIBLE")
    db.add(eq)
    db.commit()
    eq_id = eq.id
    db.close()

    today = date.today()
    due = today + timedelta(days=5)

    response = client.post("/loans", json={
        "equipment_id": eq_id, "borrower_id": 9999,
        "loan_date": str(today), "due_date": str(due),
        "return_date": None, "status": "ACTIVO"
    })
    assert response.status_code == 404

def test_tl4_registrar_prestamo_fecha_invalida():
    db = TestingSessionLocal()
    eq, b = _setup_data(db)
    db.close()

    today = date.today()
    due = today - timedelta(days=1)

    response = client.post("/loans", json={
        "equipment_id": eq.id, "borrower_id": b.id,
        "loan_date": str(today), "due_date": str(due),
        "return_date": None, "status": "ACTIVO"
    })
    assert response.status_code == 422

def test_tl5_registrar_devolucion_valida():
    db = TestingSessionLocal()
    eq, b = _setup_data(db)
    loan = Loan(equipment_id=eq.id, borrower_id=b.id, loan_date=date.today(), due_date=date.today() + timedelta(days=5), status="ACTIVO")
    eq.status = "PRESTADO"
    db.add(loan)
    db.commit()
    db.refresh(loan)
    loan_id = loan.id
    db.close()

    response = client.post(f"/loans/{loan_id}/return")
    assert response.status_code == 200
    assert response.json()["status"] == "DEVUELTO"
    assert response.json()["return_date"] is not None

def test_tl6_registrar_devolucion_ya_devuelto():
    db = TestingSessionLocal()
    eq, b = _setup_data(db)
    loan = Loan(equipment_id=eq.id, borrower_id=b.id, loan_date=date.today(), due_date=date.today() + timedelta(days=5), status="DEVUELTO", return_date=date.today())
    db.add(loan)
    db.commit()
    loan_id = loan.id
    db.close()

    response = client.post(f"/loans/{loan_id}/return")
    assert response.status_code == 409

def test_tl7_listar_equipos_disponibles():
    db = TestingSessionLocal()
    eq1 = Equipment(code="A1", name="Eq 1", category="Cat", status="DISPONIBLE")
    eq2 = Equipment(code="A2", name="Eq 2", category="Cat", status="PRESTADO")
    db.add_all([eq1, eq2])
    db.commit()
    db.close()

    response = client.get("/loans/available-equipment")
    assert response.status_code == 200
    data = response.json()
    assert len([e for e in data if e["code"] == "A1"]) == 1
    assert len([e for e in data if e["code"] == "A2"]) == 0