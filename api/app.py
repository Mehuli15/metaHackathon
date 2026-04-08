from fastapi import FastAPI

app = FastAPI()

@app.post("/reset")
def reset():
    return {"status": "reset done"}

@app.get("/state")
def state():
    return {"state": "running"}

@app.post("/step")
def step():
    return {"reward": 1.0, "done": False}