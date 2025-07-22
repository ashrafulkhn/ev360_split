"""
Configuration module for PECC system.
Defines system-wide limits, intervals, and settings.
Modular and extensible for future updates.
"""

# Example configuration dictionary
CONFIG = {
    "max_secc": 6,
    "max_guns_per_secc": 12,
    "can_poll_interval_ms": 200,
    "status_update_interval_ms": 200,
    "power_limits": {
        "voltage_min": 0,
        "voltage_max": 1000,
        "current_min": 0,
        "current_max": 500,
    },
    # Add more configuration as needed
}
