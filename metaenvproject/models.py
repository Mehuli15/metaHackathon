# Copyright (c) Meta Platforms, Inc.
# Modified for custom OpenEnv project

"""
Data models for the Metaenvproject Environment.

This environment simulates a manufacturing system where an agent
controls temperature and speed to optimize efficiency, defects,
and energy consumption.
"""

from openenv.core.env_server.types import Action, Observation
from pydantic import Field


# ---------------------------
# ACTION MODEL
# ---------------------------
class MetaenvprojectAction(Action):
    """
    Action taken by the agent.
    Controls how temperature and speed change.
    """

    temperature_change: float = Field(
        ..., description="Change in temperature (-10 to +10 recommended)"
    )
    speed_change: float = Field(
        ..., description="Change in machine speed (-2 to +2 recommended)"
    )


# ---------------------------
# OBSERVATION MODEL
# ---------------------------
class MetaenvprojectObservation(Observation):
    """
    Observation returned by the environment.
    Represents current system state.
    """

    temperature: float = Field(..., description="Current temperature")
    speed: float = Field(..., description="Current machine speed")

    efficiency: float = Field(..., description="System efficiency (0–1)")
    defect_rate: float = Field(..., description="Defect rate (0–1)")
    energy_consumption: float = Field(..., description="Energy usage")

    reward: float = Field(..., description="Reward for current step")
    done: bool = Field(..., description="Whether episode is finished")