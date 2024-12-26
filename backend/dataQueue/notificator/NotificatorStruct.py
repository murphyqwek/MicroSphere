class NotificatorStruct():
    def __init__(self,  funcToNotificate, isNotificationSingle = True, key = ""):
        self.__key = key
        self.__funcToNotificate = funcToNotificate
        self.__isSingle = isNotificationSingle

    def isSingle(self):
        return self.__isSingle
    
    def callback(self, data : str):
        if self.__funcToNotificate == None:
            return
        self.__funcToNotificate(data)