from pydantic import BaseModel
from typing import Dict

# ✅ Observation
class ObservationModel(BaseModel):
    temperature: float
    demand: float
    machine_health: float
    time_step: int

# ✅ Action
class ActionModel(BaseModel):
    production_level: float
    cooling_level: float
    maintenance: int

# ✅ Step Response
class StepResponse(BaseModel):
    state: ObservationModel
    reward: float
    done: bool
    info: Dict

# ✅ Metrics
class MetricsModel(BaseModel):
    efficiency: float
    energy: float
    health: float

# ✅ Grader Response
class GraderResponse(BaseModel):
    score: float
    metrics: MetricsModel

# ✅ Tasks
class TaskDetail(BaseModel):
    description: str
    targets: Dict[str, float]

class TasksResponse(BaseModel):
    easy: TaskDetail
    medium: TaskDetail
    hard: TaskDetail