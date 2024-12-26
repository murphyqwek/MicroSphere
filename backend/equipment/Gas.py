from backend.equipment.SimpleEquipment import SimpleEquipment

class Gas(SimpleEquipment):
    def __init__(self, dataQueue, commandQueue):
        super().__init__(dataQueue, commandQueue,"Ge", "Gd")

    def __str__(self):
        return "Gas"
        