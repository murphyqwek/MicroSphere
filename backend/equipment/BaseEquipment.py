from backend.dataQueue.DataQueue import DataQueue
from backend.equipment.EquipmentState import EquipmentState
from abc import ABC, abstractmethod

class BaseEquipment():
    __commandDataQueue = DataQueue()
    __dataQueue = DataQueue()
    __equipmentState = EquipmentState.STOPPED
    __equipmentStateChangeEvent = list()

    def __init__(self, dataQueue : DataQueue, commandQueue : DataQueue):
        self.__commandDataQueue = commandQueue
        self.__dataQueue = dataQueue
        self.__equipmentState = EquipmentState.STOPPED

    def addEquipmentStateChangeEventHandler(self, handler):
        self.__equipmentStateChangeEvent.append(handler)

    def setEquipmentState(self, EquipmentState : EquipmentState):
        self.__equipmentState = EquipmentState
        for handler in self.__equipmentStateChangeEvent:
            handler()


    def sendCommand(self, command: str):
        self.__commandDataQueue.appendData(command)

    def readData(self, extract: bool) -> str:
        return self.__dataQueue.getData(extract)

    def getEquipmentState(self) -> EquipmentState:
        return self.__equipmentState
    
    def getDataQueue(self) -> DataQueue:
        return self.__dataQueue
    
    def setDataQueue(self, dataQueue: DataQueue):
        self.__dataQueue = dataQueue

    def getCommandDataQueue(self) -> DataQueue:
        return self.__commandDataQueue
    
    def setCommandDataQueue(self, commandDataQueue: DataQueue):
        self.__commandDataQueue = commandDataQueue

    def dataBaseNotificationHandler(data: str):
        pass

    def __isInputDataForThisEquipment(data: str) -> bool:
        return True