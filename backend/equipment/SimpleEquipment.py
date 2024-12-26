from backend.equipment.BaseEquipment import BaseEquipment
from backend.equipment.EquipmentState import EquipmentState
from backend.dataQueue.DataQueue import DataQueue

class SimpleEquipment(BaseEquipment):
    def __init__(self, dataQueue : DataQueue, commandQueue : DataQueue, initCommand, stopCommand):
        super().__init__(dataQueue, commandQueue)
        self.initCommand = initCommand
        self.stopCommand = stopCommand

    def initialize(self):
        self.sendCommand(self.initCommand)
        self.setEquipmentState(EquipmentState.WORKING)
        
    def stop(self):
        self.sendCommand(self.stopCommand)
        self.setEquipmentState(EquipmentState.STOPPED)