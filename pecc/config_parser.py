"""
ConfigParser class for PECC system.
Reads configuration from config.ini and provides access as a dictionary.
"""

import configparser
import os

class PECCConfigParser:
    def __init__(self, ini_path=None):
        self.config = configparser.ConfigParser()
        if ini_path is None:
            ini_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        self.config.read(ini_path)
        self.data = self._parse_config()

    def _parse_config(self):
        data = {}
        # Server section
        server = self.config["server"]
        data["server_host"] = server.get("host", "0.0.0.0")
        data["server_port"] = server.getint("port", 8765)
        data["log_level"] = server.get("log_level", "INFO")
        # System section
        system = self.config["system"]
        data["max_secc"] = system.getint("max_secc", 6)
        data["max_guns_per_secc"] = system.getint("max_guns_per_secc", 12)
        data["can_poll_interval_ms"] = system.getint("can_poll_interval_ms", 200)
        data["status_update_interval_ms"] = system.getint("status_update_interval_ms", 200)
        # Power limits section
        power = self.config["power_limits"]
        data["power_limits"] = {
            "voltage_min": power.getint("voltage_min", 0),
            "voltage_max": power.getint("voltage_max", 1000),
            "current_min": power.getint("current_min", 0),
            "current_max": power.getint("current_max", 500),
        }
        return data

    def get(self, key, default=None):
        return self.data.get(key, default)

    def as_dict(self):
        return self.data
