# gun_module_helpers.py

"""
Helper functions and classes for aggregating and accessing gun/module data.
"""

from modules.constants import assignedModules, ModuleDataModel

class GunModuleHelper:
    @staticmethod
    def is_module_management_running():
        """
        Returns True if either manage_modules or perform_action thread is running.
        """
        return (
            (GunModuleHelper._manage_modules_thread is not None and GunModuleHelper._manage_modules_thread.is_alive()) or
            (GunModuleHelper._perform_action_thread is not None and GunModuleHelper._perform_action_thread.is_alive())
        )
    @staticmethod
    def handle_gun_disconnect(gun_id):
        """
        Removes modules from assignedModules for the gun and resets demand to 0.
        """
        from modules.constants import assignedModules, DemandDataModel
        assignedModules.module_list_per_gun[gun_id] = []
        DemandDataModel.set_demand(gun_id, 0, 0)
    import threading

    _manage_modules_thread = None
    _perform_action_thread = None

    @staticmethod
    def start_module_management():
        """
        Starts manage_modules and perform_action threads if not already running.
        """
        from modules.main import manage_modules, perform_action
        if GunModuleHelper._manage_modules_thread is None or not GunModuleHelper._manage_modules_thread.is_alive():
            GunModuleHelper._manage_modules_thread = GunModuleHelper.threading.Thread(target=manage_modules, daemon=True)
            GunModuleHelper._manage_modules_thread.start()
        if GunModuleHelper._perform_action_thread is None or not GunModuleHelper._perform_action_thread.is_alive():
            GunModuleHelper._perform_action_thread = GunModuleHelper.threading.Thread(target=perform_action, daemon=True)
            GunModuleHelper._perform_action_thread.start()

    @staticmethod
    def stop_module_management():
        """
        Stops manage_modules and perform_action threads (if you implement a stop mechanism in those functions).
        """
        # You may need to implement a stop flag in manage_modules/perform_action for clean exit
        pass

    @staticmethod
    def all_guns_in_postcharge_or_reset(gun_states):
        """
        Returns True if all guns are in 'postCharge' or 'reset' state.
        """
        return all(state in ["postCharge", "reset"] for state in gun_states.values())
    @staticmethod
    def assign_module_to_gun(gun_id):
        """
        Assigns a module to a gun using simple 1:1 mapping: GunN -> ModuleN
        Updates assignedModules.module_list_per_gun accordingly.
        """
        from modules.constants import assignedModules
        try:
            gun_num = int(gun_id.replace('GUN', ''))
            if 1 <= gun_num <= 12:
                assignedModules.module_list_per_gun[gun_id] = [gun_num]
            else:
                assignedModules.module_list_per_gun[gun_id] = []
        except Exception as e:
            assignedModules.module_list_per_gun[gun_id] = []

    @staticmethod
    def get_gun_status(gun_id):
        """
        Aggregate voltage, current, and temperature for a gun from its assigned modules.
        Returns a dict: {"VOLTAGE": ..., "CURRENT": ..., "TEMPERATURE": ...}
        """
        module_nums = assignedModules.module_list_per_gun.get(gun_id, [])
        voltages = []
        currents = []
        temperatures = []
        for module_num in module_nums:
            module_key = f"MODULE{module_num}"
            data = ModuleDataModel.read_module_data.get(module_key)
            if data:
                voltages.append(data.get("VOLTAGE", 0))
                currents.append(data.get("CURRENT", 0))
                temperatures.append(data.get("TEMPERATURE", 0))
        return {
            "VOLTAGE": sum(voltages) if voltages else 0,
            "CURRENT": sum(currents) if currents else 0,
            "TEMPERATURE": sum(temperatures) if temperatures else 0
        }

    @staticmethod
    def set_module_value(module_num, key, value):
        ModuleDataModel.set_module_value(module_num, key, value)

    @staticmethod
    def get_module_value(module_num, key):
        return ModuleDataModel.get_module_value(module_num, key)
