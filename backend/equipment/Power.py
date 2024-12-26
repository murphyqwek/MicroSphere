from backend.equipment.SimpleEquipmentWithAlgorithm import SimpleEquipmentWithAlgorithm
from backend.equipment.EquipmentState import EquipmentState
import threading

class Power(SimpleEquipmentWithAlgorithm):
    Lock = threading.Lock()
    Working = False

    def __init__(self, experimentStopFunc, dataQueue, commandQueue) -> None:
        super().__init__(dataQueue, commandQueue, "INNIT_COMMAND_POWER", "STOP_COMMAND_POWER")
        self.experimentStopFunc = experimentStopFunc

    def stopWorking(self):
        self.setEquipmentState(EquipmentState.STOPPED)
        self.Working = False

    def stop(self):
        super().stop()
        self.setEquipmentState(EquipmentState.STOPPED)
        self.Working = False 

    def startProgramm(self):
        programThread = threading.Thread(target=self.workingProgram)
        self.Working = True
        self.setEquipmentState(EquipmentState.WORKING)
        programThread.start()

    def workingProgram(self):
        while self.Working:
            data = self.readData(extract=False)
            if data == "stop":
                self.readData(extract=True)
                self.Working = False
                self.experimentStopFunc()
                continue

