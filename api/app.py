from fastapi import FastAPI
from metaenvproject.server.metaenvproject_environment import MetaenvprojectEnvironment
from metaenvproject.models import MetaenvprojectAction, MetaenvprojectObservation
from tasks.tasks import TASKS
from metaenvproject.grader import grade

app = FastAPI()

# Create environment instance
env = MetaenvprojectEnvironment()

# Reset initially
current_obs = env.reset()


@app.post("/step")
def step_api(action: MetaenvprojectAction):
    global current_obs

    current_obs = env.step(action)

    return {
        "temperature": current_obs.temperature,
        "speed": current_obs.speed,
        "efficiency": current_obs.efficiency,
        "defect_rate": current_obs.defect_rate,
        "energy_consumption": current_obs.energy_consumption,
        "reward": current_obs.reward,
        "done": current_obs.done,
    }


@app.post("/reset")
def reset_api():
    global current_obs
    current_obs = env.reset()
    return current_obs

@app.get("/tasks")
def get_tasks():
    return TASKS

@app.get("/score")
def get_score(task_name: str = "easy"):
    global current_obs

    task = TASKS.get(task_name)

    if not task:
        return {"error": "Invalid task"}

    score = grade(task, current_obs)

    return {
        "task": task_name,
        "score": score,
        "state": {
            "temperature": current_obs.temperature,
            "efficiency": current_obs.efficiency,
            "defect_rate": current_obs.defect_rate,
            "energy_consumption": current_obs.energy_consumption
        }
    }

@app.get("/state")
def get_state():
    global current_obs

    return {
        "temperature": current_obs.temperature,
        "speed": current_obs.speed,
        "efficiency": current_obs.efficiency,
        "defect_rate": current_obs.defect_rate,
        "energy_consumption": current_obs.energy_consumption,
        "reward": current_obs.reward,
        "done": current_obs.done,
    }