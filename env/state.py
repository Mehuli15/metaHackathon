class State:
    def __init__(self):
        self.temperature = 70.0
        self.machine_health = 100.0
        self.demand = 80.0
        self.production_rate = 50.0
        self.energy_usage = 0.0
        self.time_step = 0

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "machine_health": self.machine_health,
            "demand": self.demand,
            "production_rate": self.production_rate,
            "energy_usage": self.energy_usage,
            "time_step": self.time_step
        }