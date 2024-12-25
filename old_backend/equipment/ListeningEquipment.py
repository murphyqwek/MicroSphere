from backend.equipment.SimpleEquipment import SimpleEquipment
from backend.equipment.EquipmentState import EquipmentState
from backend.port.PortBase import PortBase
from abc import ABC, abstractmethod

class ListeningEquipment(SimpleEquipment, ABC):
    def __init__(self, initCommand, stopCommand):
        super().__init__(initCommand, stopCommand)

    @classmethod
    @abstractmethod
    def __commandHandler(self, command: str, port : PortBase):
        pass