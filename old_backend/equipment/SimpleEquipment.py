from backend.equipment.Equipment import Equipment
from backend.equipment.EquipmentState import EquipmentState
from backend.port.PortBase import PortBase

class SimpleEquipment(Equipment):
    def __init__(self, initCommand, stopCommand):
        super()
        self.initCommand = initCommand
        self.stopCommand = stopCommand

    def start(self, port : PortBase):
        self.Status = EquipmentState.WORKING
        try:
            port.sendDataToPort(self.initCommand)
        except Exception as e:
            self.Status = EquipmentState.Error
            raise e
        
    def stop(self, port : PortBase):
        self.Status = EquipmentState.STOPPED
        try:
            port.sendDataToPort(self.stopCommand)
        except Exception as e:
            self.Status = EquipmentState.Error
            print(e)
            pass