from backend.equipment.BaseEquipment import BaseEquipment
from backend.dataQueue.DataQueueWithNotification import DataQueueWithNotification
from ui.services.timer import RepeatTimer

class Encoder(BaseEquipment):
    command = "Re"

    moved = True

    TIMEOUT = 5

    timeLeft = TIMEOUT

    def __init__(self, dataQueue, commandQueue, baseCommandMove : str):
        super().__init__(dataQueue, commandQueue)
        self.command = baseCommandMove
        self.timer = RepeatTimer(1, self.checkForCommiting)

    def moveEncoder(self, iterations : int):
        command = self.command + str(iterations)
        
        if self.getDataQueue() is DataQueueWithNotification:
            dataQueue: DataQueueWithNotification = self.getCommandDataQueue()
            dataQueue.addNotificator("1", self.commitMovement, True)
            dataQueue.appendData(command)
            
            self.timeLeft = self.TIMEOUT
            self.timer.run()
        else:
            raise Exception("DataQueue without Notification in Encoder")

    def commitMovement(self, data : str):
        self.moved = True

    def checkForCommiting(self):
        if self.timeLeft == 0:
            raise NotImplemented("CheckForCommiting in Encoder")

        if not self.moved:
            self.timeLeft -= 1
        else:
            self.timer.stop()

    def __str__(self):
        return "Encoder"