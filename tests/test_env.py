from env.environment import ManufacturingEnv
from env.action import Action

def test_env_runs():
    env = ManufacturingEnv()
    state = env.reset()

    action = Action(
        production_level=80,
        cooling_level=10,
        maintenance=0
    )

    result = env.step(action)

    assert "observation" in result
    assert "reward" in result
    assert "done" in result