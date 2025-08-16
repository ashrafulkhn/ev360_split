from base_constant_manager import BaseConstantManager


class ConstantManager360KW(BaseConstantManager):

    def __init__(self, d1='',d2='',d3='',d4='',d5='',d6='', pe1current=0, pe2current=0, pe3current=0, pe4current=0,pe5current=0, pe6current=0, pe7current=0, pe8current=0,pe9current=0, pe10current=0, pe11current=0, pe12current=0, rc=0, vehiclestatus1=6, vehiclestatus2=6,vehiclestatus3=6, vehiclestatus4=6,vehiclestatus5=6, vehiclestatus6=6, vehiclestatus7=6,vehiclestatus8=6, vehiclestatus9=6,vehiclestatus10=6, vehiclestatus11=6,vehiclestatus12=6 ):
        super().__init__(d1,d2,d3,d4,d5,d6, pe1current, vehiclestatus2, vehiclestatus1,vehiclestatus3, vehiclestatus4,vehiclestatus5, vehiclestatus6, vehiclestatus7,vehiclestatus8, vehiclestatus9,vehiclestatus10, vehiclestatus11,vehiclestatus12,maxev1power,maxev2power)
        self._pe2_current = pe2current
        self._pe3_current = pe3current
        self._pe4_current = pe4current
        self._rc = rc
        self._power1 = targetpower1
        self._power2 = targetpower2
        self._maxpower1 = maxpower1
        self._maxpower2 = maxpower2
        
    def get_data_current_pe2(self):  # 360kW code change
        return self._pe2_current

    def set_data_current_pe2(self, x):
        self._pe2_current = x

    def get_data_current_pe3(self):  # 360kW code change
        return self._pe3_current

    def set_data_current_pe3(self, x):
        self._pe3_current = x

    def get_data_current_pe4(self):  # 360kW code change
        return self._pe4_current

    def set_data_current_pe4(self, x):
        self._pe4_current = x

    def get_data_running_current(self): # 360kW code change
        return self._rc

    def set_data_running_current(self, x):
        self._rc = x

    def get_data_targetpower_ev1(self): # 360kW code change
        return self._power1

    def set_data_targetpower_ev1(self, x):
        self._power1 = x

    def get_data_targetpower_ev2(self): # 360kW code change
        return self._power2

    def set_data_targetpower_ev2(self, x):
        self._power2 = x

    def get_data_maxpower1(self): # 360kW code change
        return self._maxpower1

    def set_data_maxpower1(self, x):
        self._maxpower1 = x

    def get_data_maxpower2(self): # 360kW code change
        return self._maxpower2

    def set_data_maxpower2(self, x):
        self._maxpower2 = x
