from fastapi import FastAPI
from pydantic import BaseModel

from metaenvproject.server.metaenvproject_environment import MetaenvprojectEnvironment
from metaenvproject.models import MetaenvprojectAction
from metaenvproject.tasks import get_tasks
from metaenvproject.grader import grade

app = FastAPI()

env = MetaenvprojectEnvironment()


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
def step(action: MetaenvprojectAction):
    return env.step(action)


# ---------------------------
# STATE
# ---------------------------
@app.get("/state")
def state():
    return env.state


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

    # find task
    task = next((t for t in tasks if t["id"] == req.task_id), None)

    if not task:
        return {"error": "Task not found"}

    observation = env.reset()  # simulate one run
    score = grade(task, observation)

    return {"score": score}