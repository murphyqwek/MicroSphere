from backend.equipment.SimpleEquipment import SimpleEquipment

class Vitaj(SimpleEquipment):
    def __init__(self, dataQueue, commandQueue):
        super().__init__(dataQueue, commandQueue,"Ve", "Vd")

    def __str__(self):
        return "Vitaj"