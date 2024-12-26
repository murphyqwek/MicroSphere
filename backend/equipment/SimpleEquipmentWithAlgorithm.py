from backend.equipment.SimpleEquipment import SimpleEquipment

class SimpleEquipmentWithAlgorithm(SimpleEquipment):
    def __init__(self, dataQueue, commandQueue, initCommand, stopCommand):
        super().__init__(dataQueue, commandQueue, initCommand, stopCommand)
    
    def workingProgram(self):
        pass

    def stopWorking(self):
        pass