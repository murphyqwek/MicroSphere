from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from ui.MainWindow import MainWindow_ui, GasQ_ui, AirQ_ui
from ui.services.timer import RepeatTimer

from backend.experiment.Experiment import Experiment
from backend.equipment.EquipmentState import EquipmentState


class MainWindow(QtWidgets.QMainWindow, MainWindow_ui.Ui_MainWindow, QObject):
    time = 0
    startingTime = 0
    stopSignal = pyqtSignal()
    SetIndicatorSignal = pyqtSignal(QtWidgets.QPushButton, EquipmentState)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.StartApp = None

        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)


        # Меняем цвет текста LCD
        palette = self.LCD.palette()
        palette.setColor(palette.WindowText, QtGui.QColor(0, 0, 0))
        self.LCD.setPalette(palette)

        # Подписываемся на события
        self.StartButton.clicked.connect(self.Start)
        self.ButtonGasQ.clicked.connect(self.GasQ)
        self.ButtonAirQ.clicked.connect(self.AirQ)
        self.timeplus.clicked.connect(self.timePlus)
        self.timeminus.clicked.connect(self.timeMinus)
        self.GasQ = None
        self.AirQ = None
        self.connectSignals()
        self.experiment = Experiment(self.VentIndicator, self.VitajIndicator, self.AirIndicator, self.FireIndicator,
                                     self.PowerIndicator, self.stopSignal.emit)
        style = "QPushButton { border: 1px solid; border-radius: 10px; border-style: solid; padding: 5px;"
        style += "background-color: rgb(255, 255, 0); border-color: rgb(255, 170, 0); }"

        self.VentIndicator.setStyleSheet(style)
        self.VitajIndicator.setStyleSheet(style)
        self.AirIndicator.setStyleSheet(style)
        self.FireIndicator.setStyleSheet(style)

    # Через сигналы мы можем корректно вызывать метода окна из других потоков
    def connectSignals(self):
        # TODO: не забыть
        self.stopSignal.connect(self.setUItoDefaultState)

    def ChangeStartButtonState(self):
        style = "QPushButton { border: 2px solid; border-radius: 20px; border-style: solid; padding: 5px;  "

        if not self.isStarted:
            style += "background-color: rgb(0, 255, 0); border-color: rgb(0, 170, 0); }"
            text = "Старт"

            # Меняем обработчик события нажатия
            self.StartButton.clicked.disconnect(self.Stop)
            self.StartButton.clicked.connect(self.Start)

        else:
            style += "background-color: rgb(255, 32, 17); border-color: rgb(170, 0, 0); }"
            text = "Стоп"

            # Меняем обработчик события нажатия
            self.StartButton.clicked.disconnect(self.Start)
            self.StartButton.clicked.connect(self.Stop)

        self.StartButton.setStyleSheet(style)
        self.StartButton.setText(text)

    def Start(self):
        self.SetStatusLabel("")

        try:
            self.experiment.start()
        except Exception as e:
            self.SetStatusLabel(e.__str__())
            return

        # Если всё хорошо, меняем состояние кнопки
        self.isStarted = True
        self.ChangeStartButtonState()

        # Устанавливаем время
        str_time = self.GetTimeFromTimeEdit().split(":")
        self.startingTime = self.ConvertTimeFromInput(str_time[0], str_time[1])
        self.time = self.startingTime
        self.UpdateLCD()

        # Запускаем таймер
        self.timer = RepeatTimer(1, self.UpdateTimer)
        self.timer.start()

    def GasQ(self):
        self.GasQ = GasQ()
        self.GasQ.show()

    def AirQ(self):
        self.AirQ = AirQ()
        self.AirQ.show()

    def timePlus(self):
        int_time = self.GetTimeFromTimeEdit().split(":")
        if int(int_time[1]) >= 59:
            int_time[1] = "00"
            if int(int_time[0]) <= 0:
                int_time[0] = "01"
            else:
                if int(int_time[0]) <= 8:
                    int_time[0] = "0" + str(int(int_time[0]) + 1)
                else:
                    int_time[0] = str(int(int_time[0]) + 1)
        else:
            if int(int_time[1]) <= 8:
                int_time[1] = "0" + str(int(int_time[1]) + 1)
            else:
                int_time[1] = str(int(int_time[1]) + 1)
        self.timeEdit.setText(int_time[0] + int_time[1])

    def timeMinus(self):
        int_time = self.GetTimeFromTimeEdit().split(":")
        if int(int_time[1]) <= 10:
            if int_time[1] == "00":
                if int_time[0] != "00":
                    int_time[1] = "59"
                else:
                    int_time[0] = "00"
                if int(int_time[0]) <= 10:
                    if int_time[0] == "00":
                        int_time[0] = "00"
                    else:
                        int_time[0] = "0" + str(int(int_time[0]) - 1)
                else:
                    int_time[0] = str(int(int_time[0]) - 1)
            else:
                int_time[1] = "0" + str(int(int_time[1]) - 1)
        else:
            int_time[1] = str(int(int_time[1]) - 1)
        self.timeEdit.setText(int_time[0] + int_time[1])

    def Stop(self):
        self.experiment.stop()
        self.setUItoDefaultState()

    def setUItoDefaultState(self):
        # Меняем состояние кнопки
        self.isStarted = False
        self.ChangeStartButtonState()

        # Обнуляем время
        self.startingTime = 0
        self.time = 0
        self.UpdateLCD()

        # Останавливаем таймер
        self.timer.cancel()

    # Получаем время с экрана
    def GetTimeFromTimeEdit(self) -> str:
        return str(self.timeEdit.text())

    # Переводим оставшиеся время для LCD дисплея
    def ConvertTime(self):
        minutes = self.time // 60
        seconds = self.time - minutes * 60
        if seconds < 10:
            seconds = f"0{seconds}"

        return f"{minutes}.{seconds}"

    # Фнукции обновления LCD экрана. Вызывается таймером каждую секунду
    def UpdateTimer(self):
        if self.time - 1 <= 0:
            self.time = 0
            self.timer.cancel()
            self.Stop()

        if self.time > 0:
            self.time -= 1
        self.UpdateLCD()
        self.experiment.timerTickHandler(self.time * 1000)

    # Устанавливаем время для LCD экрана
    def UpdateLCD(self):
        time = self.ConvertTime()
        self.LCD.display(time)

    # Переводим время с экрана в секунды
    def ConvertTimeFromInput(self, minute: str, seconds: str):
        return int(minute) * 60 + int(seconds)

    def SetStatusLabel(self, message: str):
        self.StatusLabel.setText(message)

    def closeEvent(self, event):
        self.experiment.closePort()
        event.accept()


class GasQ(QtWidgets.QWidget, GasQ_ui.Ui_Gas):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class AirQ(QtWidgets.QWidget, AirQ_ui.Ui_Air):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
