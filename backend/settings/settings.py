import platform

if platform.system() == "Linux":
    PORT = "/dev/ttyUSB0"
elif platform.system() == "Windows":
    PORT = "COM4"
else:
    PORT = ""

BAUDRATE = 115200