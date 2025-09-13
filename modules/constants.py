from modules.config_manager import ConfigManager

config = ConfigManager()

FULL_POWER = 60  # This represents combined power configuration from all the modules in Kilo Watts(kW)
TOTAL_DIN = 8
TOTAL_DOUT = 32
TOTAL_GUN = 12
TOTAL_MODULE = config.get_total_modules()

class CanId:
    # # CAN IDs for Sending Message to Power Modules.
    CAN_ID_1  = 0x02204000
    CAN_ID_2  = 0x02208000
    CAN_ID_3  = 0x0220C000
    CAN_ID_4  = 0x02210000
    CAN_ID_5  = 0x02214000
    CAN_ID_6  = 0x02218000
    CAN_ID_7  = 0x0221C000
    CAN_ID_8  = 0x02220000
    CAN_ID_9  = 0x02224000
    CAN_ID_10 = 0x02228000
    CAN_ID_11 = 0x0222C000
    CAN_ID_12 = 0x02230000
    
    # CAN IDs for recieving Message from Power Modules are Extracted from the Serial Number of the Modules
    DIGITAL_OUT1 = 0xD00
    DIGITAL_OUT2 = 0xE00
    DIGITAL_OUT3 = 0xF00
    DIGITAL_OUT4 = 0x110
    DIGITAL_OUT5 = 0x120
    DIGITAL_OUT6 = 0x130

class ModuleDataModel:
    # set_module_data = {
    #     "MODULE1": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE2": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE3": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE4": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE5": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE6": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE7": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE8": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE9": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE10": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE11": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     },
    #     "MODULE12": {
    #         "VOLTAGE" : 600,
    #         "CURRENT" : 10,
    #     }
    # }

    # # Dynamically initialize read_module_data for all modules
    set_module_data = {
        f"MODULE{i+1}": {
            "VOLTAGE": 0,
            "CURRENT": 0,
        } for i in range(TOTAL_MODULE)
    }

    # Dynamically initialize read_module_data for all modules
    read_module_data = {
        f"MODULE{i+1}": {
            "VOLTAGE": 0,
            "CURRENT": 0,
            "TEMPERATURE": 0
        } for i in range(TOTAL_MODULE)
    }

    @classmethod
    def set_module_value(cls, module_num, key, value):
        module_key = f"MODULE{module_num}"
        if module_key in cls.read_module_data and key in cls.read_module_data[module_key]:
            cls.read_module_data[module_key][key] = value
        else:
            raise KeyError(f"Invalid module or key: {module_key}, {key}")

    @classmethod
    def get_module_value(cls, module_num, key):
        module_key = f"MODULE{module_num}"
        if module_key in cls.read_module_data and key in cls.read_module_data[module_key]:
            return cls.read_module_data[module_key][key]
        else:
            raise KeyError(f"Invalid module or key: {module_key}, {key}")

class assignedModules:
    module_list_per_gun = {f"GUN{i+1}": [] for i in range(TOTAL_GUN)}    # Data format here is module_list_per_gun = {"GUN1" : [], "GUN2": []}

class DigitalInputOutput:
    digitalInput_data = {f"DIN{i+1}": 0 for i in range(TOTAL_DIN)}
    digitalOutput_data = {f"DOUT{i+1}": 0 for i in range(TOTAL_DOUT)}