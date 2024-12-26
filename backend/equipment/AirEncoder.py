from backend.equipment.Encoder import Encoder

class AirEncoder(Encoder):
    def __init__(self, dataQueue, commandQueue):
        super().__init__(dataQueue, commandQueue, "Le", "Ld")