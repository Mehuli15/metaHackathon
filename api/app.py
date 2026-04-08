from fastapi import FastAPI

from environment import ManufacturingEnv

app = FastAPI()

env = ManufacturingEnv()


# ---------------------------
# RESET
# ---------------------------
@app.post("/reset")
def reset():
    return {"message": "reset successful"}


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