class NotificatorStruct():
    def __init__(self, key : str, funcToNotificate, isNotificationSingle : bool):
        self.__key = key
        self.__funcToNotificate = funcToNotificate
        self.__isSingle = isNotificationSingle

    def isSingle(self):
        return self.__isSingle
    
    def callback(self, data : str):
        self.__funcToNotificate(data)