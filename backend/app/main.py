from fastapi import FastAPI

from backend.app.engine.scenario import create_initial_patient_state
from backend.app.schemas.patient import PatientState

app = FastAPI(
    title="CrisisLoop API",
    version="0.1.0",
    description="Backend for the CrisisLoop adaptive clinical crisis simulator.",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "CrisisLoop API",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }


@app.get("/scenario/initial", response_model=PatientState)
def get_initial_scenario() -> PatientState:
    return create_initial_patient_state()
