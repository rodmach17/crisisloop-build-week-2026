from backend.app.schemas.patient import ClinicalPhase, PatientState, VitalSigns


SCENARIO_ID = "postoperative_hemorrhagic_shock_v1"


def create_initial_patient_state() -> PatientState:
    return PatientState(
        scenario_id=SCENARIO_ID,
        elapsed_seconds=0,
        phase=ClinicalPhase.COMPENSATED,
        mental_status="alert but anxious",
        skin_perfusion="cool extremities",
        estimated_blood_loss_ml=750,
        cumulative_harm=5,
        vital_signs=VitalSigns(
            heart_rate=108,
            systolic_bp=104,
            diastolic_bp=68,
            respiratory_rate=22,
            oxygen_saturation=96,
            temperature_c=36.4,
        ),
    )
