
from constants import CanId
from message_helper import ModuleMessage as mm

if __name__ == "__main__":
    mm.setModule(CanId.CAN_ID_1,action="START")
    voltagevalue = 400
    if voltagevalue < 500:
        mm.set_high_low_Mode(CanId.CAN_ID_1, voltage=voltagevalue)
    
    mm.setVoltage(400,CanId.CAN_ID_1)
    mm.setPower(demand_current, demand_voltage, CanId.CAN_ID_1)
    mm.requestModule_Voltage(CanId.CAN_ID_1)