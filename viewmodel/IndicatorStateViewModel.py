from backend.equipment.BaseEquipment import BaseEquipment
from backend.equipment.EquipmentState import EquipmentState
from PyQt5.QtCore import QObject, pyqtSignal

class IndicatorStateViewModel(QObject):
    updateIndicatorStateSignal = pyqtSignal()

    def __init__(self, equipment : BaseEquipment, indicator):
        super().__init__()
        self.equipment = equipment
        self.indicator = indicator

        self.updateIndicatorStateSignal.connect(self.updateIndicatorState)
        self.equipment.addEquipmentStateChangeEventHandler(
            self.updateIndicatorStateSignal.emit)

    def updateIndicatorState(self):
        state = self.equipment.getEquipmentState()

        style = "QPushButton { border: 1px solid; border-radius: 10px; border-style: solid; padding: 5px;"
        if state == EquipmentState.WORKING:
            style += "background-color: rgb(0, 255, 0); border-color: rgb(0, 170, 0); }"
        elif state == EquipmentState.ERROR:
            style += "background-color: rgb(255, 32, 17); border-color: rgb(170, 0, 0); }"
        elif state == EquipmentState.STOPPED:
            style += "background-color: rgb(255, 255, 0); border-color: rgb(255, 170, 0); }"
        else:
            raise Exception("Not all Indicator states is checked")
        
        self.indicator.setStyleSheet(style)