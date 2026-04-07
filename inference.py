import os
import requests
from openai import OpenAI  # REQUIRED (even if not used heavily)

# =========================
# ENV VARIABLES (MANDATORY)
# =========================
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "baseline")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

# MUST initialize OpenAI client (requirement)
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

# =========================
# CONFIG
# =========================
TASKS = ["easy", "medium", "hard"]
MAX_STEPS = 10


# =========================
# BASELINE POLICY
# =========================
def choose_action(state):
    action = {
        "temperature_change": 0,
        "speed_change": 0
    }

    # Reduce defects
    if state["defect_rate"] > 0.2:
        action["temperature_change"] = -2

    # Improve efficiency
    if state["efficiency"] < 0.6:
        action["speed_change"] = 5

    # Reduce energy
    if state["energy_consumption"] > 10:
        action["speed_change"] -= 2

    return action


# =========================
# RUN TASK
# =========================
def run_task(task):
    rewards = []

    print(f"[START] task={task} env=metaenvproject model={MODEL_NAME}")

    # RESET
    requests.post(f"{API_BASE_URL}/reset")

    for step in range(1, MAX_STEPS + 1):
        try:
            # Get current state
            state = requests.get(f"{API_BASE_URL}/state").json()

            from baseline import BaselineAgent
            agent = BaselineAgent()
            action = agent.act(state)

            res = requests.post(f"{API_BASE_URL}/step", json=action).json()

            reward = res.get("reward", 0.0)
            done = res.get("done", False)

            rewards.append(reward)

            print(
                f"[STEP] step={step} "
                f"action={action} "
                f"reward={reward:.2f} "
                f"done={str(done).lower()} "
                f"error=null"
            )

            if done:
                break

        except Exception as e:
            print(
                f"[STEP] step={step} "
                f"action=null "
                f"reward=0.00 "
                f"done=true "
                f"error={str(e)}"
            )
            break

    # GET FINAL SCORE
    score_res = requests.get(f"{API_BASE_URL}/score?task_name={task}").json()
    score = score_res.get("score", 0.0)

    # Clamp score [0,1]
    score = max(0.0, min(1.0, score))

    success = score > 0.3

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step} "
        f"score={score:.2f} "
        f"rewards={rewards_str}"
    )


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    for task in TASKS:
        run_task(task)