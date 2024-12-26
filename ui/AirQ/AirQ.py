from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *

from ui.AirQ import AirQ_ui
from ui.services.timer import RepeatTimer

from backend.equipment.Encoder.AirEncoder import AirEncoder

from backend.dataQueue.DataQueue import DataQueue

import json


class AirQ(QtWidgets.QWidget, AirQ_ui.Ui_Air):
    def __init__(self, dataQueue : DataQueue, commandQueue : DataQueue):
        super().__init__()
        self.setupUi(self)

        #Очереди на получение и отправку данных
        self.dataQueue = dataQueue
        self.commandQueue = commandQueue

        #Энкодер
        self.encoderEq = AirEncoder(dataQueue, commandQueue) 

        # Настройка начальных значений
        self.dialAir.setMinimum(0)
        self.dialAir.setMaximum(132)  # Полный диапазон импульсов энкодера
        self.dialAir.setValue(0)
        self.valueAir.setText("00.00")
        self.valueAir.setReadOnly(True)
        self.valueAir.setInputMask("00.00")  # Устанавливаем маску для точности до сотых
        self.file_path = "Air_value.json"  # Путь к файлу для сохранения данных

        # Восстановление состояния
        self.current_value = self.load_air_value()

        # Обновляем UI
        self.update_ui_from_value()

        # Связываем сигналы
        self.dialAir.valueChanged.connect(self.update_value_air_from_dial)
        self.plusAir.clicked.connect(self.increment_air_value)
        self.minusAir.clicked.connect(self.decrement_air_value)

        self

    def load_air_value(self):
        """Считывает значение расхода из файла."""
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return data.get("current_value", 0.0)
        except FileNotFoundError:
            return 0.0

    def save_air_value(self):
        """Сохраняет значение расхода в файл."""
        with open(self.file_path, "w") as file:
            json.dump({"current_value": self.current_value}, file)

    def update_ui_from_value(self):
        """Обновляет интерфейс на основе текущего значения расхода."""
        dial_value = round(self.current_value * 132 / 60)
        self.dialAir.setValue(dial_value)
        self.valueAir.setText(f"{self.current_value:.2f}")

    def update_value_air_from_dial(self):
        """Обновляет расход на основе значения QDial."""
        self.current_value = self.dialAir.value() * 60 / 132
        self.valueAir.setText(f"{self.current_value:.2f}")
        self.save_air_value()

    def increment_air_value(self):
        """Увеличивает значение расхода воздуха."""
        current_value = self.dialAir.value()
        if current_value < self.dialAir.maximum():
            self.encoderEq.moveEncoder(1)
            self.dialAir.setValue(current_value + 1)

    def decrement_air_value(self):
        """Уменьшает значение расхода воздуха."""
        current_value = self.dialAir.value()
        if current_value > self.dialAir.minimum():
            self.encoderEq.moveEncoder(-1)
            self.dialAir.setValue(current_value - 1)

    def send_command_to_device(self, step):
        """Отправляет команду устройству."""
        self.encoderEq.moveEncoder(step)
