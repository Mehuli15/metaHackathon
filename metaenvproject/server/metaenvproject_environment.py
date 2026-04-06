# Copyright (c) Meta Platforms, Inc.
# Modified for custom OpenEnv project

from uuid import uuid4
import pandas as pd

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import MetaenvprojectAction, MetaenvprojectObservation
except ImportError:
    from models import MetaenvprojectAction, MetaenvprojectObservation


class MetaenvprojectEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        import os

        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir, "../../"))

        file_path = os.path.join(project_root, "_h_batch_process_data.xlsx")

        print("DEBUG PATH:", file_path)

        self.data = pd.read_excel(file_path)

        # Clean column names
        self.data.columns = self.data.columns.str.strip()

        print("COLUMNS:", self.data.columns.tolist())   # ---------------------------
    # RESET FUNCTION
    # ---------------------------
    def reset(self) -> MetaenvprojectObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        # 🔥 Pick random row from dataset
        row = self.data.sample(1).iloc[0]

        self.temperature = row["Temperature_C"]
        self.speed = row["Motor_Speed_RPM"]

        self.energy_consumption = row["Power_Consumption_kW"]

        self.efficiency = row["Pressure_Bar"]
        self.defect_rate = max(0, (100 - row["Compression_Force_kN"]) / 100)
        return MetaenvprojectObservation(
            temperature=self.temperature,
            speed=self.speed,
            efficiency=self.efficiency,
            defect_rate=self.defect_rate,
            energy_consumption=self.energy_consumption,
            done=False,
            reward=0.0,
        )

    # ---------------------------
    # STEP FUNCTION
    # ---------------------------
    def step(self, action: MetaenvprojectAction) -> MetaenvprojectObservation:
        self._state.step_count += 1

        # Apply action changes
        self.temperature += action.temperature_change
        self.speed += action.speed_change

        # Clamp values
        self.temperature = max(0, min(100, self.temperature))
        self.speed = max(0, min(1000, self.speed))

        # 🔥 Find closest dataset row (REALISTIC SIMULATION)
        closest_row = self.data.iloc[
            ((self.data["Temperature_C"] - self.temperature).abs()).argsort()[:1]
        ].iloc[0]

        self.energy_consumption = closest_row["Power_Consumption_kW"]
        self.efficiency = closest_row["Pressure_Bar"]
        self.defect_rate = max(0, (100 - closest_row["Compression_Force_kN"]) / 100)
        # ---------------------------
        # REWARD FUNCTION
        # ---------------------------
        efficiency_reward = self.efficiency * 2.0
        defect_penalty = self.defect_rate * 3.0
        energy_penalty = self.energy_consumption * 1.5

        # Stability bonus
        stability_bonus = 0.0
        if abs(action.temperature_change) < 5 and abs(action.speed_change) < 50:
            stability_bonus = 0.5

        reward = efficiency_reward - defect_penalty - energy_penalty + stability_bonus

        done = self._state.step_count >= 50

        return MetaenvprojectObservation(
            temperature=self.temperature,
            speed=self.speed,
            efficiency=self.efficiency,
            defect_rate=self.defect_rate,
            energy_consumption=self.energy_consumption,
            done=done,
            reward=reward,
        )

    # ---------------------------
    # STATE PROPERTY
    # ---------------------------
    @property
    def state(self) -> State:
        return self._state