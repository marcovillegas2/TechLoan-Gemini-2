from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TechLoan — Sistema Administrativo de Control de Préstamos de Equipos Tecnológicos",
    description="Infraestructura inicial base para el sistema TechLoan.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://127.0.0.1:63342"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Al inicio de tu archivo main.py (después de crear la instancia 'app = FastAPI()'),
# agrega estas líneas para importar y registrar los routers:

from app.controllers.equipment_controller import router as equipment_router
from app.controllers.borrower_controller import router as borrower_router
from app.controllers.loan_controller import router as loan_router
from app.controllers.dashboard_controller import router as dashboard_router

app.include_router(equipment_router)
app.include_router(borrower_router)
app.include_router(loan_router)
app.include_router(dashboard_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "TechLoan API inicializada correctamente y lista para la siguiente fase."
    }
