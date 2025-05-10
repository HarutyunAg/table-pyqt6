from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from blackbox.app.static import label


class FinderDialogBase(QDialog):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        label_window = label("finder_dialog.title")
        label_value = label("finder_dialog.value")
        label_find = label("finder_dialog.find")
        label_arrow_up = label("finder_dialog.arrow_up")
        label_arrow_down = label("finder_dialog.arrow_down")

        self.setWindowTitle(label_window)

        self.search_value = QLineEdit(self)
        self.search_value.setPlaceholderText(label_value)

        self.find_button = QPushButton(label_find, self)
        self.arrow_up_button = QPushButton(label_arrow_up, self)
        self.arrow_down_button = QPushButton(label_arrow_down, self)

        self.arrow_up_button.setEnabled(False)
        self.arrow_down_button.setEnabled(False)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        layout.addWidget(self.search_value)
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.arrow_up_button)
        button_layout.addWidget(self.arrow_down_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


class FindDialogLogic:
    """
    Abstract class encapsulating the logic for finding text in a table.
    """

    def __init__(self, dialog, table_logic) -> None:
        self.found_items = []
        self.current_index = -1

        self.dialog = dialog
        self.table_logic = table_logic
        self.setup_connections()

    def setup_connections(self):
        """
        Connect signals related to finding and navigating text.
        """
        self.dialog.find_button.clicked.connect(self._find_text)
        self.dialog.arrow_down_button.clicked.connect(self._find_next)
        self.dialog.arrow_up_button.clicked.connect(self._find_previous)

    def _find_text(self):
        """
        Finds the text in the table using TableWidgetLogic.
        """
        search_text = self.dialog.search_value.text()
        if self._find_text_logic(search_text):
            self.table_logic.select_current_item()

    def _find_next(self):
        """
        Navigates to the next occurrence of the found text.
        """
        if not self.found_items:
            return False
        self.current_index = (self.current_index + 1) % len(self.found_items)
        self.__select_current_item()
        return True

    def _find_previous(self):
        """
        Navigates to the previous occurrence of the found text.
        """
        if not self.found_items:
            return False
        self.current_index = (self.current_index - 1) % len(self.found_items)
        self.__select_current_item()
        return True

    def __select_current_item(self):
        tw = self.table_logic.table_widget
        if self.current_index != -1:
            row, column = self.found_items[self.current_index]
            tw.setCurrentCell(row, column)

    def _find_text_logic(self, text):
        """
        Searches the table for occurrences of the specified text.
        """
        self.found_items = []
        self.current_index = -1
        tw = self.table_logic.table_widget

        for row in range(tw.rowCount()):
            for col in range(tw.columnCount()):
                item = tw.item(row, col)
                if item and text == item.text():
                    self.found_items.append((row, col))

        if self.found_items:
            self.dialog.arrow_down_button.setEnabled(True)
            self.dialog.arrow_up_button.setEnabled(True)
            self._find_next()

