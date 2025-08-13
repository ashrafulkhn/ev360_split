import threading

class DispenserDataModel:
    @classmethod
    def from_json_file(cls, json_path):
        import json
        with open(json_path, 'r') as f:
            raw = json.load(f)
        # Flatten nested structure to a single dict of parameters
        def flatten(d, parent_key='', sep='.'):
            items = {}
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.update(flatten(v, new_key, sep=sep))
                else:
                    items[new_key] = v
            return items
        flat_data = flatten(raw)
        return cls(flat_data)
    """
    Thread-safe data model for dispenser parameters, supporting dynamic use for all guns.
    Automatically generates getter and setter methods for all parameters.
    """
    def __init__(self, initial_data=None):
        self._lock = threading.RLock()
        self._data = initial_data.copy() if initial_data else {}

    def get(self, key):
        with self._lock:
            return self._data.get(key)

    def set(self, key, value):
        with self._lock:
            self._data[key] = value

    def get_all(self):
        with self._lock:
            return self._data.copy()

    def update(self, data_dict):
        with self._lock:
            self._data.update(data_dict)

    def __getattr__(self, name):
        # Allow dynamic getter/setter for any parameter
        if name.startswith('get_'):
            param = name[4:]
            return lambda: self.get(param)
        elif name.startswith('set_'):
            param = name[4:]
            return lambda value: self.set(param, value)
        raise AttributeError(f"No such attribute: {name}")


if __name__ == "__main__":
    # Load initial data from JSON file
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "datamodel_dispenser.json")
    model = DispenserDataModel.from_json_file(json_path)
    print("Initial data loaded from JSON:")
    for k, v in model.get_all().items():
        print(f"{k}: {v}")
