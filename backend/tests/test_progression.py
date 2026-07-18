from backend.app.engine.progression import advance_patient_state
from backend.app.engine.scenario import create_initial_patient_state
from backend.app.schemas.patient import ClinicalPhase


def test_patient_deteriorates_after_180_seconds_without_intervention() -> None:
    initial = create_initial_patient_state()

    current = advance_patient_state(initial, 180)

    assert current.elapsed_seconds == 180
    assert current.phase == ClinicalPhase.DECOMPENSATED
    assert current.vital_signs.heart_rate > initial.vital_signs.heart_rate
    assert current.vital_signs.systolic_bp < initial.vital_signs.systolic_bp
    assert current.estimated_blood_loss_ml > initial.estimated_blood_loss_ml
    assert current.cumulative_harm > initial.cumulative_harm


def test_zero_seconds_returns_equivalent_state() -> None:
    initial = create_initial_patient_state()

    current = advance_patient_state(initial, 0)

    assert current == initial
    assert current is not initial
