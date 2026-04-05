from fastapi import FastAPI
from models import ActionModel, StepResponse, ObservationModel, MetricsModel
from env import step

app = FastAPI()

state = {
    "temperature": 70,
    "demand": 80,
    "machine_health": 100,
    "time_step": 0
}

@app.post("/step", response_model=StepResponse)
def step_api(action: ActionModel):
    global state

    new_state, reward, done, info = step(state, action)

    state = new_state

    return StepResponse(
        state=ObservationModel(**new_state),
        reward=reward,
        done=done,
        info=MetricsModel(**info)
    )