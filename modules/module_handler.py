from modules.constants import CanId, assignedModules
from modules.message_helper import ModuleMessage as mm
import threading
from modules.read_module.read_module_data import perform_action

# def update_module():
#     import time
#     from modules.constants import CanId, assignedModules, TOTAL_GUN
#     gun_keys = [f"GUN{i+1}" for i in range(TOTAL_GUN)]
#     all_can_ids = [getattr(CanId, f"CAN_ID_{i+1}") for i in range(TOTAL_GUN)]
#     while True:
#         print("update_module thread running...")
#         # Static 1:1 mapping: GUN1->MODULE1, GUN2->MODULE2, ...
#         modules_per_gun = {gun: [can_id] for gun, can_id in zip(gun_keys, all_can_ids)}
#         assignedModules.module_list_per_gun = modules_per_gun
#         print(f"[STATIC TEST] Updated module assignments: {assignedModules.module_list_per_gun}")
#         time.sleep(30)   # Cycle every 60 Seconds to give some time to the modules to stabilise before reassignment.

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

# if __name__ == "__main__":
#     # th1 = threading.Thread(target=update_module)
#     th2 = threading.Thread(target=manage_modules)
#     th3 = threading.Thread(target=perform_action)  # Run perform_action in a thread
#     # th1.start()
#     th2.start()
#     th3.start()
#     print("Threads started.")
#     # th1.join()
#     th2.join()
#     th3.join()