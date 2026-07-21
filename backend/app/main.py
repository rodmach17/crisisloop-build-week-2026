import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAIError

from backend.app.coach.service import generate_adaptive_debrief
from backend.app.engine.interventions import apply_clinical_action
from backend.app.engine.progression import advance_patient_state
from backend.app.engine.scenario import create_initial_patient_state
from backend.app.engine.session import (
    advance_session,
    apply_action_to_session,
    create_replay_session,
    create_simulation_session,
)
from backend.app.schemas.actions import ApplyActionRequest, ActionResult
from backend.app.schemas.comparison import SessionComparison
from backend.app.schemas.coach import (
    CoachDebriefRequest,
    CoachDebriefResponse,
)
from backend.app.schemas.patient import PatientState
from backend.app.schemas.session_api import (
    AdvanceSessionRequest,
    ApplySessionActionRequest,
    CompareSessionsRequest,
    ReplaySessionRequest,
    SessionScoreResponse,
)
from backend.app.schemas.simulation import (
    AdvanceScenarioRequest,
    AdvanceScenarioResponse,
)
from backend.app.schemas.timeline import SimulationSession
from backend.app.scoring.evaluator import evaluate_session
from backend.app.scoring.comparison import compare_sessions

app = FastAPI(
    title="CrisisLoop API",
    version="0.1.0",
    description="Backend for the CrisisLoop adaptive clinical crisis simulator.",
)

DEFAULT_ALLOWED_ORIGINS = (
    "http://127.0.0.1:5173,"
    "http://localhost:5173"
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CRISISLOOP_ALLOWED_ORIGINS",
        DEFAULT_ALLOWED_ORIGINS,
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": "CrisisLoop API",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }


@app.get("/scenario/initial", response_model=PatientState)
async def get_initial_scenario() -> PatientState:
    return create_initial_patient_state()


@app.post("/scenario/advance", response_model=AdvanceScenarioResponse)
async def advance_scenario(
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
async def apply_action(
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
async def create_session() -> SimulationSession:
    return create_simulation_session()


@app.post("/session/advance", response_model=SimulationSession)
async def advance_existing_session(
    request: AdvanceSessionRequest,
) -> SimulationSession:
    return advance_session(
        session=request.session,
        seconds=request.seconds,
    )


@app.post("/session/action", response_model=SimulationSession)
async def apply_session_action(
    request: ApplySessionActionRequest,
) -> SimulationSession:
    return apply_action_to_session(
        session=request.session,
        action=request.action,
    )


@app.post("/session/score", response_model=SessionScoreResponse)
async def score_session(
    session: SimulationSession,
) -> SessionScoreResponse:
    return SessionScoreResponse(
        session=session,
        score=evaluate_session(session),
    )


@app.post("/coach/debrief", response_model=CoachDebriefResponse)
async def create_adaptive_debrief(
    request: CoachDebriefRequest,
) -> CoachDebriefResponse:
    score = evaluate_session(request.session)

    try:
        return await generate_adaptive_debrief(
            session=request.session,
            score=score,
            language=request.language,
        )
    except (OpenAIError, RuntimeError) as error:
        raise HTTPException(
            status_code=503,
            detail="Adaptive coaching is temporarily unavailable.",
        ) from error


@app.post("/session/replay", response_model=SimulationSession)
async def create_replay(
    request: ReplaySessionRequest,
) -> SimulationSession:
    try:
        return create_replay_session(
            source_session=request.session,
            replay_from_seconds=request.replay_from_seconds,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.post("/session/compare", response_model=SessionComparison)
async def compare_simulation_sessions(
    request: CompareSessionsRequest,
) -> SessionComparison:
    try:
        return compare_sessions(
            initial_session=request.initial_session,
            replay_session=request.replay_session,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
