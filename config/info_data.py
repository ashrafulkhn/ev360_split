from modules.constants  import *

class InfoData:
    @staticmethod
    def get_gun_info(gun_id):
        from modules.constants import assignedModules, ModuleDataModel
        module_ids = assignedModules.module_list_per_gun.get(gun_id, [])
        voltages = []
        currents = []
        temperatures = []
        for can_id in module_ids:
            # Map CAN ID to module number
            module_num = None
            for i in range(1, ModuleDataModel.read_module_data.__len__() + 1):
                expected_can_id = getattr(CanId, f"CAN_ID_{i}", None)
                if expected_can_id == can_id:
                    module_num = i
                    break
            if module_num:
                module_key = f"MODULE{module_num}"
                data = ModuleDataModel.read_module_data.get(module_key, {})
                voltages.append(data.get("VOLTAGE", 0))
                currents.append(data.get("CURRENT", 0))
                temperatures.append(data.get("TEMPERATURE", 0))
        # Aggregate: sum current, pick first voltage, average temperature
        measured_voltage = voltages[0] if voltages else 0
        measured_current = sum(currents) if currents else 0
        temperature = sum(temperatures) / len(temperatures) if temperatures else 0
        # You can add more fields as needed
        return {
            "measuredVoltage": measured_voltage,
            "measuredCurrent": measured_current,
            "drivenVoltage": 0,
            "drivenCurrent": 0,
            "temperature": temperature,
            "contactorsStatus": "open",
            "isolationStatus": "valid",
            "operationalStatus": "operative"
        }
