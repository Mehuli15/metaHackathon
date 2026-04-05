try:
    from fastapi import FastAPI
except ImportError:
    FastAPI = None

app = FastAPI() if FastAPI is not None else None
state = {"machine_health": 100}


def compute_score(efficiency, energy=None, health=None):
    if isinstance(efficiency, list):
        return sum(item.get("reward", 0) for item in efficiency)

    if energy is None or health is None:
        raise ValueError("compute_score requires efficiency, energy, and health values")

    score = max(0.0, min(1.0, efficiency * 0.6 + (100.0 - energy) / 100.0 * 0.3 + health / 100.0 * 0.1))
    defect_rate = max(0.0, 1.0 - efficiency) + max(0.0, (100.0 - health) / 100.0 * 0.5)
    return score, round(defect_rate, 3)


if app is not None:
    @app.get("/grader")
    def get_score():
        global state

        efficiency = 0.8  # you can track last step metrics instead
        energy = 50
        health = state["machine_health"]

        score, defect_rate = compute_score(efficiency, energy, health)

        return {
            "score": score,
            "metrics": {
                "efficiency": efficiency,
                "energy": energy,
                "health": health,
                "defect_rate": defect_rate
            }
        }