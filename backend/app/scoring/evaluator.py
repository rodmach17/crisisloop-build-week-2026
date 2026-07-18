from backend.app.schemas.actions import ClinicalActionType
from backend.app.schemas.scoring import CriticalDecision, SessionScore
from backend.app.schemas.timeline import SimulationSession


def _first_action_time(
    session: SimulationSession,
    action: ClinicalActionType,
) -> int | None:
    for event in session.timeline:
        if event.action == action:
            return event.elapsed_seconds
    return None


def evaluate_session(session: SimulationSession) -> SessionScore:
    help_time = _first_action_time(
        session,
        ClinicalActionType.CALL_FOR_HELP,
    )
    fluids_time = _first_action_time(
        session,
        ClinicalActionType.START_IV_FLUIDS,
    )
    transfusion_time = _first_action_time(
        session,
        ClinicalActionType.ACTIVATE_TRANSFUSION,
    )

    omissions: list[ClinicalActionType] = []

    if help_time is None:
        omissions.append(ClinicalActionType.CALL_FOR_HELP)

    if fluids_time is None:
        omissions.append(ClinicalActionType.START_IV_FLUIDS)

    if transfusion_time is None:
        omissions.append(ClinicalActionType.ACTIVATE_TRANSFUSION)

    recognition_time = help_time
    if recognition_time is None:
        recognition_score = 0
    elif recognition_time <= 60:
        recognition_score = 30
    elif recognition_time <= 120:
        recognition_score = 20
    elif recognition_time <= 180:
        recognition_score = 10
    else:
        recognition_score = 5

    intervention_score = 0

    if fluids_time is not None:
        if fluids_time <= 90:
            intervention_score += 15
        elif fluids_time <= 180:
            intervention_score += 10
        else:
            intervention_score += 5

    if transfusion_time is not None:
        if transfusion_time <= 120:
            intervention_score += 25
        elif transfusion_time <= 210:
            intervention_score += 15
        else:
            intervention_score += 5

    final_harm = session.current_state.cumulative_harm
    safety_score = max(0, 30 - round(final_harm * 0.3))

    critical_decision: CriticalDecision | None = None

    if help_time is None or help_time > 120:
        critical_decision = CriticalDecision(
            elapsed_seconds=120,
            reason="Delayed recognition and escalation of hemorrhagic shock.",
            missed_action=ClinicalActionType.CALL_FOR_HELP,
        )
    elif transfusion_time is None or transfusion_time > 210:
        critical_decision = CriticalDecision(
            elapsed_seconds=150,
            reason="Definitive hemorrhage control and transfusion were delayed.",
            missed_action=ClinicalActionType.ACTIVATE_TRANSFUSION,
        )
    elif fluids_time is None or fluids_time > 180:
        critical_decision = CriticalDecision(
            elapsed_seconds=90,
            reason="Initial resuscitation was delayed.",
            missed_action=ClinicalActionType.START_IV_FLUIDS,
        )

    total_score = min(
        100,
        recognition_score + intervention_score + safety_score,
    )

    return SessionScore(
        total_score=total_score,
        recognition_score=recognition_score,
        intervention_score=intervention_score,
        safety_score=safety_score,
        final_harm=final_harm,
        critical_omissions=omissions,
        critical_decision=critical_decision,
    )
