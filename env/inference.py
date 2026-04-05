from env.action import Action

# ---------------- MEMORY ----------------
prev_production = 60
prev_cooling = 12
maintenance_cooldown = 0

def baseline_policy(state):
    temp = state["temperature"]
    health = state["machine_health"]
    demand = state["demand"]

    production = demand * 0.8
    cooling = 20
    maintenance = 5

    if temp > 75:
        cooling += 20

    if health < 90:
        maintenance += 15

    return {
        "production_level": min(production, 100),
        "cooling_level": min(cooling, 100),
        "maintenance": min(maintenance, 100)
    }