from backend.equipment.SimpleEquipment import SimpleEquipment

class Fire(SimpleEquipment):
    def __init__(self, dataQueue, commandQueue):
        super().__init__(dataQueue, commandQueue, "Fe", "Fd")

    def __str__(self):
        return "Gas"
    
    def updateEquipmentBasedOnTime(self, seconds: int, startingTime: int):
        pass