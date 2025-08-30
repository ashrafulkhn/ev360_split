import logging
from can_readers import *

#logger = logging.getLogger(__name__)

class FactoryReader:
    reader_dict = {
        PMSetDataCurrentPeccStatus1.arbitration_id: PMSetDataCurrentPeccStatus1,
        PMSetDataCurrentPeccStatus2.arbitration_id: PMSetDataCurrentPeccStatus2,
        PMSetDataCurrentPeccStatus3.arbitration_id: PMSetDataCurrentPeccStatus3,
        PMSetDataCurrentPeccStatus4.arbitration_id: PMSetDataCurrentPeccStatus4,
    }

    @staticmethod
    def create_reader(arbitration_id, data):
        reader_class = FactoryReader.reader_dict.get(arbitration_id)
        if not reader_class:
            #logger.warning(f'No matching reader object found for the arbitration ID: {arbitration_id}')
            return None
        return reader_class(data)
