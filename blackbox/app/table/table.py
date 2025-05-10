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


class TableWidgetLogic:
    def __init__(self, table_widget):
        self.table_widget = table_widget

        self.replace_dialog = ReplaceDialogBase(self.table_widget)
        self.replace_logic = ReplaceDialogLogic(self.replace_dialog, self)

        self.finder_dialog = FinderDialogBase(self.table_widget)
        self.finder_logic = FindDialogLogic(self.finder_dialog, self)

        self.__setup_shortcuts()
        logger.debug("Initialized TableWidgetLogic with table_widget")

    def drop_event_logic(self, event):
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

    def show_context_menu(self, pos):
        logger.debug("Showing context menu")
        index = self.table_widget.indexAt(pos)
        if index.isValid():
            remove_label = label('table_context_menu.remove')
            above_label = label('table_context_menu.add_above')
            below_label = label('table_context_menu.add_below')

            menu = QMenu(self.table_widget)

            remove_row: QAction = self.__action_connect(
                self.table_widget,
                lambda: self.__remove_row(index.row()),
                remove_label
                )

            add_row_below: QAction = self.__action_connect(
                self.table_widget,
                lambda: self.__add_row(index.row(), above=False),
                below_label
                )

            add_row_above: QAction = self.__action_connect(
                self.table_widget,
                lambda: self.__add_row(index.row(), above=True),
                above_label
                )

            menu.addAction(remove_row)
            menu.addAction(add_row_above)
            menu.addAction(add_row_below)

            menu.exec(self.table_widget.viewport().mapToGlobal(pos))
            logger.info("Context menu displayed")

    def __action_connect(parent, slot, label) -> QAction:
        action = QAction(label, parent)
        action.triggered.connect(slot)
        return action

    def __add_row(self, row=None, above=True):
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
        if row is None:
            if self.table_widget.rowCount() > 0:
                self.table_widget.removeRow(self.table_widget.rowCount() - 1)
                logger.info(f"Removed last row, new row count: {self.table_widget.rowCount()}")
        else:
            if self.table_widget.rowCount() > 0:
                self.table_widget.removeRow(row)
                logger.info(f"Removed row {row}, new row count: {self.table_widget.rowCount()}")

    def __setup_shortcuts(self):
        
        find_cut: str = shortcut('table.find')
        replace_cut: str = shortcut('table.replace')
        remove_cut: str = shortcut('table.remove_row')
        below_cut: str = shortcut('table.add_row_below')
        above_cut: str = shortcut('table.add_row_above')

        t = self.table_widget
        self.add_row_above_shortcut = QShortcut(QKeySequence(above_cut), t)
        self.add_row_below_shortcut = QShortcut(QKeySequence(below_cut), t)
        self.remove_row_shortcut = QShortcut(QKeySequence(remove_cut), t)
        self.replace_shortcut = QShortcut(QKeySequence(replace_cut), t)
        self.find_shortcut = QShortcut(QKeySequence(find_cut), t)

        logger.debug("Setting up shortcuts")
        self.add_row_above_shortcut.activated.connect(self._add_row_above)
        self.add_row_below_shortcut.activated.connect(self._add_row_below)
        self.remove_row_shortcut.activated.connect(self._remove_row)
        self.replace_shortcut.activated.connect(self.replace_dialog.show)
        self.find_shortcut.activated.connect(self.finder_dialog.show)

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

    def handle_data_loaded(self, df: pd.DataFrame):
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


class TableWidget(QTableWidget):
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

        self.logic = TableWidgetLogic(self)

    def dropEvent(self, event):
        self.logic.drop_event_logic(event)

    def show_context_menu(self, pos):
        self.logic.show_context_menu(pos)

    def handle_data_loaded(self, df: pd.DataFrame):
        self.logic.handle_data_loaded(df)
