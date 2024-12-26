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

    def __generateCommand(self, value : int):
        if value < 0:
            return f"{self.commandDown}{abs(value)}"
        else:
            return f"{self.commandUp}{abs(value)}"

    def moveEncoder(self, step : int):
        command = self.__generateCommand(step)
        self.currentPosition += step
        
        self.sendCommand(command)
        print("Отправка команды: " + command)
        #TODO: раскоментить
        """
        if self.getDataQueue() is DataQueueWithNotification:
            dataQueue: DataQueueWithNotification = self.getCommandDataQueue()
            dataQueue.addNotificator("1", self.commitMovement, True)
            dataQueue.appendData(command)


            
            #self.timeLeft = self.TIMEOUT
            #self.timer.run()
        else:
            raise Exception("DataQueue without Notification in Encoder")
            """

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