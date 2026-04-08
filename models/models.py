from pydantic import BaseModel, Field
from typing import Dict

# Observation (State)
class ObservationModel(BaseModel):
    temperature: float
    demand: float
    machine_health: float
    time_step: int


# Action (Input)
class ActionModel(BaseModel):
    production_level: float = Field(ge=0, le=100)
    cooling_level: float = Field(ge=0, le=100)
    maintenance: float = Field(ge=0, le=100)


# Metrics (Info)
class MetricsModel(BaseModel):
    efficiency: float
    energy: float
    health: float
    defect_rate: float


# Step Response
class StepResponse(BaseModel):
    state: ObservationModel
    reward: float
    done: bool
    info: MetricsModel


# Grader Response
class GraderResponse(BaseModel):
    score: float
    metrics: MetricsModel