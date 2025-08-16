import logging
from base_reader import BaseReader
from power_180kw.constant_manager_180kw import ConstantManager180KW
from utility import bytetobinary

#logger = logging.getLogger(__name__)


class DigitalInputReader1(BaseReader):
    arbitration_id = 3330

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager360KW()

    def read_input_data(self):
        #logger.info('Reading digital input data for 180KW')
        self._global_data.set_data_d1(bytetobinary(self.data)[0])

class DigitalInputReader2(BaseReader):
    arbitration_id = 3586

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager360KW()

    def read_input_data(self):
        #logger.info('Reading digital input data for 180KW')
        self._global_data.set_data_d2(bytetobinary(self.data)[0])

class DigitalInputReader3(BaseReader):
    arbitration_id = 3842

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager360KW()

    def read_input_data(self):
        #logger.info('Reading digital input data for 180KW')
        self._global_data.set_data_d3(bytetobinary(self.data)[0])

class DigitalInputReader4(BaseReader):
    arbitration_id = 274

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager360KW()

    def read_input_data(self):
        #logger.info('Reading digital input data for 180KW')
        self._global_data.set_data_d4(bytetobinary(self.data)[0])

class DigitalInputReader5(BaseReader):
    arbitration_id = 290

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager360KW()

    def read_input_data(self):
        #logger.info('Reading digital input data for 180KW')
        self._global_data.set_data_d5(bytetobinary(self.data)[0])

class DigitalInputReader6(BaseReader):
    arbitration_id = 306

    def __init__(self, data):
        self.data = data
        self._global_data = ConstantManager360KW()

    def read_input_data(self):
        #logger.info('Reading digital input data for 180KW')
        self._global_data.set_data_d6(bytetobinary(self.data)[0])
