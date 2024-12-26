from backend.equipment.SimpleEquipment import SimpleEquipment

class Gas(SimpleEquipment):
    def __init__(self):
        super().__init__("INIT_COMMAND_GAS", "STOP_COMMAND_GAS")

    def __str__(self):
        return "Gas"
        