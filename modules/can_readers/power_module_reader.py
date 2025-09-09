from config_manager import ConfigManager
import logging
from base_reader import BaseReader
from constants import *
from utility import bytetobinary, binaryToDecimal, DTH

#logger = logging.getLogger(__name__)

class PowerModuleReader(BaseReader):
    def __init__(self, data, arbitration_id):
        self.data = data
        self.arbitration_id = arbitration_id
        self._binary_data = bytetobinary(data)

    def read_input_data(self):
        self._diff_vol_current = binaryToDecimal(int(self._binary_data[1]))
        bd = self._binary_data
        config_mgr = ConfigManager()
        module_id = config_mgr.get_module_num_by_arbitration_id(self.arbitration_id)
        module_voltage = None
        module_current = None
        module_temperature = None
        if module_id:
            # Read and Store Voltage Value
            if self._diff_vol_current == 98:
                volatge_power_module = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
                module_voltage = ((volatge_power_module) / 1000)
                ModuleDataModel.set_module_value(module_id, "VOLTAGE", module_voltage)
                # Print full module data after voltage update
                # print(f"INFO: MODULE{module_id} DATA AFTER VOLTAGE UPDATE: {ModuleDataModel.read_module_data[f'MODULE{module_id}']}")

            # Read and Store Current Value
            if self._diff_vol_current == 48:
                current_power_module = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
                module_current = int(current_power_module/1000)
                ModuleDataModel.set_module_value(module_id, "CURRENT", module_current)
                # Print full module data after current update
                print(f"INFO: MODULE{module_id} DATA AFTER CURRENT UPDATE: {ModuleDataModel.read_module_data[f'MODULE{module_id}']}")
            # If temperature is available, update similarly:
            if self._diff_vol_current == 30:
                module_temperature = binaryToDecimal(int(bd[4] + bd[5] + bd[6] + bd[7]))
                ModuleDataModel.set_module_value(module_id, "TEMPERATURE", module_temperature/1000)

            # print(f"INFO: READ MODULE{module_id} - V: {module_voltage}, I: {module_current}")