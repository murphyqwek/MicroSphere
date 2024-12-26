from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *

from ui.GasQ import GasQ_ui
from ui.services.timer import RepeatTimer

from backend.equipment.Encoder.GasEncoder import GasEncoder

from backend.dataQueue.DataQueue import DataQueue

import json

class GasQ(QtWidgets.QWidget, GasQ_ui.Ui_Gas):
    def __init__(self, dataQueue : DataQueue, commandQueue : DataQueue):
        super().__init__()
        self.setupUi(self)

        #Очереди на отправку и прием
        self.dataQueue = dataQueue
        self.commandQueue = commandQueue

        #Энкодер
        self.encoderEq = GasEncoder(dataQueue, commandQueue)

        # Настройка начальных значений
        self.dialGas.setMinimum(0)
        self.dialGas.setMaximum(132)  # Полный диапазон импульсов энкодера
        self.dialGas.setValue(0)
        self.valueGas.setText("00.00")
        self.valueGas.setReadOnly(True)
        self.valueGas.setInputMask("00.00")  # Устанавливаем маску для точности до сотых
        self.file_path = "gas_value.json"  # Путь к файлу для сохранения данных

        # Восстановление состояния
        self.current_value = self.load_gas_value()

        # Обновляем UI
        self.update_ui_from_value()

        # Связываем сигналы
        self.dialGas.valueChanged.connect(self.update_value_gas_from_dial)
        self.plusGas.clicked.connect(self.increment_gas_value)
        self.minusGas.clicked.connect(self.decrement_gas_value)

    def load_gas_value(self):
        """Считывает значение расхода из файла."""
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return data.get("current_value", 0.0)
        except FileNotFoundError:
            return 0.0

    def save_gas_value(self):
        """Сохраняет значение расхода в файл."""
        with open(self.file_path, "w") as file:
            json.dump({"current_value": self.current_value}, file)

    def update_ui_from_value(self):
        """Обновляет интерфейс на основе текущего значения расхода."""
        dial_value = round(self.current_value * 132 / 20)
        self.dialGas.setValue(dial_value)
        self.valueGas.setText(f"{self.current_value:.2f}")

    def update_value_gas_from_dial(self):
        """Обновляет расход на основе значения QDial."""
        self.current_value = self.dialGas.value() * 20 / 132
        self.valueGas.setText(f"{self.current_value:.2f}")
        self.save_gas_value()

    def increment_gas_value(self):
        """Увеличивает значение расхода газа."""
        current_value = self.dialGas.value()
        if current_value < self.dialGas.maximum():
            self.send_command_to_device(1)
            self.dialGas.setValue(current_value + 1)

    def decrement_gas_value(self):
        """Уменьшает значение расхода газа."""
        current_value = self.dialGas.value()
        if current_value > self.dialGas.minimum():
            self.send_command_to_device(-1)
            self.dialGas.setValue(current_value - 1)

    def generate_command(self, direction, action, steps):
        """
        Генерирует команду для энкодера.
        :param direction: 'L' или 'R' для газа или воздуха.
        :param action: 'e' (увеличение) или 'd' (уменьшение).
        :param steps: Количество шагов.
        """
        command = f"{direction}{action}{steps}n"
        print(f"Отправка команды: {command}")  # Для проверки
        self.send_command_to_device(command)

    def send_command_to_device(self, step : int):
        """Отправляет команду устройству."""
        self.encoderEq.moveEncoder(step)
        pass


