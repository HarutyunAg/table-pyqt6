import sys
from src.app.main_window import MainWindow
from PyQt6.QtWidgets import QApplication


def openApp():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
