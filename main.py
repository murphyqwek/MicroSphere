import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from ui.MainWindow import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()