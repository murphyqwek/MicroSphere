import queue
import threading

class DataQueue:
    __dataQueue = queue.Queue()

    def __init__(self):
        self.__dataQueue = queue.Queue()

    def clear(self):
        try:
            while True:
                self.__dataQueue.get(False)
        except queue.Empty:
            return


    def getData(self, extract: bool) -> str:
        if extract:
            try:
                data = self.__dataQueue.get(False)
            except queue.Empty():
                return ""
            return data
        
        with threading.Lock():
            if len(self.__dataQueue.queue) == 0:
                return ""
            
            data = self.__dataQueue.queue[0]

            return data
        
    def appendData(self, data: str):
        self.__dataQueue.put(data)