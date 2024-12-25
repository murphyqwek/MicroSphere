from backend.equipment.SimpleEquipment import SimpleEquipment
from backend.dataQueue.DataQueue import DataQueue

class Air(SimpleEquipment):
    def __init__(self, dataQueue : DataQueue, commandQueue : DataQueue):
        super().__init__(dataQueue, commandQueue,"Ae", "Ad")

    def __str__(self):
        return "Air"