import pandas as pd
from loguru import logger
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QFileDialog, QMenuBar, QTableWidgetItem

from blackbox.app.static import label, shortcut


class FileMenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.__setup()

    def __setup(self):
        # Labels and Shortcuts Configuration
        action_config = {
            'bar.file_menu.save': (self.__save, True),
            'bar.file_menu.upload': (self.__upload, True),
            'bar.file_menu.new_table': (self.__create_new_table, True),
        }

        # Menu Label
        file_menu_label: str = label('bar.file_menu.menu_name')
        file_menu = self.addMenu(file_menu_label)

        # Create and add actions dynamically
        for key, (method, has_shortcut) in action_config.items():
            action = self.__create_action(key, method, has_shortcut)
            file_menu.addAction(action)

        file_menu.addSeparator()

    def __create_action(self, key: str, method, has_shortcut: bool) -> QAction:
        """
        Creates a QAction, connects it to a method, and optionally sets a shortcut.

        Args:
            key (str): The dot notation key for fetching label and shortcut.
            method (callable): The method to bind to the action.
            has_shortcut (bool): If True, assigns a shortcut from the configuration.

        Returns:
            QAction: Configured action instance.
        """
        action = QAction(label(key), self)
        action.triggered.connect(method)
        if has_shortcut:
            action.setShortcut(QKeySequence(shortcut(key)))
        return action

    def __upload(self):
        return self.parent.loader_menu_widget.load_from_menu()

    def __save(self):
        path, _ = QFileDialog.getSaveFileName(self.parent,
                                              "Save", "",
                                              "Excel Files (*.xlsx *.xls);;All Files (*)")
        if not path:
            return 

        columns = [self.parent.table_widget.horizontalHeaderItem(j).text()
                   for j in range(self.parent.table_widget.model().columnCount())]

        df = pd.DataFrame(columns=columns)

        for row in range(self.parent.table_widget.rowCount()):
            for col in range(self.parent.table_widget.columnCount()):
                item = self.parent.table_widget.item(row, col)
                df.at[row, columns[col]] = item.text() if item is not None else ""
        df.fillna("", inplace=True)
        df.to_excel(path, index=False)
        logger.success(f'file was saved on path {path}')

    def __create_new_table(self):
        """
        Clears the current table and sets up an empty one with default headers.
        """
        self.parent.table_widget.clear()
        self.parent.table_widget.setRowCount(0)
        self.parent.table_widget.setColumnCount(3)  # Default to 3 columns
        headers = ['Column 1', 'Column 2', 'Column 3']
        self.parent.table_widget.setHorizontalHeaderLabels(headers)

        # Add an initial empty row for convenience
        self.parent.table_widget.insertRow(0)
        for col in range(3):
            self.parent.table_widget.setItem(0, col, QTableWidgetItem(""))

        self.parent.table_widget.update()
        self.parent.table_widget.repaint()
