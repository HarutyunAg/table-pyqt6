import pandas as pd
from blackbox.app.static import label, shortcut
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMenuBar, QFileDialog


class FileMenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.__setup()

    def __setup(self):
        save_cut: str = shortcut('bar.file_menu.save')
        upload_cut: str = shortcut('bar.file_menu.upload')
        
        save_label: str = label('bar.file_menu.save')
        upload_label: str = label('bar.file_menu.upload')
        file_menu_label: str = label('bar.file_menu.menu_name')
        

        file_menu = self.addMenu(file_menu_label)

        upload_action: QAction = self.__action_connect(self, self.__upload, upload_label)
        save_action: QAction = self.__action_connect(self, self.__save, save_label)

        upload_action.setShortcut(QKeySequence(upload_cut))
        save_action.setShortcut(QKeySequence(save_cut))

        file_menu.addAction(upload_action)
        file_menu.addAction(save_action)

    def __action_connect(self, parent, slot, label: str) -> QAction:
        action = QAction(label, parent)
        action.triggered.connect(slot)
        return action

    def __upload(self):
        return self.parent.loader_menu_widget.load_from_menu()

    def __save(self):
        path, _ = QFileDialog.getSaveFileName(self.parent,
                                              "Сохранить", "",
                                              "Excel Files (*.xlsx *.xls);;All Files (*)")
        if not path:
            return 

        columns = []
        for j in range(self.parent.table_widget.model().columnCount()):
            columns.append(self.parent.table_widget.horizontalHeaderItem(j).text())

        df = pd.DataFrame(columns=columns)

        for row in range(self.parent.table_widget.rowCount()):
            for col in range(self.parent.table_widget.columnCount()):
                df.at[row, columns[col]] = self.parent.table_widget.item(row, col).text()

        df.to_excel(path, index=False)
