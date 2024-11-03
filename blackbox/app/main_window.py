from PyQt6.QtGui import QIcon
from blackbox.app.bar import FileMenuBar
from blackbox.app.static import LOGO, label
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from blackbox.app.table import TableWidget, LoaderMenuWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        window_label = label('main_window.title')

        self.setWindowIcon(QIcon(LOGO))
        self.setWindowTitle(window_label)
        self.setGeometry(200, 100, 1000, 600)

        self.file_menu_bar = FileMenuBar(self)
        self.setMenuBar(self.file_menu_bar)
    
        self.table_widget = TableWidget()
        self.loader_menu_widget = LoaderMenuWidget()

        self.layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        layout.addWidget(self.table_widget)

        self.loader_menu_widget.data_loaded.connect(self.table_widget.handle_data_loaded)
