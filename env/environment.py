from .grader import compute_score

class FactoryEnv:
    def __init__(self):
        self.reset()

    # 🔄 Reset environment
    def reset(self, task="medium"):
        self.temperature = 70.0
        self.demand = 80.0
        self.machine_health = 100.0
        self.time_step = 0

        # Metrics tracking
        self.efficiency = 0.0
        self.energy = 0.0

        return self.get_state()

    # ▶️ Step function
    MAX_STEPS = 50

    def step(self, action):
        production, cooling, maintenance = normalize_action(action)

        new_state, reward, done, info = apply_step(
            self.temperature,
            self.demand,
            self.machine_health,
            self.time_step,
            production,
            cooling,
            maintenance
        )

        self.temperature = new_state["temperature"]
        self.demand = new_state["demand"]
        self.machine_health = new_state["machine_health"]
        self.time_step = new_state["time_step"]
        self.efficiency = info["efficiency"]
        self.energy = info["energy"]

        return {
            "observation": new_state,
            "reward": reward,
            "done": done,
            "info": info
        }

    # 📊 Get current state
    def get_state(self):
        return {
            "temperature": round(self.temperature, 2),
            "demand": round(self.demand, 2),
            "machine_health": round(self.machine_health, 2),
            "time_step": self.time_step
        }

    # 📈 Get performance metrics
    def get_metrics(self):
        return {
            "efficiency": round(self.efficiency, 4),
            "energy": round(self.energy, 2),
            "health": round(self.machine_health, 2)
        }


ManufacturingEnv = FactoryEnv


def normalize_action(action):
    if isinstance(action, dict):
        return (
            float(action.get("production_level", 0)),
            float(action.get("cooling_level", 0)),
            float(action.get("maintenance", 0))
        )

    return (
        float(getattr(action, "production_level", 0)),
        float(getattr(action, "cooling_level", 0)),
        float(getattr(action, "maintenance", 0))
    )


def apply_step(temperature, demand, health, time_step, production, cooling, maintenance):
    temperature += 0.1 * production - 0.2 * cooling
    temperature = max(0, temperature)

    health -= 0.05 * production
    health += 0.1 * maintenance
    health = max(0, min(health, 100))

    time_step += 1

    efficiency = min(production / max(demand, 1), 1.0)
    energy = production * 0.5 + cooling * 0.3 + maintenance * 0.2

    score, defect_rate = compute_score(efficiency, energy, health)
    reward = score

    done = (
        time_step >= FactoryEnv.MAX_STEPS
        or health < 50
        or temperature > 100
    )

    new_state = {
        "temperature": temperature,
        "demand": demand,
        "machine_health": health,
        "time_step": time_step
    }

    info = {
        "efficiency": efficiency,
        "energy": energy,
        "health": health,
        "defect_rate": defect_rate
        }

    return new_state, reward, done, info


def step(state, action):
    production, cooling, maintenance = normalize_action(action)

    return apply_step(
        state["temperature"],
        state["demand"],
        state["machine_health"],
        state["time_step"],
        production,
        cooling,
        maintenance
    )