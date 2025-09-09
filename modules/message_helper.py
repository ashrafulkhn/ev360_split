import can
from modules.caninterface import CanInterface
from modules.constants import CanId, assignedModules, ModuleDataModel
from modules.utility import DTH
import threading
import time

class ModuleMessage:
    bus = CanInterface.bus_instance
    # module_list = []

    @classmethod
    def sync_active_modules(cls):
        """
        Starts all modules currently assigned in assignedModules.module_list_per_gun,
        sends voltage/current parameters, and stops all others.
        If voltage is zero, send STOP instead of START for that module.
        """
        from modules.constants import CanId, assignedModules, ModuleDataModel
        all_can_ids = [getattr(CanId, f"CAN_ID_{i}") for i in range(1, 13)]   # TODO: Add the maximum number of modules in the config file.
        current_active = set()
        for modules in assignedModules.module_list_per_gun.values():
            current_active.update(modules)
        # Start and send parameters for active modules
        for can_id in current_active:
            # Find module name from CAN ID
            module_name = None
            for name in ModuleDataModel.module_data:
                idx = name.replace("MODULE", "")
                try:
                    if can_id == getattr(CanId, f"CAN_ID_{idx}"):
                        module_name = name
                        break
                except AttributeError:
                    continue
            voltage = None
            if module_name:
                voltage = ModuleDataModel.module_data[module_name]["VOLTAGE"]
            if voltage == 0:
                cls.setModule("STOP", can_id)
            else:
                cls.setModule("START", can_id)
                time.sleep(.05)
                current = ModuleDataModel.module_data[module_name]["CURRENT"] if module_name else 0
                cls.setVoltage(voltage, can_id)
                cls.setCurrent(current, can_id)
        # Stop all modules not currently assigned
        for can_id in set(all_can_ids) - current_active:
            cls.setModule("STOP", can_id)

    @classmethod
    def set_high_low_Mode(cls, can_id, voltage):
        # Mode should be Low of High (2 - Low, 1 - High)
        mode = 2 if (voltage <= 500) else 1
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            16, 95, 0, 0, 0, 0, 0, mode])    #b1=2 -lowmode, b1=1 -highmode
        # print(f"[CAN] set_high_low_Mode: CAN_ID={hex(can_id)}, voltage={voltage}, mode={mode}, data={message.data}")
        cls.bus.send(message)

    @classmethod
    def requestModule_Voltage(cls, can_id):
        #Add voltage request
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            18, 98, 0, 0, 0, 0, 0, 0])
        # print(f"[CAN] requestModule_Voltage: CAN_ID={hex(can_id)}, data={message.data}")
        cls.bus.send(message)

    @classmethod
    def requestModule_Current(cls, can_id):
        # add current request value
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            18, 48, 0, 0, 0, 0, 0, 0])
        # print(f"[CAN] requestModule_Current: CAN_ID={hex(can_id)}, data={message.data}")
        cls.bus.send(message)
    @classmethod
    def requestModule_Temperature(cls, can_id):
        # add current request value
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            18, 30, 0, 0, 0, 0, 0, 0])
        # print(f"[CAN] requestModule_Current: CAN_ID={hex(can_id)}, data={message.data}")
        cls.bus.send(message)

    @classmethod
    def setModule(cls, action, can_id):
        # Action:
        # START = 0
        # STOP = 1

        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            16, 4, 0, 0, 0, 0, 0, (0 if action == "START" else 1)])                                              # b2=0-startModule, b2=1 -stopModule
        # print(f"[CAN] setModule: CAN_ID={hex(can_id)}, action={action}, data={message.data}")
        cls.bus.send(message)

    @classmethod
    def setVoltage(cls, voltageValue, can_id):
        # voltageValue : float, eg. 
        cls.set_high_low_Mode(can_id=can_id, voltage=voltageValue)
        voltageValue_hex = DTH.convertohex(voltageValue)
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[16, 2, 0, 0, 0] + voltageValue_hex)
        # print(f"[CAN] setVoltage: CAN_ID={hex(can_id)}, voltage={voltageValue}, data={message.data}")
        cls.bus.send(message)

    @classmethod
    def setCurrent(cls, currentValue, can_id):
        currentvalue_hex = DTH.convertohex(currentValue)
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[16, 3, 0, 0, 0] + currentvalue_hex)
        # print(f"[CAN] setCurrent: CAN_ID={hex(can_id)}, current={currentValue}, data={message.data}")
        cls.bus.send(message)