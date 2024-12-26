from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from ui.MainWindow import MainWindow_ui

from ui.AirQ.AirQ import AirQ
from ui.GasQ.GasQ import GasQ

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

        # Таймеры для кнопок
        self.hold_timer_increase = None
        self.hold_timer_decrease = None

        # Состояние удержания
        self.is_holding_increase = False
        self.is_holding_decrease = False

        # Подключение событий кнопок
        self.timeplus.pressed.connect(self.start_hold_increase)
        self.timeplus.released.connect(self.stop_hold_increase)

        self.timeminus.pressed.connect(self.start_hold_decrease)
        self.timeminus.released.connect(self.stop_hold_decrease)

        # Подписываемся на события
        self.StartButton.clicked.connect(self.Start)
        self.ButtonGasQ.clicked.connect(self.GasQ)
        self.ButtonAirQ.clicked.connect(self.AirQ)
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

    def start_hold_increase(self):
        """Обработка начала удержания кнопки увеличения."""
        self.increment_timer(1)  # Увеличиваем на 1 при нажатии
        self.is_holding_increase = True
        self.hold_timer_increase = RepeatTimer(0.5, self.increment_on_hold_increase)
        self.hold_timer_increase.start()

    def stop_hold_increase(self):
        """Остановка удержания кнопки увеличения."""
        self.is_holding_increase = False
        if self.hold_timer_increase:
            self.hold_timer_increase.cancel()

    def increment_on_hold_increase(self):
        """Увеличение времени на 5 при удержании кнопки."""
        if self.is_holding_increase:
            self.increment_timer(5)

    def start_hold_decrease(self):
        """Обработка начала удержания кнопки уменьшения."""
        self.decrement_timer(1)  # Уменьшаем на 1 при нажатии
        self.is_holding_decrease = True
        self.hold_timer_decrease = RepeatTimer(0.5, self.decrement_on_hold)
        self.hold_timer_decrease.start()

    def stop_hold_decrease(self):
        """Остановка удержания кнопки уменьшения."""
        self.is_holding_decrease = False
        if self.hold_timer_decrease:
            self.hold_timer_decrease.cancel()

    def decrement_on_hold(self):
        """Уменьшение времени на 5 при удержании кнопки."""
        if self.is_holding_decrease:
            self.decrement_timer(5)

    def increment_timer(self, amount):
        """Увеличение таймера на заданное количество секунд."""
        int_time = self.GetTimeFromTimeEdit().split(":")
        minutes = int(int_time[0])
        seconds = int(int_time[1]) + amount

        if seconds >= 60:
            minutes += seconds // 60
            seconds %= 60

        self.timeEdit.setText(f"{minutes:02}:{seconds:02}")

    def decrement_timer(self, amount):
        """Уменьшение таймера на заданное количество секунд."""
        int_time = self.GetTimeFromTimeEdit().split(":")
        minutes = int(int_time[0])
        seconds = int(int_time[1]) - amount

        if seconds < 0:
            minutes -= 1
            seconds += 60

        # Убедимся, что время не становится отрицательным
        if minutes < 0:
            minutes = 0
            seconds = 0

        self.timeEdit.setText(f"{minutes:02}:{seconds:02}")

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
        self.GasQ = GasQ(self.experiment.dataQueue, self.experiment.commandQueue)
        self.GasQ.show()

    def AirQ(self):
        self.AirQ = AirQ(self.experiment.dataQueue, self.experiment.commandQueue)
        self.AirQ.show()

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