@app.post("/openenv/reset")
def reset():
    global initialized
    obs = env.reset()
    initialized = True
    return obs.dict()


@app.get("/openenv/state")
def state():
    if not initialized:
        return {"error": "Call /reset first"}

    return {
        "temperature": env.temperature,
        "speed": env.speed,
        "efficiency": env.efficiency,
        "defect_rate": env.defect_rate,
        "energy_consumption": env.energy_consumption
    }


@app.post("/openenv/step")
def step(action: dict):
    if not initialized:
        return {"error": "Call /reset first"}

    obs = env.step(type("Action", (), action))
    return {
        "reward": obs.reward,
        "done": obs.done,
        "error": None
    }