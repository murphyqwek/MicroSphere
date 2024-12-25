from backend.dataQueue.DataQueue import DataQueue
import threading

class DataQueueWithNotification(DataQueue):
    __listOfSubscribers = list()

    def appendData(self, data):
        super().appendData(data)
        self.__invokeAllSubscribers(data)

    def __invokeAllSubscribers(self, data: str):
        with threading.Lock():
            for sub in self.__listOfSubscribers:
                self.__invokeSubscriber(sub, data)

    def __invokeSubscriber(self, subInvokeFunc, data: str):
        subInvokeFunc(data)