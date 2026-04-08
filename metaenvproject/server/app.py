from fastapi import FastAPI
from pydantic import BaseModel

from metaenvproject.server.metaenvproject_environment import MetaenvprojectEnvironment
from metaenvproject.tasks import get_tasks
from metaenvproject.grader import grade

app = FastAPI()

env = MetaenvprojectEnvironment()


# ---------------------------
# REQUEST MODEL
# ---------------------------
class ActionRequest(BaseModel):
    temperature_change: float
    speed_change: float


# ---------------------------
# RESET
# ---------------------------
@app.post("/reset")
def reset():
    return env.reset()


# ---------------------------
# STEP
# ---------------------------
@app.post("/step")
def step(action: ActionRequest):
    action_dict = {
        "temperature_change": action.temperature_change,
        "speed_change": action.speed_change
    }
    return env.step(action_dict)


# ---------------------------
# STATE
# ---------------------------
@app.get("/state")
def state():
    return env.get_state()


# ---------------------------
# TASKS
# ---------------------------
@app.get("/tasks")
def tasks():
    return get_tasks()


# ---------------------------
# GRADER
# ---------------------------
class GradeRequest(BaseModel):
    task_id: str


@app.post("/grade")
def grade_task(req: GradeRequest):
    tasks = get_tasks()

    task = next((t for t in tasks if t["id"] == req.task_id), None)

    if not task:
        return {"error": "Task not found"}

    observation = env.reset()
    score = grade(task, observation)

    return {"score": score}


# ---------------------------
# HEALTH (IMPORTANT FOR HF)
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}