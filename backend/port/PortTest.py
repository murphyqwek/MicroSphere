from backend.dataQueue.DataQueue import DataQueue
import threading

class PortTest():
    Lock = threading.Lock()
    __dataQueue = DataQueue()
    __commandDataQueue = DataQueue()
    __isOpen = False
    isListening = False
    time = -1

    def __init__(self, dataQueue: DataQueue, commandDataQueue: DataQueue):
        self.__dataQueue = dataQueue
        self.__commandDataQueue = commandDataQueue

    def open(self):
        self.__isOpen = True

    def IsOpen(self):
        return self.__isOpen

    def close(self):
        self.__isOpen = False
        self.isListening = False
    
    def stopListening(self):
        self.isListening = False

    def startListening(self):
        self.isListening = True
        time = 1
        listeningThread = threading.Thread(target=self.__listening)
        listeningThread.start()


    def __listening(self):
        isWorking = self.isListening
        while isWorking:
            if self.time == 0:
                data = "stop"
                self.time = -10
            else:
                data = ""
            if data != "" and data != None:
                print(data)
                self.__dataQueue.appendData(data)
            
            try:
                command = self.__commandDataQueue.getData(True)
            except:
                command = ""

            if command != "":
                print(command)
                isWorking = True
                continue

            isWorking = self.isListening and self.isOpen()


    def setTime(self, seconds):
        with self.Lock:
            self.time = seconds