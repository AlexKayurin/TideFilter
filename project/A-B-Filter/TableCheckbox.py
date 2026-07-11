import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data, checked):
        super().__init__()
        self._data = data
        self._checked = checked

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            return str(value)

        if role == Qt.ItemDataRole.CheckStateRole:
            checked = self._checked[index.row()][index.column()]
            if checked:
                return Qt.CheckState.Checked
            return Qt.CheckState.Unchecked

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.CheckStateRole:
            checked = value == Qt.CheckState.Checked.value
            self._checked[index.row()][index.column()] = checked
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsUserCheckable
        )


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = [
            [1, 9, 2],
            [1, 0, -1],
            [3, 5, 2],
            [3, 3, 2],
            [5, 8, 9],
        ]

        checked = [
            [True, True, True],
            [False, False, False],
            [True, False, False],
            [True, False, True],
            [False, True, True],
        ]

        self.model = TableModel(data, checked)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()