from backend.equipment.Ventilation import Ventilation
from backend.equipment.Air import Air
from backend.equipment.Gas import Gas
from backend.equipment.Vitaj import Vitaj
from backend.equipment.Fire import Fire
from backend.equipment.Power import Power
from backend.port import Port, PortTest
from backend.dataQueue import DataQueue, DataQueueWithNotification
from ui.MainWindow import MainWindow
from time import sleep

from viewmodel.IndicatorStateViewModel import IndicatorStateViewModel
from viewmodel.ClickableIndicatorStateViewModel import ClickableIndicatorStateViewModel

class Experiment():
    def __init__(self, VentIndicator, VitajIndicator, AirIndicator, FireIndicator, PowerIndicator, StopSignal):
        #Сохраняем индикаторы
        self.VentIndicator = VentIndicator
        self.VitajIndicator = VitajIndicator
        self.AirIndicator = AirIndicator
        self.FireIndicator = FireIndicator
        self.PowerIndicator = PowerIndicator

        #Функция для завершения эксперимента для UI
        self.UIStop = StopSignal

        #Инициализируем очереди
        self.dataQueue = DataQueueWithNotification.DataQueueWithNotification()
        self.commandQueue = DataQueue.DataQueue()

        #Инициализируем порт
        #self.port = Port.Port(commandDataQueue=self.commandQueue, dataQueue=self.dataQueue)
        self.port = PortTest.PortTest(commandDataQueue=self.commandQueue, dataQueue=self.dataQueue)

        #Инициализируем объекты устройств
        self.Ventilation = Ventilation(self.dataQueue, self.commandQueue)
        self.Vitaj = Vitaj(self.dataQueue, self.commandQueue)
        self.Air = Air(self.dataQueue, self.commandQueue)
        self.Gas = Gas(self.dataQueue, self.commandQueue)
        self.Fire = Fire(self.dataQueue, self.commandQueue)
        self.Power = Power(self.stopByOutterCommand, self.dataQueue, self.commandQueue)
        self.time = 0

        #Подписываемся на события изменения состояния оборудования
        self.initIndicatorsViewModels()

        self.port.open()
        self.port.startListening()

    def initIndicatorsViewModels(self):
        self.VentInicatorVM = ClickableIndicatorStateViewModel(self.Ventilation, self.VentIndicator, 
                                                        self.Ventilation.initialize, self.Ventilation.stop,
                                                        self.getIsPortOpen)
        self.VitajIndicatorVM = ClickableIndicatorStateViewModel(self.Vitaj, self.VitajIndicator, 
                                                        self.Vitaj.initialize, self.Vitaj.stop,
                                                        self.getIsPortOpen)
        
        self.AirIndicatorVM = ClickableIndicatorStateViewModel(self.Air, self.AirIndicator, 
                                                        self.Air.initialize, self.Air.stop,
                                                        self.getIsPortOpen)
        
        self.FireIndicatorVM = ClickableIndicatorStateViewModel(self.Fire, self.FireIndicator, 
                                                        self.Fire.initialize, self.Fire.stop,
                                                        self.getIsPortOpen)

        #self.PowerIndicatorVM = IndicatorStateViewModel(self.Power, self.PowerIndicator)

    def getIsPortOpen(self) -> bool:
        return self.port.IsOpen()

    def openPort(self):
        self.port.open()

    def closePort(self):
        self.port.close()

    def startListening(self):
        self.port.startListening()
    
    def stopListening(self):
        self.port.stopListening()

    def stopEquipment(self):
        #self.Ventilation.stop()
        self.stopAir()
        self.stopVitaj()
        self.stopGas()
        self.stopFire()
        #self.stopPower()
        self.dataQueue.clear()

    def stopByOutterCommand(self):
        self.stopEquipment()
        self.UIStop()

    def stop(self):
        self.stopEquipment()

    def start(self):
        self.openPort()
        #self.initializeEquipments()
        self.step1()
        self.step2()
        self.step3()
        self.Power.startProgramm()

    def step1(self):
        self.initializeVentilation()
        self.initializeVitaj()
        sleep(2)
        #self.time = MainWindow.MainWindow.time
        #while self.time <= (MainWindow.MainWindow.time + 2):


    def step2(self):
        self.initializeFire()
        self.initializeGas()
        #while self.time <= (MainWindow.MainWindow.time + 2):
        sleep(2)

    def step3(self):
        self.initializeAir()
        self.stopFire()


    def initializeEquipments(self):
        self.initializeVentilation()
        self.initializeVitaj()
        self.initializeAir()
        self.initializeGas()
        self.initializeFire()
        #self.initializePower()


    def timerTickHandler(self, milliseconds):
        if isinstance(self.port, PortTest.PortTest):
            self.port.setTime(milliseconds // 1000)

    def initializeVentilation(self):
        self.Ventilation.initialize()

    def stopVentilation(self):
        self.Ventilation.stop()

    def initializeAir(self):
        self.Air.initialize()

    def stopAir(self):
        self.Air.stop()

    def initializeGas(self):
        self.Gas.initialize()

    def stopGas(self):
        self.Gas.stop()

    def stopVitaj(self):
        self.Vitaj.stop()

    def initializeVitaj(self):
        self.Vitaj.initialize()

    def initializeFire(self):
        self.Fire.initialize()

    def stopFire(self):
        self.Fire.stop()

    def initializeFire(self):
        self.Fire.initialize()

    def stopFire(self):
        self.Fire.stop()

    def initializePower(self):
        self.Power.initialize()

    def stopPower(self):
        self.Power.stop()