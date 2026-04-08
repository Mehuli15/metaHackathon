from typing import Dict


class BaselineAgent:
    def __init__(self):
        self.prev_defect = None
        self.prev_efficiency = None

    def act(self, obs: Dict) -> Dict:
        """
        Returns action in correct API format
        """

        efficiency = obs["efficiency"]
        defect_rate = obs["defect_rate"]
        energy = obs["energy_consumption"]

        # IMPORTANT: use *_change (not absolute values)
        action = {
            "temperature_change": 0,
            "speed_change": 0
        }

        # 🔴 Rule 1: Reduce defects
        if defect_rate > 0.2:
            action["temperature_change"] -= 2
            action["speed_change"] -= 2

        # 🟢 Rule 2: Improve efficiency
        if efficiency < 0.6:
            action["speed_change"] += 3

        # 🔵 Rule 3: Reduce energy
        if energy > 10:
            action["speed_change"] -= 2
            action["temperature_change"] -= 1

        # 🟡 Rule 4: Trend-based improvement
        if self.prev_defect is not None:
            if defect_rate > self.prev_defect:
                action["temperature_change"] -= 1

        if self.prev_efficiency is not None:
            if efficiency < self.prev_efficiency:
                action["speed_change"] += 1

        # Save history
        self.prev_defect = defect_rate
        self.prev_efficiency = efficiency

        return action