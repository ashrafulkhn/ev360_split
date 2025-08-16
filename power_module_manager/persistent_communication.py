import can
#import logging
import threading
import time

from constants import PECC, CanId
from caninterface import CanInterface

#logger = logging.getLogger(__name__)


class SetInterval:
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        try:
            thread=threading.Thread(target=self.__setInterval)
            thread.start()
            #logger.info(f"Started thread for constant status update from following method: {action.__name__}")
        except threading.ThreadException as err:
            pass
            #logger.error(f"Failed to start the thread for following method: {action.__name__}, error: {err}")

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()
        #logger.info(f"Stopped status update from following method: {self.action.__name__}")


class PECCStatusManager:
    # Bus interface
    bus = CanInterface.bus_instance

    @staticmethod
    def pecc_powers_voltage_limits_1():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L1,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun1)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_1():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L1,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun1)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_2():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L2,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun2)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_2():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L2,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun2)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_3():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L3,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun3)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_3():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L3,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun3)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_4():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L4,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun4)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_4():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L4,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun4)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_5():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L5,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun5)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_5():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L5,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun5)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_6():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L6,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun6)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_6():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L6,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun6)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_7():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L7,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun7)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_7():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L7,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun7)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_8():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L8,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun8)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_8():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L8,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun8)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_9():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L9,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun9)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_9():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L9,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun9)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_10():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L10,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun10)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_10():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L10,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun10)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_11():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L11,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun11)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_11():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L11,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun11)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_powers_voltage_limits_12():
        message = can.Message(arbitration_id=CanId.PECC_POWER_VOLTAGE_L12,
                              is_extended_id=False, data=PECC.LIMITS1_DATA_Gun12)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_current_limits_12():
        message = can.Message(arbitration_id=CanId.PECC_CURRENT_L12,
                              is_extended_id=False, data=PECC.LIMITS2_DATA_Gun12)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun1():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_GUN1,
                              is_extended_id=False, data=PECC.STATUS1_GUN1_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun1():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_GUN1,
                              is_extended_id=False, data=PECC.STATUS2_GUN1_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun2():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun2,
                              is_extended_id=False, data=PECC.STATUS1_GUN2_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun2():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun2,
                              is_extended_id=False, data=PECC.STATUS2_GUN2_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun3():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun3,
                              is_extended_id=False, data=PECC.STATUS1_GUN3_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun3():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun3,
                              is_extended_id=False, data=PECC.STATUS2_GUN3_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun4():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun4,
                              is_extended_id=False, data=PECC.STATUS1_GUN4_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun4():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun4,
                              is_extended_id=False, data=PECC.STATUS2_GUN4_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun5():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun5,
                              is_extended_id=False, data=PECC.STATUS1_GUN5_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun5():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun5,
                              is_extended_id=False, data=PECC.STATUS2_GUN5_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun6():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun6,
                              is_extended_id=False, data=PECC.STATUS1_GUN6_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun6():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun6,
                              is_extended_id=False, data=PECC.STATUS2_GUN6_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun7():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun7,
                              is_extended_id=False, data=PECC.STATUS1_GUN7_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun7():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun7,
                              is_extended_id=False, data=PECC.STATUS2_GUN7_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun8():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun8,
                              is_extended_id=False, data=PECC.STATUS1_GUN8_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun8():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun8,
                              is_extended_id=False, data=PECC.STATUS2_GUN8_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun9():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun9,
                              is_extended_id=False, data=PECC.STATUS1_GUN9_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun9():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun9,
                              is_extended_id=False, data=PECC.STATUS2_GUN9_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun10():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun10,
                              is_extended_id=False, data=PECC.STATUS1_GUN10_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun10():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun10,
                              is_extended_id=False, data=PECC.STATUS2_GUN10_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_1_Gun11():
        message = can.Message(arbitration_id=CanId.PECC_STATUS1_Gun11,
                              is_extended_id=False, data=PECC.STATUS1_GUN11_DATA)
        PECCStatusManager.bus.send(message)

    @staticmethod
    def pecc_status_2_Gun11():
        message = can.Message(arbitration_id=CanId.PECC_STATUS2_Gun11,
                              is_extended_id=False, data=PECC.STATUS2_GUN11_DATA)
        PECCStatusManager.bus.send(message)


def set_status_update():
    # Get all the attributes of the class
    attributes = dir(PECCStatusManager)

    # Filter for methods
    send_status_methods = [attr for attr in attributes if callable(getattr(PECCStatusManager, attr)) and not attr.startswith('__')]

    # Invoke all the methods
    for send_status in send_status_methods:
        send_status_method = getattr(PECCStatusManager, send_status)
        SetInterval(0.25, send_status_method)
