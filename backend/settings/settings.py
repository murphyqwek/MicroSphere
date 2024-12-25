from backend.experiment.Experiment import Experiment
from backend.dataQueue.DataQueue import DataQueue
from backend.port.Port import Port

def setupExperiment(experiment : Experiment):
    #Инициализируем очереди
    experiment.dataQueue = DataQueue()
    experiment.commandQueue = DataQueue()

    #Инициализируем порт
    experiment.port = Port(experiment.dataQueue, experiment.commandQueue, "COM2", 9600)