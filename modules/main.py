
from constants import CanId
from message_helper import ModuleMessage as mm
if __name__ == "__main__":
    mm.setModule(CanId.CAN_ID_1,action="START")
    voltagevalue = 400
    if voltagevalue < 500:
        mm.set_high_lowMode(CanId.CAN_ID_1,mode=2)
    
    mm.setVoltage(400,CanId.CAN_ID_1)
    mm.setPower(demand_current, demand_voltage, CanId.CAN_ID_1)
    mm.readModule_Voltage(CanId.CAN_ID_1)
