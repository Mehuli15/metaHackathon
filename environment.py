import numpy as np
import pandas as pd
class ManufacturingEnv:
    def __init__(self):
        self.df = pd.read_excel("_h_batch_process_data.xlsx")
        self.reset()
    def reset(self):
        row = self.df.sample(1).iloc[0]
        self.temperature = row["Temperature_C"]
        self.speed = row["Motor_Speed_RPM"]
        outputs = self.get_outputs(self.temperature, self.speed)
        self.efficiency = outputs["efficiency"]
        self.defect_rate = outputs["defect_rate"]
        self.energy = outputs["energy"]
        return self.get_state()
    def get_outputs(self, temp, speed):
        row = self.df.iloc[
            ((self.df["Temperature_C"] - temp) ** 2 +
             (self.df["Motor_Speed_RPM"] - speed) ** 2).argmin()
        ]
        energy = row["Power_Consumption_kW"]
        efficiency = max(0, 1 - (energy / 100))
        defect_rate = min(1, energy / 100)
        return {
            "efficiency": efficiency,
            "defect_rate": defect_rate,
            "energy": energy
        }
    def step(self, action):
        prev_temp = self.temperature
        prev_speed = self.speed
        self.temperature += action["temp_change"]
        self.speed += action["speed_change"]
        self.temperature = np.clip(self.temperature, 0, 500)
        self.speed = np.clip(self.speed, 0, 5000)
        outputs = self.get_outputs(self.temperature, self.speed)
        self.efficiency = outputs["efficiency"]
        self.defect_rate = outputs["defect_rate"]
        self.energy = outputs["energy"]
        reward = self.compute_reward(prev_temp, prev_speed)
        done = False
        return self.get_state(), reward, done, {}
    def compute_reward(self, prev_temp, prev_speed):
        reward = 0
        reward += self.efficiency * 2
        reward -= self.defect_rate * 3
        reward -= self.energy * 0.5
        reward -= abs(self.temperature - prev_temp) * 0.05
        reward -= abs(self.speed - prev_speed) * 0.05
        return reward
    def get_state(self):
        return {
            "temperature": float(self.temperature),
            "speed": float(self.speed),
            "efficiency": float(self.efficiency),
            "defect_rate": float(self.defect_rate),
            "energy_consumption": float(self.energy)
        }