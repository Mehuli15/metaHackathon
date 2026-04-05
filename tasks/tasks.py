# tasks/tasks.py

TASKS = {
    "easy": {
        "description": "Maintain safe temperature and high machine health",
        "targets": {
            "max_temp": 80,
            "min_health": 90
        }
    },
    "medium": {
        "description": "Balance efficiency and energy consumption",
        "targets": {
            "efficiency": 0.7,
            "max_energy": 30
        }
    },
    "hard": {
        "description": "Optimize full system performance",
        "targets": {
            "efficiency": 0.75,
            "max_energy": 25,
            "min_health": 85
        }
    }
}