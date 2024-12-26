from backend.equipment.SimpleEquipment import SimpleEquipment

class Air(SimpleEquipment):
    def __init__(self):
        super().__init__("INIT_COMMAND_AIR", "STOP_COMMAND_AIR")

    def __str__(self):
        return "Air"