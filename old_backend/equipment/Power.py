from backend.equipment.ListeningEquipment import ListeningEquipment
from backend.equipment.EquipmentState import EquipmentState
from backend.port.PortBase import PortBase
import threading

class Power(ListeningEquipment):
    StopEvent = list()
    Lock = threading.Lock()

    def __init__(self) -> None:
        super().__init__("INNIT_COMMAND_POWER", "STOP_COMMAND_POWER")

    def _ListeningEquipment__commandHandler(self, command: str, port : PortBase):
        if self.Status != EquipmentState.WORKING:
            return
        
        print(command)

        if command == "stop":
            self.stop(port)
            self.__stopEvent()
            #TODO: прописать логику
            #В зависимости от функционала лучше создать новую функцию, запускаемую в новом потоке

    #Добавляем новый хендлер события, когда надо остановить всё
    def addStopEventHandler(self, stopEventHandler):
        with self.Lock:
            self.StopEvent.append(stopEventHandler)
    
    #Вызываем событие остановки
    def __stopEvent(self):
        with self.Lock:
            eventHanlders = self.StopEvent.copy()
        
        for handler in eventHanlders:
            handler()

    def __str__(self):
        return "Fire"

    def updateEquipmentBasedOnTime(self, seconds: int, startingTime: int):
        #TODO: определить
        print("Hello")
