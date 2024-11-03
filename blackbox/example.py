import sys
from PyQt6.QtGui import QIcon
from blackbox.app.bar import FileMenuBar
from blackbox.app.static import LOGO, label
from blackbox.app.table import TableWidget, LoaderFromMenuWidget
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        window_label = label('main_window.title')

        self.setWindowIcon(QIcon(LOGO))
        self.setWindowTitle(window_label)
        self.setGeometry(200, 100, 1000, 600)

        file_menu_bar = FileMenuBar(self)
        self.setMenuBar(file_menu_bar)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        table_widget = TableWidget()
        layout.addWidget(table_widget)

        self.loader_menu_widget = LoaderFromMenuWidget()
        self.loader_menu_widget.data_loaded.connect(table_widget.handle_data_loaded)


def openApp():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    openApp()
