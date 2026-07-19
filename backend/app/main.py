from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.coach.service import generate_adaptive_debrief
from backend.app.engine.interventions import apply_clinical_action
from backend.app.engine.progression import advance_patient_state
from backend.app.engine.scenario import create_initial_patient_state
from backend.app.engine.session import (
    advance_session,
    apply_action_to_session,
    create_simulation_session,
)
from backend.app.schemas.actions import ApplyActionRequest, ActionResult
from backend.app.schemas.coach import (
    CoachDebriefRequest,
    CoachDebriefResponse,
)
from backend.app.schemas.patient import PatientState
from backend.app.schemas.session_api import (
    AdvanceSessionRequest,
    ApplySessionActionRequest,
    SessionScoreResponse,
)
from backend.app.schemas.simulation import (
    AdvanceScenarioRequest,
    AdvanceScenarioResponse,
)
from backend.app.schemas.timeline import SimulationSession
from backend.app.scoring.evaluator import evaluate_session

app = FastAPI(
    title="CrisisLoop API",
    version="0.1.0",
    description="Backend for the CrisisLoop adaptive clinical crisis simulator.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.post("/scenario/advance", response_model=AdvanceScenarioResponse)
def advance_scenario(
    request: AdvanceScenarioRequest,
) -> AdvanceScenarioResponse:
    current_state = advance_patient_state(
        state=request.state,
        seconds=request.seconds,
    )

    return AdvanceScenarioResponse(
        previous_state=request.state,
        current_state=current_state,
    )


@app.post("/scenario/action", response_model=ActionResult)
def apply_action(
    request: ApplyActionRequest,
) -> ActionResult:
    updated_state, description = apply_clinical_action(
        state=request.state,
        action=request.action,
    )

    return ActionResult(
        action=request.action,
        description=description,
        state_before=request.state,
        state_after=updated_state,
    )


@app.post("/session", response_model=SimulationSession)
def create_session() -> SimulationSession:
    return create_simulation_session()


@app.post("/session/advance", response_model=SimulationSession)
def advance_existing_session(
    request: AdvanceSessionRequest,
) -> SimulationSession:
    return advance_session(
        session=request.session,
        seconds=request.seconds,
    )


@app.post("/session/action", response_model=SimulationSession)
def apply_session_action(
    request: ApplySessionActionRequest,
) -> SimulationSession:
    return apply_action_to_session(
        session=request.session,
        action=request.action,
    )


@app.post("/session/score", response_model=SessionScoreResponse)
def score_session(
    session: SimulationSession,
) -> SessionScoreResponse:
    return SessionScoreResponse(
        session=session,
        score=evaluate_session(session),
    )

@app.post("/coach/debrief", response_model=CoachDebriefResponse)
def create_adaptive_debrief(
    request: CoachDebriefRequest,
) -> CoachDebriefResponse:
    score = evaluate_session(request.session)

    return generate_adaptive_debrief(
        session=request.session,
        score=score,
    )

