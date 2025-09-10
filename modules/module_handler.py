from modules.constants import CanId, assignedModules, ModuleDataModel
from modules.message_helper import ModuleMessage as mm
import threading
from modules.read_module.read_module_data import perform_action

def update_module(gun_id, voltage, current, state):
    from modules.constants import assignedModules, ModuleDataModel, CanId
    # Only assign module if gun is active (cablecheck, precharge, charging) and demand > 0
    if state in ["cablecheck", "preCharge", "charging"] and (voltage > 0 or current > 0):
        module_num = int(gun_id.replace("GUN", ""))
        can_id = getattr(CanId, f"CAN_ID_{module_num}")
        assignedModules.module_list_per_gun[gun_id] = [can_id]
        ModuleDataModel.set_module_data[f"MODULE{module_num}"]["VOLTAGE"] = voltage
        ModuleDataModel.set_module_data[f"MODULE{module_num}"]["CURRENT"] = current
        print(f"Assigned {gun_id} to MODULE{module_num} (CAN_ID={hex(can_id)}) with V={voltage} C={current}")
        print(f"Assigned Modules: {assignedModules.module_list_per_gun}")
        print(f"Assigned Modules Values: {ModuleDataModel.set_module_data}")
    else:
        assignedModules.module_list_per_gun[gun_id] = []
        module_num = int(gun_id.replace("GUN", ""))
        ModuleDataModel.set_module_data[f"MODULE{module_num}"]["VOLTAGE"] = 0
        ModuleDataModel.set_module_data[f"MODULE{module_num}"]["CURRENT"] = 0
        print(f"Cleared assignment for {gun_id} (inactive or zero demand)")
        print(f"Assigned Modules: {assignedModules.module_list_per_gun}")
        print(f"Assigned Modules Values: {ModuleDataModel.set_module_data}")

def manage_modules():
    import time
    from modules.message_helper import ModuleMessage as mm
    from modules.constants import assignedModules
    while True:
        print("manage_modules thread running...")
        mm.sync_active_modules()
        # Get all active module CAN IDs
        active_can_ids = set()
        for module_list in assignedModules.module_list_per_gun.values():
            active_can_ids.update(module_list)

        print(f"INFO: Active Module Can IDs: {active_can_ids}")
        # Request voltage and current for each active module
        for can_id in active_can_ids:
            mm.requestModule_Voltage(can_id=can_id)
            mm.requestModule_Current(can_id=can_id)
            mm.requestModule_Temperature(can_id=can_id)
        time.sleep(1)

if __name__ == "__main__":
    th1 = threading.Thread(target=update_module)
    th2 = threading.Thread(target=manage_modules)
    th3 = threading.Thread(target=perform_action)  # Run perform_action in a thread
    th1.start()
    th2.start()
    th3.start()
    print("Threads started.")
    th1.join()
    th2.join()
    th3.join()

else:
    print(f"{__name__} is imported succesfully.")