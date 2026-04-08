from fastapi import FastAPI

from environment import ManufacturingEnv

app = FastAPI()

env = ManufacturingEnv()

<<<<<<< HEAD

# ---------------------------
# RESET
# ---------------------------
=======
# ✅ REQUIRED for validator
@app.post("/openenv/reset")
def openenv_reset():
    state = env.reset()
    return {
        "state": state
    }

# optional (keep yours also)
>>>>>>> 1d84ded (add openenv reset endpoint)
@app.post("/reset")
def reset():
    return env.reset()


# ---------------------------
# STEP
# ---------------------------
@app.post("/step")
def step(action: dict):
    state, reward, done, info = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }


# ---------------------------
# STATE
# ---------------------------
@app.get("/state")
def state():
    return env.get_state()


# ---------------------------
# HEALTH
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}