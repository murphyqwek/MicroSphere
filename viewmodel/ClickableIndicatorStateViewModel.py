from backend.equipment.BaseEquipment import BaseEquipment
from backend.equipment.EquipmentState import EquipmentState
from PyQt5.QtCore import QObject, pyqtSignal
from viewmodel.IndicatorStateViewModel import IndicatorStateViewModel

class ClickableIndicatorStateViewModel(IndicatorStateViewModel):
    def __init__(self, equipment : BaseEquipment, indicator, startFunc, stopFunc, getIsPortOpen):
        super().__init__(equipment, indicator)

        self.startFunc = startFunc
        self.stopFunc = stopFunc
        self.getIsPortOpen = getIsPortOpen
        self.indicator.clicked.connect(self.click)


    def click(self):
        if not self.getIsPortOpen():
            return
        if self.equipment.getEquipmentState() == EquipmentState.WORKING:
            self.stopFunc()
        else:
            self.startFunc()