from enum import StrEnum

from pydantic import BaseModel, Field


class ClinicalPhase(StrEnum):
    COMPENSATED = "compensated"
    EARLY_SHOCK = "early_shock"
    DECOMPENSATED = "decompensated"
    CRITICAL = "critical"
    STABILIZED = "stabilized"


class VitalSigns(BaseModel):
    heart_rate: int = Field(ge=0, le=250)
    systolic_bp: int = Field(ge=0, le=300)
    diastolic_bp: int = Field(ge=0, le=200)
    respiratory_rate: int = Field(ge=0, le=80)
    oxygen_saturation: int = Field(ge=0, le=100)
    temperature_c: float = Field(ge=25, le=45)


class PatientState(BaseModel):
    scenario_id: str
    elapsed_seconds: int = Field(ge=0)
    phase: ClinicalPhase
    mental_status: str
    skin_perfusion: str
    estimated_blood_loss_ml: int = Field(ge=0)
    cumulative_harm: int = Field(ge=0, le=100)
    vital_signs: VitalSigns
