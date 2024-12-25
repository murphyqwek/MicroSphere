import enum

class EquipmentStatus(enum.Enum):
    Working = 1
    Waiting = 2
    Stopped = 3
    Error = 4 
    NotWorking = 5