def grade(task, observation):
    score = 0.0
    total = 0

    targets = task["targets"]

    # ---------------------------
    # TEMPERATURE (max_temp)
    # ---------------------------
    if "max_temp" in targets:
        total += 1
        if observation.temperature <= targets["max_temp"]:
            score += 1

    # ---------------------------
    # HEALTH (derived)
    # health = 1 - defect_rate
    # ---------------------------
    if "min_health" in targets:
        total += 1
        health = 1 - observation.defect_rate
        if health * 100 >= targets["min_health"]:
            score += 1

    # ---------------------------
    # EFFICIENCY
    # ---------------------------
    if "efficiency" in targets:
        total += 1
        diff = abs(observation.efficiency - targets["efficiency"])
        score += max(0, 1 - diff)

    # ---------------------------
    # ENERGY
    # ---------------------------
    if "max_energy" in targets:
        total += 1
        if observation.energy_consumption <= targets["max_energy"]:
            score += 1

    # ---------------------------
    # FINAL SCORE (0–1)
    # ---------------------------
    if total == 0:
        return 0.0

    final_score = score / total
    return round(final_score, 3)