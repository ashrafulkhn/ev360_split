from constants import ModuleDataModel, assignedModules
from message_helper import ModuleMessage as mm
import threading

data=ModuleDataModel.module_data
            
def read_Voltage_Current_Values(mod):
    mm.requestModule_Current(mod)
    mm.requestModule_Voltage(mod)
    

        
