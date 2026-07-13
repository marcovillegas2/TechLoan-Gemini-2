import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from datetime import date
from main import app
from database import Base, get_db
import app.controllers.dashboard_controller as dashboard_controller

# Importar modelos explícitamente para que create_all los detecte
from app.models.equipment import Equipment
from app.models.borrower import Borrower
from app.models.loan import Loan

from app.controllers.equipment_controller import router

# Montar el router en la app temporalmente para los tests (sin modificar main.py)
app.include_router(router)

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
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
    # Limpiar y recrear tablas antes de cada test para asegurar aislamiento
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_t1_registrar_equipo_valido():
    response = client.post("/equipment", json={
        "code": "EQ-001",
        "name": "Laptop Dell X1",
        "category": "Laptops",
        "description": "Laptop de uso general",
        "status": "DISPONIBLE"
    })
    assert response.status_code == 201
    assert response.json()["code"] == "EQ-001"


def test_t2_registrar_equipo_duplicado():
    client.post("/equipment", json={
        "code": "EQ-DUP", "name": "Laptop A", "category": "Laptops", "status": "DISPONIBLE"
    })
    response = client.post("/equipment", json={
        "code": "EQ-DUP", "name": "Laptop B", "category": "Laptops", "status": "DISPONIBLE"
    })
    assert response.status_code == 409


def test_t3_registrar_equipo_sin_nombre():
    response = client.post("/equipment", json={
        "code": "EQ-003",
        "name": "",
        "category": "Laptops",
        "status": "DISPONIBLE"
    })
    assert response.status_code == 422


def test_t4_registrar_equipo_estado_no_permitido():
    response = client.post("/equipment", json={
        "code": "EQ-004",
        "name": "Monitor Samsung",
        "category": "Perifericos",
        "status": "INVALID_STATUS"
    })
    assert response.status_code == 422


def test_t5_actualizar_equipo_valido():
    create_resp = client.post("/equipment", json={
        "code": "EQ-005", "name": "Teclado", "category": "Accesorios", "status": "DISPONIBLE"
    })
    eq_id = create_resp.json()["id"]

    update_resp = client.put(f"/equipment/{eq_id}", json={
        "code": "EQ-005-MOD",
        "name": "Teclado Mecánico",
        "category": "Accesorios",
        "status": "PRESTADO"
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Teclado Mecánico"
    assert update_resp.json()["status"] == "PRESTADO"


def test_t6_eliminar_equipo_sin_prestamos_activos():
    create_resp = client.post("/equipment", json={
        "code": "EQ-006", "name": "Mouse", "category": "Accesorios", "status": "DISPONIBLE"
    })
    eq_id = create_resp.json()["id"]

    del_resp = client.delete(f"/equipment/{eq_id}")
    assert del_resp.status_code == 200

    get_resp = client.get(f"/equipment/{eq_id}")
    assert get_resp.status_code == 404


def test_t7_eliminar_equipo_con_prestamos_activos():
    # 1. Crear equipo
    create_resp = client.post("/equipment", json={
        "code": "EQ-007", "name": "Proyector", "category": "Audiovisual", "status": "PRESTADO"
    })
    eq_id = create_resp.json()["id"]

    # 2. Inyectar Borrower y Loan activo directamente en DB (simulando estado interno del sistema)
    db = TestingSessionLocal()
    borrower = Borrower(dni="12345678", full_name="Ana Test", email="ana@test.com", phone="555", department="IT")
    db.add(borrower)
    db.commit()

    loan = Loan(
        equipment_id=eq_id,
        borrower_id=borrower.id,
        loan_date=date.today(),
        due_date=date.today(),
        return_date=None,
        status="ACTIVO"
    )
    db.add(loan)
    db.commit()
    db.close()

    # 3. Intentar eliminar
    del_resp = client.delete(f"/equipment/{eq_id}")
    assert del_resp.status_code == 409
    assert "préstamos activos" in del_resp.json()["detail"]