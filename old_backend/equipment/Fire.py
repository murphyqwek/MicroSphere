from backend.equipment.SimpleEquipment import SimpleEquipment

class Fire(SimpleEquipment):
    def __init__(self):
        super().__init__("INIT_COMMAND_FIRE", "STOP_COMMAND_FIRE")

    def __str__(self):
        return "Gas"
    
    def updateEquipmentBasedOnTime(self, seconds: int, startingTime: int):
        pass