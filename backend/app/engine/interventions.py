from backend.app.schemas.actions import ClinicalActionType
from backend.app.schemas.patient import PatientState


def apply_clinical_action(
    state: PatientState,
    action: ClinicalActionType,
) -> tuple[PatientState, str]:
    updated = state.model_copy(deep=True)

    if action == ClinicalActionType.CALL_FOR_HELP:
        updated.cumulative_harm = max(0, updated.cumulative_harm - 3)
        description = "Urgent assistance requested. Escalation delay reduced."

    elif action == ClinicalActionType.START_IV_FLUIDS:
        updated.vital_signs.systolic_bp = min(
            300,
            updated.vital_signs.systolic_bp + 8,
        )
        updated.vital_signs.diastolic_bp = min(
            200,
            updated.vital_signs.diastolic_bp + 4,
        )
        updated.vital_signs.heart_rate = max(
            0,
            updated.vital_signs.heart_rate - 4,
        )
        updated.cumulative_harm = max(0, updated.cumulative_harm - 5)
        description = "Intravenous fluids started. Temporary hemodynamic support applied."

    elif action == ClinicalActionType.ACTIVATE_TRANSFUSION:
        updated.vital_signs.systolic_bp = min(
            300,
            updated.vital_signs.systolic_bp + 14,
        )
        updated.vital_signs.diastolic_bp = min(
            200,
            updated.vital_signs.diastolic_bp + 7,
        )
        updated.vital_signs.heart_rate = max(
            0,
            updated.vital_signs.heart_rate - 8,
        )
        updated.estimated_blood_loss_ml = max(
            0,
            updated.estimated_blood_loss_ml - 250,
        )
        updated.cumulative_harm = max(0, updated.cumulative_harm - 12)
        description = "Transfusion protocol activated. Definitive resuscitation initiated."

    else:
        raise ValueError(f"Unsupported action: {action}")

    return updated, description
