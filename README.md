"# MetaHack Project" 
# Manufacturing Optimization Environment

Simulates a factory system with:

- Temperature dynamics
- Production control
- Energy usage
- Machine health

## Run

python main.py

Simulation & Reward Engine (Completed)

Role: Build the core system that simulates the factory environment and computes rewards for actions.

Features Implemented
State Variables:
temperature, demand, machine_health, time_step
Action Integration:
Accepts production_level, cooling_level, maintenance
Updates state based on these inputs
Reward Function (Multi-Objective):
Rewards high efficiency
Penalizes high defect rates
Penalizes excessive energy consumption
Done Condition:
Simulation ends if max time steps reached
Or if machine health or temperature cross safe limits
Pydantic Models:
ActionModel, ObservationModel, MetricsModel, StepResponse
Ensures type-safe API requests and responses
API Integration
/step endpoint returns:
state → current environment state
reward → computed reward
done → simulation status
info → metrics (efficiency, energy, health, defect_rate)

Example /step response:

{
  "state": {
    "temperature": 60,
    "demand": 80,
    "machine_health": 100,
    "time_step": 1
  },
  "reward": 0.7,
  "done": false,
  "info": {
    "efficiency": 1,
    "energy": 100,
    "health": 100,
    "defect_rate": 0
  }
}

Status: ✅ All environment, simulation logic, reward computation, and state management completed and fully functional.