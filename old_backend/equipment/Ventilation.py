from backend.equipment.SimpleEquipment import SimpleEquipment

class Ventilation(SimpleEquipment):
    def __init__(self):
        super().__init__("INIT_COMMAND_GAS", "STOP_COMMAND_GAS")

    def __str__(self):
        return "Ventilation"