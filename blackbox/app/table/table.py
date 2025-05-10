import pandas as pd
from loguru import logger
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QKeySequence, QShortcut
from PyQt6.QtWidgets import QAbstractItemView, QMenu, QTableWidget, QTableWidgetItem

from blackbox.app.static import label, shortcut
from blackbox.app.table.dialogs import (
    FindDialogLogic,
    FinderDialogBase,
    ReplaceDialogBase,
    ReplaceDialogLogic,
)


class _TableWidgetInnerLogic:
    """
    Provides the core logic and functionality for the TableWidget.

    This class manages interactions, data manipulation, and UI elements
    such as context menus, drag-and-drop, and find/replace dialogs for
    a given QTableWidget instance.

    It acts as a controller, separating the logical operations from the visual representation.
    """

    def __init__(self, table_widget: QTableWidget):
        self.table_widget: QTableWidget = table_widget

        self.replace_dialog = ReplaceDialogBase(self.table_widget)
        self.replace_logic = ReplaceDialogLogic(self.replace_dialog, self)

        self.finder_dialog = FinderDialogBase(self.table_widget)
        self.finder_logic = FindDialogLogic(self.finder_dialog, self)

        self.__setup_shortcuts()
        logger.debug("Initialized _TableWidgetInnerLogic with table_widget")

    def drop_event_logic(self, event) -> None:
        """
        Handles the logic for drag and drop events within the table.

        Moves selected rows to the target drop location, maintaining
        the order of the moved rows.

        Args:
            event (QDropEvent): The drop event object.
        """
        logger.debug("Handling drop event")
        if event.source() == self.table_widget:
            mapping = dict()
            rows = set([mi.row() for mi in self.table_widget.selectedIndexes()])
            pos: QPoint = event.position().toPoint()
            target: int = self.table_widget.indexAt(pos).row()

            rows.discard(target)
            rows = sorted(rows)

            if not rows:
                logger.debug("No rows to move")
                return

            if target == -1:
                target = self.table_widget.rowCount()

            if rows[0] < target:
                target += 1

            for _ in range(len(rows)):
                self.table_widget.insertRow(target)

            for idx, row in enumerate(rows):
                if row < target:
                    mapping[row] = target + idx
                else:
                    mapping[row + len(rows)] = target + idx

            for src, tgt in sorted(mapping.items()):
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.takeItem(src, col)
                    if item:
                        self.table_widget.setItem(tgt, col, item)

            for row in reversed(sorted(mapping.keys())):
                self.table_widget.removeRow(row)

            event.accept()
            logger.info(f"Rows moved to target {target}")


    @staticmethod
    def __action_connect(parent, slot, label) -> QAction:
        """
        Creates and connects a QAction to a given slot.

        Args:
            parent (QWidget): The parent widget for the action.
            slot (callable): The function to connect to the action's triggered signal.
            label (str): The text label for the action.

        Returns:
            QAction: The created and connected QAction.
        """
        action = QAction(label, parent)
        action.triggered.connect(slot)
        return action

    def __add_row(self, row=None, above=True):
        """
        Adds a new row to the table.

        Args:
            row (int, optional): The index of the row relative to which the new row will be added.
                                 If None, the row is added at the end. Defaults to None.
            above (bool, optional): If True, the new row is inserted above the specified row.
                                   If False, it's inserted below. Defaults to True.
        """
        if row is None:
            rowCount = self.table_widget.rowCount()
            self.table_widget.insertRow(rowCount)
            logger.info(f"Added row at end, new row count: {rowCount + 1}")
        else:
            if above:
                self.table_widget.insertRow(row)
                logger.info(f"Added row above row {row}")
            else:
                self.table_widget.insertRow(row + 1)
                logger.info(f"Added row below row {row}")

    def __remove_row(self, row=None):
        """
        Removes a row from the table.
        Args:
            row (int, optional): The index of the row to remove.
            If None, the last row is removed. Defaults to None.
        """
        if row is None:
            if self.table_widget.rowCount() > 0:
                self.table_widget.removeRow(self.table_widget.rowCount() - 1)
                logger.info(f"Removed last row, new row count: {self.table_widget.rowCount()}")
        else:
            if self.table_widget.rowCount() > 0:
                self.table_widget.removeRow(row)
                logger.info(f"Removed row {row}, new row count: {self.table_widget.rowCount()}")
    def __setup_shortcuts(self):
        """
        Configures keyboard shortcuts for table operations.
        You can set shortcuts in json file blackbox/app/static/namespace/shortcuts.json
        Access values from this file using dot.notation
        """
        logger.debug("Setting up shortcuts")

        t = self.table_widget

        # Mapping of shortcut keys to their corresponding methods
        # use dot.notation here
        shortcuts = {
            'table.add_column_after': self._add_col_after,
            'table.add_column_before': self._add_col_before,
            'table.remove_column': self._remove_col,
            'table.add_row_above': self._add_row_above,
            'table.add_row_below': self._add_row_below,
            'table.remove_row': self._remove_row,
            'table.replace': self.replace_dialog.show,
            'table.find': self.finder_dialog.show
        }

        # Loop through the mapping and register shortcuts
        for key, method in shortcuts.items():
            shortcut_key = shortcut(key)
            shortcut_instance = QShortcut(QKeySequence(shortcut_key), t)
            shortcut_instance.activated.connect(method)

    def _add_row_above(self):
        current_row = self.table_widget.currentRow()
        self.__add_row(current_row, above=True)
        logger.debug(f"Shortcut activated: add row above {current_row}")

    def _add_row_below(self):
        current_row = self.table_widget.currentRow()
        self.__add_row(current_row, above=False)
        logger.debug(f"Shortcut activated: add row below {current_row}")

    def _remove_row(self):
        current_row = self.table_widget.currentRow()
        self.__remove_row(current_row)
        logger.debug(f"Shortcut activated: remove row {current_row}")

    def _add_col_after(self):
        current_col = self.table_widget.currentColumn()
        self.__add_column(current_col, before=False)
        logger.debug(f"Shortcut activated: add column after {current_col}")

    def _add_col_before(self):
        current_col = self.table_widget.currentColumn()
        self.__add_column(current_col)
        logger.debug(f"Shortcut activated: add column before {current_col}")

    def _remove_col(self):
        current_col = self.table_widget.currentColumn()
        self.__remove_column(current_col)
        logger.debug(f"Shortcut activated: Removing column {current_col}")

    def handle_data_loaded(self, df: pd.DataFrame):
        """
        Populates the table widget with data from a pandas DataFrame.
        Sets the row and column counts, headers, and item values based
        on the DataFrame's structure and content.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to display.
        """
        logger.debug("Loading data into table")
        headers = df.columns.values.tolist()

        self.table_widget.setRowCount(len(df))
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(i, j, item)

        logger.info("Data loaded into table from DataFrame")

    def show_context_menu(self, pos):
        """
        Displays the custom context menu for the table.
        The menu provides options to remove the current row/column or add new rows/columns
        above/below or before/after the current row/column.

        Args:
            pos (QPoint): The position where the context menu is requested.
        """
        SEPARATOR_INDEX = 3
        logger.debug("Showing context menu")
        index = self.table_widget.indexAt(pos)
        if not index.isValid():
            return

        menu = QMenu(self.table_widget)

        # Action configuration
        # Use dot.notation for accessing labels from blackbox/app/static/namespace/en_labels.json
        action_map = {
            # Row Actions
            'table_context_menu.remove': (lambda: self.__remove_row(index.row())),
            'table_context_menu.add_above': (lambda: self.__add_row(index.row(), above=True)),
            'table_context_menu.add_below': (lambda: self.__add_row(index.row(), above=False)),

            # Column Actions
            'table_context_menu.remove_column': (lambda: self.__remove_column(index.column())),
            'table_context_menu.add_column_before': (lambda: self.__add_column(index.column(), before=True)),
            'table_context_menu.add_column_after': (lambda: self.__add_column(index.column(), before=False))
        }

    # Dynamically create actions and add to menu
        for idx, action_key in enumerate(action_map.keys()):
            if idx == SEPARATOR_INDEX:
                menu.addSeparator()
            menu.addAction(self.__create_action(action_key, action_map[action_key]))

        menu.exec(self.table_widget.viewport().mapToGlobal(pos))
        logger.info("Context menu displayed")

    def __create_action(self, label_key, slot):
        """
        Creates a QAction connected to the specified slot.

        Args:
            label_key (str): The dot-separated key for the label in the JSON.
            slot (callable): The function to call when the action is triggered.

        Returns:
            QAction: The created action.
        """
        label_text = label(label_key)
        return self.__action_connect(parent=self.table_widget, slot=slot, label=label_text)


    def __add_column(self, col=None, before=True):
        """
        Adds a new column to the table.

        Args:
            col (int, optional): The index of the column relative to which the new column will be added.
                                If None, the column is added at the end. Defaults to None.
            before (bool, optional): If True, the new column is inserted before the specified column.
                                    If False, it's inserted after. Defaults to True.
        """
        if col is None:
            col = self.table_widget.columnCount()
        
        insert_at = col if before else col + 1
        self.table_widget.insertColumn(insert_at)

        # Optional: Set header label for the new column
        self.table_widget.setHorizontalHeaderItem(insert_at, QTableWidgetItem(f"Column {insert_at + 1}"))
        logger.info(f"Added column at index {insert_at}")

    def __remove_column(self, col=None):
        """
        Removes a column from the table.

        Args:
            col (int, optional): The index of the column to remove.
                                If None, the last column is removed. Defaults to None.
        """
        if col is None:
            col = self.table_widget.columnCount() - 1
        
        if col >= 0 and self.table_widget.columnCount() > 0:
            self.table_widget.removeColumn(col)
            logger.info(f"Removed column at index {col}")



