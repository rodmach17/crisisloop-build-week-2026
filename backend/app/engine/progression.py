from backend.app.schemas.patient import ClinicalPhase, PatientState, VitalSigns


def advance_patient_state(
    state: PatientState,
    seconds: int,
) -> PatientState:
    if seconds <= 0:
        return state.model_copy(deep=True)

    elapsed = state.elapsed_seconds + seconds
    blood_loss = state.estimated_blood_loss_ml + int(seconds * 4.5)

    if elapsed < 60:
        phase = ClinicalPhase.COMPENSATED
        mental_status = "alert but anxious"
        skin_perfusion = "cool extremities"
        heart_rate = 108 + elapsed // 10
        systolic_bp = 104 - elapsed // 20
        diastolic_bp = 68
        respiratory_rate = 22 + elapsed // 20
        oxygen_saturation = 96
        cumulative_harm = min(100, 5 + elapsed // 15)

    elif elapsed < 150:
        phase = ClinicalPhase.EARLY_SHOCK
        mental_status = "anxious and increasingly restless"
        skin_perfusion = "cool, pale and clammy"
        heart_rate = 114 + (elapsed - 60) // 8
        systolic_bp = 101 - (elapsed - 60) // 6
        diastolic_bp = 66 - (elapsed - 60) // 30
        respiratory_rate = 25 + (elapsed - 60) // 18
        oxygen_saturation = 95
        cumulative_harm = min(100, 10 + (elapsed - 60) // 4)

    elif elapsed < 240:
        phase = ClinicalPhase.DECOMPENSATED
        mental_status = "confused and slow to respond"
        skin_perfusion = "cold, mottled and diaphoretic"
        heart_rate = 126 + (elapsed - 150) // 6
        systolic_bp = 86 - (elapsed - 150) // 5
        diastolic_bp = 58 - (elapsed - 150) // 10
        respiratory_rate = 30 + (elapsed - 150) // 15
        oxygen_saturation = 93
        cumulative_harm = min(100, 35 + (elapsed - 150) // 2)

    else:
        phase = ClinicalPhase.CRITICAL
        mental_status = "obtunded"
        skin_perfusion = "severely mottled with weak peripheral pulses"
        heart_rate = min(170, 141 + (elapsed - 240) // 8)
        systolic_bp = max(45, 68 - (elapsed - 240) // 4)
        diastolic_bp = max(30, 46 - (elapsed - 240) // 6)
        respiratory_rate = min(45, 36 + (elapsed - 240) // 20)
        oxygen_saturation = max(82, 91 - (elapsed - 240) // 30)
        cumulative_harm = min(100, 80 + (elapsed - 240) // 3)

    return PatientState(
        scenario_id=state.scenario_id,
        elapsed_seconds=elapsed,
        phase=phase,
        mental_status=mental_status,
        skin_perfusion=skin_perfusion,
        estimated_blood_loss_ml=blood_loss,
        cumulative_harm=cumulative_harm,
        vital_signs=VitalSigns(
            heart_rate=heart_rate,
            systolic_bp=max(0, systolic_bp),
            diastolic_bp=max(0, diastolic_bp),
            respiratory_rate=respiratory_rate,
            oxygen_saturation=oxygen_saturation,
            temperature_c=max(35.0, state.vital_signs.temperature_c - seconds * 0.001),
        ),
    )
