import logging
from power_360kw.can_readers import *

#logger = logging.getLogger(__name__)


class FactoryReader:

    reader_dict = {
        DigitalInputReader1.arbitration_id: DigitalInputReader1,
        DigitalInputReader2.arbitration_id: DigitalInputReader2,
        DigitalInputReader3.arbitration_id: DigitalInputReader3,
        DigitalInputReader4.arbitration_id: DigitalInputReader4,
        DigitalInputReader5.arbitration_id: DigitalInputReader5,
        DigitalInputReader6.arbitration_id: DigitalInputReader6,
        PMSetDataCurrentPeccStatus1.arbitration_id: PMSetDataCurrentPeccStatus1,
        PMSetDataCurrentPeccStatus2.arbitration_id: PMSetDataCurrentPeccStatus2,
        PMSetDataCurrentPeccStatus3.arbitration_id: PMSetDataCurrentPeccStatus3,
        PMSetDataCurrentPeccStatus4.arbitration_id: PMSetDataCurrentPeccStatus4,
        PMSetDataCurrentPeccStatus5.arbitration_id: PMSetDataCurrentPeccStatus5,
        PMSetDataCurrentPeccStatus6.arbitration_id: PMSetDataCurrentPeccStatus6,
        PMSetDataCurrentPeccStatus7.arbitration_id: PMSetDataCurrentPeccStatus7,
        PMSetDataCurrentPeccStatus8.arbitration_id: PMSetDataCurrentPeccStatus8,
        PMSetDataCurrentPeccStatus9.arbitration_id: PMSetDataCurrentPeccStatus9,
        PMSetDataCurrentPeccStatus10.arbitration_id: PMSetDataCurrentPeccStatus10,
        PMSetDataCurrentPeccStatus11.arbitration_id: PMSetDataCurrentPeccStatus11,
        PMSetDataCurrentPeccStatus12.arbitration_id: PMSetDataCurrentPeccStatus12,
        Vehicle1StatusReader.arbitration_id: Vehicle1StatusReader,
        Vehicle2StatusReader.arbitration_id: Vehicle2StatusReader,
        Vehicle3StatusReader.arbitration_id: Vehicle3StatusReader,
        Vehicle4StatusReader.arbitration_id: Vehicle4StatusReader,
        Vehicle5StatusReader.arbitration_id: Vehicle5StatusReader,
        Vehicle6StatusReader.arbitration_id: Vehicle6StatusReader,
        Vehicle7StatusReader.arbitration_id: Vehicle7StatusReader,
        Vehicle8StatusReader.arbitration_id: Vehicle8StatusReader,
        Vehicle9StatusReader.arbitration_id: Vehicle9StatusReader,
        Vehicle10StatusReader.arbitration_id: Vehicle10StatusReader,
        Vehicle11StatusReader.arbitration_id: Vehicle11StatusReader,
        Vehicle12StatusReader.arbitration_id: Vehicle12StatusReader,
        ResetGunModule1.arbitration_id: ResetGunModule1,
        ResetGunModule2.arbitration_id: ResetGunModule2,
        ResetGunModule3.arbitration_id: ResetGunModule3,
        ResetGunModule4.arbitration_id: ResetGunModule4,
        ResetGunModule5.arbitration_id: ResetGunModule5,
        ResetGunModule6.arbitration_id: ResetGunModule6,
        ResetGunModule7.arbitration_id: ResetGunModule7,
        ResetGunModule8.arbitration_id: ResetGunModule8,
        ResetGunModule9.arbitration_id: ResetGunModule9,
        ResetGunModule10.arbitration_id: ResetGunModule10,
        ResetGunModule11.arbitration_id: ResetGunModule11,
        ResetGunModule12.arbitration_id: ResetGunModule12,
        MaxEVvalues1.arbitration_id: MaxEVvalues1,
        MaxEVvalues2.arbitration_id: MaxEVvalues2
    }

    @staticmethod
    def create_reader(arbitration_id, data):
        reader_class = FactoryReader.reader_dict.get(arbitration_id)
        if not reader_class:
            #logger.warning(f'No matching reader object found for the arbitration ID: {arbitration_id}')
            return None
        return reader_class(data)
