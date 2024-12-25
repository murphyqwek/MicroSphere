import threading
from backend.port import PortTest
import serial
import time


def main():
    serialPort = serial.Serial("COM7")
    p = PortTest.PortTest(serialPort)

    p.startListening()
    p.sendDataToPort("OGO!!!")
    print("Sended")
    p.sendDataToPort("12321")
    print("Sended")
    p.sendDataToPort("123")
    print("Sended")
    time.sleep(5)
    p.close()

if __name__ == "__main__":
    main()