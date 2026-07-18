from uuid import uuid4

from backend.app.engine.interventions import apply_clinical_action
from backend.app.engine.progression import advance_patient_state
from backend.app.engine.scenario import create_initial_patient_state
from backend.app.schemas.actions import ClinicalActionType
from backend.app.schemas.timeline import SimulationSession, TimelineEvent


def create_simulation_session() -> SimulationSession:
    initial = create_initial_patient_state()

    return SimulationSession(
        session_id=str(uuid4()),
        initial_state=initial,
        current_state=initial.model_copy(deep=True),
        timeline=[],
    )


def advance_session(
    session: SimulationSession,
    seconds: int,
) -> SimulationSession:
    previous = session.current_state.model_copy(deep=True)
    current = advance_patient_state(previous, seconds)

    event = TimelineEvent(
        elapsed_seconds=current.elapsed_seconds,
        event_type="time_advance",
        description=f"Scenario advanced by {seconds} seconds.",
        state_before=previous,
        state_after=current,
    )

    updated = session.model_copy(deep=True)
    updated.current_state = current
    updated.timeline.append(event)

    return updated


def apply_action_to_session(
    session: SimulationSession,
    action: ClinicalActionType,
) -> SimulationSession:
    previous = session.current_state.model_copy(deep=True)
    current, description = apply_clinical_action(previous, action)

    event = TimelineEvent(
        elapsed_seconds=current.elapsed_seconds,
        event_type="clinical_action",
        action=action,
        description=description,
        state_before=previous,
        state_after=current,
    )

    updated = session.model_copy(deep=True)
    updated.current_state = current
    updated.timeline.append(event)

    return updated
