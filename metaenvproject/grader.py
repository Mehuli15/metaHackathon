def grade(task, observation):
    score = 0.0

    target = task["target"]

    # ---------------------------
    # DEFECT SCORE
    # ---------------------------
    if "defect_rate" in target:
        diff = abs(observation.defect_rate - target["defect_rate"])
        score += max(0, 1 - diff)

    # ---------------------------
    # EFFICIENCY SCORE
    # ---------------------------
    if "efficiency" in target:
        diff = abs(observation.efficiency - target["efficiency"])
        score += max(0, 1 - diff)

    # ---------------------------
    # ENERGY SCORE
    # ---------------------------
    if "energy_consumption" in target:
        diff = abs(observation.energy_consumption - target["energy_consumption"])
        score += max(0, 1 - diff)

    # Normalize score (0–1)
    total_metrics = len(target)
    final_score = score / total_metrics if total_metrics > 0 else 0

    return min(max(final_score, 0), 1)