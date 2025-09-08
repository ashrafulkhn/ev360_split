
import logging
from modules.can_readers.power_module_reader import PowerModuleReader
from modules.constants import *

#logger = logging.getLogger(__name__)

total_module = TOTAL_MODULE
class FactoryReader:
    # No need for reader_dict; use generic PowerModuleReader

    @staticmethod
    def create_reader(arbitration_id, data):
        # Use generic PowerModuleReader for all modules
        return PowerModuleReader(data, arbitration_id)
