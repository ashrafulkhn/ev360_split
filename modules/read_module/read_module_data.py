from modules.caninterface import CanInterface
from modules.factory_reader import FactoryReader

def readAllCanData(d):
    reader = FactoryReader.create_reader(d.arbitration_id,d.data)
    if reader:
        reader.read_input_data()

def readFromCan():
    bus = CanInterface.bus_instance
    for m in bus:
        readAllCanData(m)

def perform_action():
    readFromCan()