from backend.equipment.Encoder.Encoder import Encoder
from backend.dataQueue.DataQueue import DataQueue

class GasEncoder(Encoder):
    def __init__(self, dataQueue : DataQueue, commandQueue : DataQueue):
        super().__init__(dataQueue, commandQueue, "Le", "Ld")