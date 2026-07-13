import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
import app.controllers.dashboard_controller as dashboard_controller

from app.models.borrower import Borrower
from app.controllers.borrower_controller import router

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
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_tb1_registrar_solicitante_valido():
    response = client.post("/borrowers", json={
        "dni": "12345678", "full_name": "Juan Perez",
        "email": "juan@test.com", "phone": "5551234", "department": "IT"
    })
    assert response.status_code == 201
    assert response.json()["dni"] == "12345678"


def test_tb2_registrar_solicitante_dni_duplicado():
    client.post("/borrowers", json={
        "dni": "87654321", "full_name": "Ana",
        "email": "ana@test.com", "phone": "555", "department": "HR"
    })
    response = client.post("/borrowers", json={
        "dni": "87654321", "full_name": "Pedro",
        "email": "pedro@test.com", "phone": "666", "department": "IT"
    })
    assert response.status_code == 409


def test_tb3_registrar_solicitante_campo_faltante():
    response = client.post("/borrowers", json={
        "dni": "11223344", "full_name": "",
        "email": "test@test.com", "phone": "123", "department": "IT"
    })
    assert response.status_code == 422

    response2 = client.post("/borrowers", json={
        "dni": "11223344", "email": "test@test.com"
    })
    assert response2.status_code == 422


def test_tb4_actualizar_solicitante_valido():
    create_resp = client.post("/borrowers", json={
        "dni": "44444444", "full_name": "Luis",
        "email": "luis@test.com", "phone": "111", "department": "Ventas"
    })
    b_id = create_resp.json()["id"]

    update_resp = client.put(f"/borrowers/{b_id}", json={
        "dni": "44444444", "full_name": "Luis Modificado",
        "email": "luis.mod@test.com", "phone": "222", "department": "Marketing"
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["full_name"] == "Luis Modificado"