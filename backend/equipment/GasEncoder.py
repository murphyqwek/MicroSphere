from backend.equipment.Encoder import Encoder

class GasEncoder(Encoder):
    def __init__(self, dataQueue, commandQueue):
        super().__init__(dataQueue, commandQueue, "Re", "Rd")