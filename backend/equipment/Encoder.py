from backend.equipment.BaseEquipment import BaseEquipment
from backend.dataQueue.DataQueueWithNotification import DataQueueWithNotification
from ui.services.timer import RepeatTimer

class Encoder(BaseEquipment):
    commandUp = "Re"
    commandDown = "Rd"

    moved = True

    TIMEOUT = 5

    timeLeft = TIMEOUT

    currentPosition = 0

    def __init__(self, dataQueue, commandQueue, commandUp : str, commandDown : str):
        super().__init__(dataQueue, commandQueue)
        self.commandUp = commandUp
        self.commandDown = commandDown
        self.timer = RepeatTimer(1, self.checkForCommiting)

    def moveEncoder(self, newPosition):
        delta = newPosition - self.currentPosition
        if delta > 0:
            command = self.commandUp # + str(delta)
        elif delta < 0:
            command = self.commandDown # + str(delta)
        else:
            return
        
        self.currentPosition = newPosition
        
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