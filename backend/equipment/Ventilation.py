from backend.equipment.SimpleEquipment import SimpleEquipment

class Ventilation(SimpleEquipment):
    def __init__(self, dataQueue, commandQueue):
        super().__init__(dataQueue, commandQueue, "Be", "Bd")

    def __str__(self):
        return "Ventilation"