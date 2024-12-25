from backend.equipment.EquipmentState import EquipmentState
from abc import ABC, abstractmethod
from backend.port.PortBase import PortBase

class Equipment(ABC):
    Status = EquipmentState.STOPPED

    def __init__(self) -> None:
        self.Status = EquipmentState.NotWorking

    @classmethod
    @abstractmethod
    def start(self, port : PortBase):
        pass
    
    @classmethod
    @abstractmethod
    def stop(self, port : PortBase):
        pass

    #начальное время (statringTime) в секундах 
    def updateEquipmentBasedOnTime(self, seconds: int, startingTime: int):
        pass