import os

import pandas as pd
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QWidget

from blackbox.app.static import label


class ExcelLoader:

    def __init__(self, parent=None):
        self.parent = parent

    def read_excel(self, path) -> pd.DataFrame:
        try:
            df = pd.read_excel(path, dtype=str)
            return df
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return pd.DataFrame()

    def load_file_dialog(self) -> str:
        directory: str = os.getcwd()
        initial_filter: str = 'Excel File (*.xlsx *.xls)'
        dialog_label: str = label('table_loader.dialog')
        file_filter: str = 'Data File (*.xlsx *.csv *.data);; Excel File (*.xlsx *.xls)'

        path, _ = QFileDialog.getOpenFileName(
            parent=self.parent,
            caption=dialog_label,
            directory=directory,
            filter=file_filter,
            initialFilter=initial_filter
        )

        return path

    def load(self) -> pd.DataFrame:
        path = self.load_file_dialog()
        if path:
            return self.read_excel(path)
        return pd.DataFrame()


class LoaderWidgetBase(QWidget):

    data_loaded = pyqtSignal(pd.DataFrame)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.excel_loader = ExcelLoader(self)

    def load(self) -> pd.DataFrame:
        df = self.excel_loader.load()
        if not df.empty:
            self.data_loaded.emit(df)
            return df
        return pd.DataFrame()


class LoaderFromMenuWidget(LoaderWidgetBase):

    def __init__(self, parent=None):
        super().__init__(parent)

    def load_from_menu(self) -> pd.DataFrame:
        return self.load()
