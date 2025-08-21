import can
from caninterface import CanInterface
from constants import CanId
from utility import DTH

class ModuleMessage:
    bus = CanInterface.bus_instance

    @classmethod
    def set_high_lowMode(cls,can_id, voltage):
        # Mode should be Low of High (2 - Low, 1 - High)
        mode = 2 if (voltage <= 500) else 1
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            16, 95, 0, 0, 0, 0, 0, mode])
        cls.bus.send(message)                                                       #b1=2 -lowmode, b1=1 -highmode

    @classmethod
    def requestModule_Voltage(cls, can_id):
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            18, 98, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    @classmethod
    def requestModule_Current(cls, can_id):
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            18, 48, 0, 0, 0, 0, 0, 0])
        cls.bus.send(message)

    @classmethod
    def setModule(cls, can_id, action):
        # Action:
        # START = 0
        # STOP = 1

        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[
            16, 4, 0, 0, 0, 0, 0, (0 if action == "START" else 1)])                                              # b2=0-startModule, b2=1 -stopModule
        cls.bus.send(message)

    @classmethod
    def setVoltage(cls, voltageValue, can_id):
        # voltageValue : float, eg. 400
        ModuleMessage.set_high_lowMode(cls, can_id, voltageValue)
        voltageValue_hex = DTH.convertohex(voltageValue)
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[16, 2, 0, 0, 0] + voltageValue_hex)
        cls.bus.send(message)

    @classmethod
    def setCurrent(cls, currentvalue,can_id):
       
        currentvalue_hex = DTH.convertohex(currentvalue)
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=[16, 3, 0, 0, 0] + currentvalue_hex)

        cls.bus.send(message)

 

    