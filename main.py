from env.environment import ManufacturingEnv
from env.inference import baseline_policy
from env.grader import compute_score

env = ManufacturingEnv(level="easy")

state = env.reset()
history = []

print("🚀 Starting Factory Simulation\n")

while True:

    action = baseline_policy(state)

    result = env.step(action)
    history.append(result)

    state = result["observation"]

    print(f"Step {state['time_step']}: Reward = {result['reward']:.2f}, Temp = {result['info']['temperature']:.1f}, Health = {result['info']['machine_health']:.1f}, Efficiency = {result['info']['efficiency']:.3f}")

    if result["done"]:
        break

score = compute_score(history)

print("\n🏁 FINAL SCORE:", score)