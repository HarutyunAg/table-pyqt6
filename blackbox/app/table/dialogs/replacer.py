from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from blackbox.app.static import label
from blackbox.app.table.dialogs.finder import FindDialogLogic


class ReplaceDialogBase(QDialog):
    """
    A dialog window for performing find and replace operations in a QTableWidget.

    This dialog allows users to enter text to find and replace within a table.
    It provides options to find the next or previous occurrence,
    change the current occurrence, or change all occurrences of the specified text.

    Attributes:
        search_value (QLineEdit): Input field for the text to find.
        new_value_edit (QLineEdit): Input field for the text to replace with.
    
        change_button (QPushButton): Button to change the current occurrence of the old text to the new text.
        change_all_button (QPushButton): Button to change all occurrences of the old text to the new text.
        find_button (QPushButton): Button to find the next occurrence of the old text.
        arrow_down_button (QPushButton): Button to find the next occurrence of the old text.
        arrow_up_button (QPushButton): Button to find the previous occurrence of the old text.
    """
    def __init__(self, parent: QWidget = None):
        
        super().__init__(parent)

        label_old = label("replace_dialog.old")
        label_new = label("replace_dialog.new")
        label_find = label("replace_dialog.find")
        label_window = label("replace_dialog.title")
        label_change = label("replace_dialog.change")
        label_arrow_up = label("replace_dialog.arrow_up")
        label_change_all = label("replace_dialog.change_all")
        label_arrow_down = label("replace_dialog.arrow_down")

        self.setWindowTitle(label_window)

        self.search_value = QLineEdit(self)
        self.search_value.setPlaceholderText(label_old)

        self.new_value_edit = QLineEdit(self)
        self.new_value_edit.setPlaceholderText(label_new)

        self.find_button = QPushButton(label_find, self)
        self.change_button = QPushButton(label_change, self)
        self.change_all_button = QPushButton(label_change_all, self)

        self.arrow_up_button = QPushButton(label_arrow_up, self)
        self.arrow_down_button = QPushButton(label_arrow_down, self)

        # TODO: add radio buttons
        # self.radio_button_match_case = QRadioButton("--", self)
        # self.radio_button_match_whole_word = QRadioButton("---", self)
        # self.radio_button_match_case.setEnabled(False)
        # self.radio_button_match_whole_word.setEnabled(False)

        self.change_button.setEnabled(False)
        self.arrow_up_button.setEnabled(False)
        self.arrow_down_button.setEnabled(False)
        self.change_all_button.setEnabled(False)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        layout.addWidget(self.search_value)
        layout.addWidget(self.new_value_edit)

        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.change_button)
        button_layout.addWidget(self.change_all_button)
        button_layout.addWidget(self.arrow_down_button)
        button_layout.addWidget(self.arrow_up_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


class ReplaceDialogLogic(FindDialogLogic):
    """
    Handles the logic for the ReplaceDialog, including find and replace operations.
    """

    def setup_connections(self):
        """
        Connects the find and replace signals from the ReplaceDialog.
        """
        super().setup_connections()
        self.dialog.change_button.clicked.connect(self.change_text)
        self.dialog.change_all_button.clicked.connect(self.change_all_text)

    def change_text(self):
        """
        Changes the current occurrence of the old text to the new text.
        """
        old = self.dialog.search_value.text()
        new = self.dialog.new_value_edit.text()
        tw = self.table_logic.table_widget

        if self.current_index == -1:
            return False

        row, col = self.found_items[self.current_index]
        item = tw.item(row, col)

        if item and item.text() == old:
            item.setText(new)
            self._find_next()
            return True
        return False

    def change_all_text(self):
        """
        Changes all occurrences of the old text to the new text.
        """
        old = self.dialog.search_value.text()
        new = self.dialog.new_value_edit.text()
        tw = self.table_logic.table_widget

        for row in range(tw.rowCount()):
            for col in range(tw.columnCount()):
                item = tw.item(row, col)
                if item and item.text() == old:
                    item.setText(new)

    def _find_text_logic(self, text):
        """
        Extends the find logic to also enable 'replace' and 'replace_all' buttons.
        """
        super()._find_text_logic(text)

        if self.found_items:
            self.dialog.change_button.setEnabled(True)
            self.dialog.change_all_button.setEnabled(True)
        else:
            self.dialog.change_button.setEnabled(False)
            self.dialog.change_all_button.setEnabled(False)
