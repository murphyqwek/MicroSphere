from backend.port.PortBase import PortBase, Parity
import serial
import threading
import time
import queue

class PortTest(PortBase):
    def __init__(self):
        super().__init__(None)
    
    def open(self):
        self.isOpen = True

    def stop(self):
        self.isOpen = False
        self.IsListening = False

    def _PortBasecheckIfIsWorking(self):
        return self.isOpen and self.IsListening

    def _PortBase__listening(self):
        print("listening thread starts")
        while self.isOpen:
            try:
                self.queueIncomeData.put("stop")
                break
            except:
                break
        print("listening thread is closed")
    
    #Эта функция крутиться в отдельном потоке и шлет команды из очереди команд
    def _PortBase__sendingDataInThread(self):
        print("command send thread starts")
        with self.Lock:
            isWorking = self._PortBasecheckIfIsWorking()
        while isWorking:
            try:
                try:
                    command = self.queueToSend.get(timeout=0.1)
                except queue.Empty:
                    with self.Lock:
                        isWorking = self._PortBasecheckIfIsWorking()
                        continue

                print(command)
                isWorking = True
            except serial.SerialException as e:
                print(e)
                break
            except Exception as e:
                print(e)
                raise e
        print("command send thread is closed")


    #Эта функция крутится в потоке вызова обработчиков поступающих данных
    def _PortBase__invokeSubsrcibersWhenIncomeDataCycle(self):
        print("update listeners thread starts")
        try:
            with self.Lock:
                isWorking = self._PortBasecheckIfIsWorking()
            while isWorking:
                with self.Lock:
                    subs = self.subscribersToIncomeData.copy()
            
                if len(subs) == 0:
                    continue

                try:
                    command = self.queueIncomeData.get(timeout=0.1)
                except queue.Empty:
                    with self.Lock:
                        isWorking = self._PortBasecheckIfIsWorking()
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