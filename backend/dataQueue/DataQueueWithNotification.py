from backend.dataQueue.DataQueue import DataQueue
from backend.dataQueue.NotificatorStruct import NotificatorStruct
import threading

class DataQueueWithNotification(DataQueue):
    __notificationHashTable = dict()

    def appendData(self, data):
        super().appendData(data)
        notificator = self.__checkForNotification(data)
        notificator.callback(data)

    def __checkForNotification(self, data: str) -> NotificatorStruct:
        with threading.Lock():
            notificator = self.__notificationHashTable.get(data, None)
        if notificator.isSingle():
            self.__notificationHashTable.pop(data)

        return notificator
    
    def addNotificator(self, key : str, funcToNotificate, isSingle : bool):
        notifStruct = NotificatorStruct(key, funcToNotificate, isSingle)
        with threading.Lock():
            if self.__notificationHashTable.get(key, None) != None:
                print("DATA QUEUE NOTIFICATION HASH TABLE ALREADY HAS NOTIFICATOR")
            self.__notificationHashTable[key] = notifStruct