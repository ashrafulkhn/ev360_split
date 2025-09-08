import configparser

class ConfigManager:
    def __init__(self, config_path="modules/module_config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_total_modules(self):
        # print("INFO: Get Total Power Module.")
        return int(self.config["total_power_module"]["TOTAL_MODULE"])

    def get_power_config(self, key):
        return self.config["power_360kw"].get(key)

    def get_module_id_map(self):
        id_map = {}
        total = self.get_total_modules()
        for i in range(1, total + 1):
            key = f"PS{i}_ID"
            value = int(self.get_power_config(key))
            id_map[value] = i
        return id_map

    def get_module_num_by_arbitration_id(self, arbitration_id):
        id_map = self.get_module_id_map()
        return id_map.get(arbitration_id)