class TableWidget(QTableWidget):
    """
    A custom QTableWidget with enhanced functionalities such as drag-and-drop
    row reordering, a context menu for row manipulation, and keyboard shortcuts
    for common table operations.

    This widget integrates the logic provided by the _TableWidgetInnerLogic
    to handle these features.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        
        _select = QAbstractItemView.SelectionMode.ExtendedSelection
        _behv = QAbstractItemView.SelectionBehavior.SelectRows
        _dnd = QAbstractItemView.DragDropMode.InternalMove
        self.setSelectionMode(_select)
        self.setSelectionBehavior(_behv)
        self.setDragDropMode(_dnd)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.logic = _TableWidgetInnerLogic(self)


    def dropEvent(self, event):
        """
        Overrides the default dropEvent to use the custom drag-and-drop logic.

        Args:
            event (QDropEvent): The drop event object.
        """
        self.logic.drop_event_logic(event)

    def show_context_menu(self, pos):
        """
        Overrides the default show_context_menu to use the custom context menu logic.

        Args:
            pos (QPoint): The position where the context menu is requested.
        """
        self.logic.show_context_menu(pos)

    def handle_data_loaded(self, df: pd.DataFrame):
        """
        A convenience method to load data into the table using the internal logic.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to display.
        """
        self.logic.handle_data_loaded(df)
