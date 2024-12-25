import serial
import enum
from backend.exceptions.PortIsNotOpenException import PortIsNotOpenException
from backend.exceptions.PortIsListeninngException import PortIsListeningException
from backend.exceptions.PortIsNotWokingException import PortIsNotWokingException
from abc import ABC, abstractmethod
import queue
import threading
import atexit

class Parity(enum.Enum):
    Yes = 1
    No = 2

class PortBase(ABC):
    subscribersToIncomeData = list()
    sendingToSubscribersIncomeDataThread = threading.Thread()
    queueToSend = queue.Queue()
    queueIncomeData = queue.Queue()
    isOpen = False
    incomeDataListeningThread = threading.Thread() 
    sendingDataToPortThread = threading.Thread()
    Lock = threading.Lock()
    IsListening = True

    def __init__(self, SerialPort : serial.Serial):
        self.serialPort = SerialPort

        self.__clearCommandQueue()
        self.__setListeningThreads()

    #Устанавливаем потоки
    def __setListeningThreads(self):
        self.incomeDataListeningThread = threading.Thread(target=self.__listening)
        self.sendingToSubscribersIncomeDataThread = threading.Thread(target=self.__invokeSubsrcibersWhenIncomeDataCycle)
        self.sendingDataToPortThread = threading.Thread(target=self.__sendingDataInThread)

    def __clearCommandQueue(self):
        self.queueToSend.queue.clear()

    def __update_isOpen(self):
        self.isOpen = self.serialPort.is_open

    def open(self):
        self.serialPort.open()
        self.__update_isOpen()

    def stopListening(self):
        self.IsListening = False
        self.incomeDataListeningThread.join()
        self.sendingDataToPortThread.join()

    def close(self):
        with self.Lock:
            self.serialPort.close()
            self.__update_isOpen()
        self.sendingDataToPortThread.join()
        self.incomeDataListeningThread.join()

    def __preparePortAndThreadsBeforeListening(self):
        if self.incomeDataListeningThread.is_alive():
            raise PortIsListeningException()
        self.__setListeningThreads()
        if not self.isOpen:
            self.open()
        self.IsListening = True

    def startListening(self):
        self.__preparePortAndThreadsBeforeListening()
        self.incomeDataListeningThread.start()
        self.sendingToSubscribersIncomeDataThread.start()
        self.sendingDataToPortThread.start()

    #Добавляем новый обработчик получаемых данных
    def subscribeNewDelegateToIncomeData(self, func):
        with self.Lock:
            self.subscribersToIncomeData.append(func)
    
    #Эта функция крутится в потоке вызова обработчиков поступающих данных
    def __invokeSubsrcibersWhenIncomeDataCycle(self):
        print("update listeners thread starts")
        try:
            with self.Lock:
                isWorking = self.checkIfIsWorking()
            while isWorking:
                with self.Lock:
                    subs = self.subscribersToIncomeData.copy()
            
                if len(subs) == 0:
                    continue

                try:
                    command = self.queueIncomeData.get(timeout=0.1)
                except queue.Empty:
                    with self.Lock:
                        isWorking = self.checkIfIsWorking()
                        continue

                for sub in subs:
                    sub(command, self)
                
                isWorking = True
        except serial.SerialException as e:
            print(e)
        except Exception as e:
            print(e)
            raise e
        print("update listeners thread is closed")


    @classmethod
    @abstractmethod
    def __listening(self):
        pass

    #Добавляем команду в очередь команд для отправки
    def sendDataToPort(self, data: str):
        if not self.isOpen:
            raise PortIsNotOpenException()
        if not self.sendingDataToPortThread.is_alive():
            raise PortIsNotWokingException("Can't put command in command queue if the port is not working")
        self.__addDataToQueueToSend(data)

    def checkIfIsWorking(self):
        return self.serialPort.is_open and self.IsListening

    #Эта функция крутиться в отдельном потоке и шлет команды из очереди команд
    def __sendingDataInThread(self):
        print("command send thread starts")
        with self.Lock:
            isWorking = self.checkIfIsWorking()
        while isWorking:
            try:
                try:
                    command = self.queueToSend.get(timeout=0.1)
                except queue.Empty:
                    with self.Lock:
                        isWorking = self.checkIfIsWorking()
                        continue

                print(command)
                self.serialPort.write(command.encode('utf-8'))
                isWorking = True
            except serial.SerialException as e:
                print(e)
                break
            except Exception as e:
                print(e)
                raise e
        print("command send thread is closed")

    def __addDataToQueueToSend(self, command: str):
        with self.Lock:
            self.queueToSend.put(command)

    def cleanup(self):
        self.close()
        self.incomeDataListeningThread.join(10)
        self.sendingToSubscribersIncomeDataThread.join(10)