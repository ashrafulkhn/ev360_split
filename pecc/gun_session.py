"""
GunSession: Manages the state and logic for a single gun/outlet.
Implements state transitions (idle, charging, error, etc.) and session data.
"""

import asyncio
from enum import Enum, auto

class GunState(Enum):
    IDLE = auto()
    CHARGING = auto()
    ERROR = auto()
    STOPPED = auto()

class GunSession:
    def __init__(self, gun_id):
        self.gun_id = gun_id
        self.state = GunState.IDLE
        self.data = {
            "status": None,
            "current_demand": None,
            "voltage_demand": None,
            # Add more fields as needed
        }
        self.lock = asyncio.Lock()

    async def set_status(self, status):
        async with self.lock:
            self.data["status"] = status

    async def get_status(self):
        async with self.lock:
            return self.data["status"]

    async def set_current_demand(self, value):
        async with self.lock:
            self.data["current_demand"] = value

    async def get_current_demand(self):
        async with self.lock:
            return self.data["current_demand"]

    async def set_voltage_demand(self, value):
        async with self.lock:
            self.data["voltage_demand"] = value

    async def get_voltage_demand(self):
        async with self.lock:
            return self.data["voltage_demand"]

    async def transition_state(self, new_state):
        async with self.lock:
            self.state = new_state

    async def get_state(self):
        async with self.lock:
            return self.state

    # Add more getters/setters and state transitions as needed
