def get_tasks():
    return [
        {
            "id": "easy",
            "description": "Reduce defect rate below 0.2",
            "target": {
                "defect_rate": 0.2
            }
        },
        {
            "id": "medium",
            "description": "Balance efficiency and energy",
            "target": {
                "efficiency": 0.7,
                "energy_consumption": 1.2
            }
        },
        {
            "id": "hard",
            "description": "Optimize full system",
            "target": {
                "efficiency": 0.8,
                "defect_rate": 0.1,
                "energy_consumption": 1.0
            }
        }
    ]