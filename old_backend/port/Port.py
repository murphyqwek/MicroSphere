from backend.port.PortBase import PortBase
import serial
import threading

class Port(PortBase):
    Lock = threading.Lock()

    def __init__(self, SerialPort : serial.Serial):
        super().__init__(SerialPort)

    def open(self):
        self.isOpen = True

    def _PortBase__listening(self):
        with self.Lock:
            isWorking = self.serialPort.is_open and self.IsListening
        while isWorking:
            try:
                data = self.serialPort.readline().decode("utf-8")
                if data == "":
                    continue
                self.queueIncomeData.put(data)

                with self.Lock:
                    isWorking = self.serialPort.is_open and self.IsListening
            except serial.SerialException as e:
                print(e)
                return
            except Exception as e:
                print(e)
                raise e
