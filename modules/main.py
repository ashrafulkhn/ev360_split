from constants import CanId, assignedModules
from message_helper import ModuleMessage as mm
import threading

def update_module():
    import random
    import time
    from constants import CanId, assignedModules
    gun_keys = list(assignedModules.module_list_per_gun.keys())
    all_can_ids = [getattr(CanId, f"CAN_ID_{i}") for i in range(1, 13)]
    cycle_sizes = [5, 12, 6, 8, 3, 10]  # Example drastic changes
    cycle_idx = 0
    while True:
        print("update_module thread running...")
        available_can_ids = all_can_ids.copy()
        new_assignment = {}
        # Pick a random cycle size for this iteration
        num_modules = cycle_sizes[cycle_idx % len(cycle_sizes)]
        cycle_idx += 1
        # Randomly select num_modules from all_can_ids
        selected_modules = random.sample(all_can_ids, num_modules)
        # Distribute selected modules randomly among guns
        random.shuffle(gun_keys)
        modules_per_gun = {gun: [] for gun in gun_keys}
        for can_id in selected_modules:
            gun = random.choice(gun_keys)
            modules_per_gun[gun].append(can_id)
        assignedModules.module_list_per_gun = modules_per_gun
        print(f"Updated module assignments: {assignedModules.module_list_per_gun}")
        time.sleep(10)

if __name__ == "__main__":
    def manage_modules():
        import time
        from message_helper import ModuleMessage as mm
        while True:
            print("manage_modules thread running...")
            mm.sync_active_modules()
            time.sleep(0.500)

    th1 = threading.Thread(target=update_module)
    th2 = threading.Thread(target=manage_modules)
    th1.start()
    th2.start()
    print("Threads started.")
    th1.join()
    th2.join()