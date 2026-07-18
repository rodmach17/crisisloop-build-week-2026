from backend.app.engine.interventions import apply_clinical_action
from backend.app.engine.progression import advance_patient_state
from backend.app.engine.scenario import create_initial_patient_state
from backend.app.schemas.actions import ClinicalActionType


def create_decompensated_state():
    initial = create_initial_patient_state()
    return advance_patient_state(initial, 180)


def test_start_iv_fluids_improves_hemodynamics() -> None:
    state = create_decompensated_state()

    updated, description = apply_clinical_action(
        state,
        ClinicalActionType.START_IV_FLUIDS,
    )

    assert updated.vital_signs.systolic_bp > state.vital_signs.systolic_bp
    assert updated.vital_signs.heart_rate < state.vital_signs.heart_rate
    assert updated.cumulative_harm < state.cumulative_harm
    assert "Temporary hemodynamic support" in description


def test_activate_transfusion_has_stronger_effect_than_fluids() -> None:
    state = create_decompensated_state()

    fluids_state, _ = apply_clinical_action(
        state,
        ClinicalActionType.START_IV_FLUIDS,
    )
    transfusion_state, _ = apply_clinical_action(
        state,
        ClinicalActionType.ACTIVATE_TRANSFUSION,
    )

    fluids_bp_gain = (
        fluids_state.vital_signs.systolic_bp
        - state.vital_signs.systolic_bp
    )
    transfusion_bp_gain = (
        transfusion_state.vital_signs.systolic_bp
        - state.vital_signs.systolic_bp
    )

    assert transfusion_bp_gain > fluids_bp_gain
    assert (
        transfusion_state.cumulative_harm
        < fluids_state.cumulative_harm
    )
    assert (
        transfusion_state.estimated_blood_loss_ml
        < state.estimated_blood_loss_ml
    )


def test_call_for_help_reduces_harm_without_changing_vitals() -> None:
    state = create_decompensated_state()

    updated, _ = apply_clinical_action(
        state,
        ClinicalActionType.CALL_FOR_HELP,
    )

    assert updated.cumulative_harm < state.cumulative_harm
    assert updated.vital_signs == state.vital_signs
