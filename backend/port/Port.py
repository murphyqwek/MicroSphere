from backend.dataQueue.DataQueue import DataQueue
from backend.settings import settings
import serial
import threading

class Port():
    Lock = threading.Lock()
    __dataQueue = DataQueue()
    __commandDataQueue = DataQueue()
    isListening = False

    def __init__(self, dataQueue: DataQueue, commandDataQueue: DataQueue):
        self.__serialPort = serial.Serial(settings.PORT, settings.BAUDRATE)
        self.__dataQueue = dataQueue
        self.__commandDataQueue = commandDataQueue

    def IsOpen(self):
        return self.__serialPort.is_open

    def open(self):
        if self.__serialPort.is_open:
            return
        self.__serialPort.open()

    def close(self):
        self.__serialPort.close()
        self.isListening = False
    
    def stopListening(self):
        self.isListening = False

    def startListening(self):
        self.isListening = True

        listeningThread = threading.Thread(target=self.__listening)
        listeningThread.start()


    def __listening(self):
        isWorking = self.isListening
        while isWorking:
            data = ""
            try:
                if self.__serialPort.in_waiting != 0:
                    data = self.__serialPort.readline().decode()
            except:
                self.isListening = False
                isWorking = False
                self.Lock = False
                break
            if data != "" and data != None:
                print("-> " + data)
                self.__dataQueue.appendData(data)
            
            try:
                command = self.__commandDataQueue.getData(True)
            except:
                command = ""

            if command != "":
                print("<- " + command)
                self.__serialPort.write(command.encode())
                isWorking = True
                continue

            isWorking = self.isListening and self.IsOpen()