import random

from PyQt5 import QtCore, Qt
import pandas as pd
from PyQt5.QtCore import QModelIndex, QSortFilterProxyModel


class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()

    # TODO разобраться с фильтрацией

    def sort(self, column, order = ...):
        print('сорт работает')
        if order == QtCore.Qt.SortOrder.AscendingOrder:
            check = True
        else:
            check = False
        local_data = self.sourceModel()._data
        local_data = local_data.sort_values(by=local_data.columns[column], ascending=check)
        print(local_data.columns[column], check)
        # print(self.data)

        self.sourceModel()._data = local_data
        self.sourceModel().layoutChanged.emit()

        # return True

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        left_data = self.sourceModel().data(left)
        right_data = self.sourceModel().data(right)
        if left_data is None:
            return True
        elif right_data is None:
            return True
        # elif left_data < right_data:
        #     return left_data < right_data
        else:
            return int(left_data) < int(right_data)
        # else:
        #     return left_data > right_data


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self._data = data

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.values)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self._data.columns.size

    '''
    def insertColumn(self, column, parent = ...):
        pass
    '''

    def insertColumns(self, column, count, parent = ...):
        self.beginInsertColumns(QtCore.QModelIndex(), column, column+count-2)
        for j in range(count):
            self._data[str(random.randint(0, 1000))] = [0 for i in range(len(self._data.values))]
        self.layoutChanged.emit()
        self.endInsertColumns()

    def insertRows(self, row, count, parent=...):
        self.beginInsertRows(QtCore.QModelIndex(), row, row + count-2)
        for j in range(count):
            self._data.loc[len(self._data.index)] = [0 for i in range(self._data.columns.size)]
        self.layoutChanged.emit()
        self.endInsertRows()

    def removeColumns(self, column, count, parent = ...):
        self.beginRemoveColumns(QtCore.QModelIndex(), column, column+count-1)
        for j in range(count):
            del self._data[self._data.columns[-1]]
        self.layoutChanged.emit()
        self.endRemoveColumns()

    def removeRows(self, row, count, parent = ...):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row+count-1)
        for j in range(count):
            # del self.__data.loc[int(len(self.__data.index)-1)]
            self._data = self._data.iloc[:len(self._data.index) - 1] # поч не сохраняется..
            # self.__data = self.__data.drop(int(len(self.__data.index)-1))
        self.layoutChanged.emit()
        self.endRemoveRows()

    def data(self, index: QModelIndex, role: int = ...):
        if index.isValid():
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                # QtCore.Qt.DisplayRole
                return str(self._data.values[index.row()][index.column()])
        else:
            return None

    def headerData(self, section: int, orientation, role: int = ...):
        if orientation == QtCore.Qt.LayoutDirection.RightToLeft and role == QtCore.Qt.ItemDataRole.DisplayRole:
            # QtCore.Qt.Horizontal
            # QtCore.Qt.DisplayRole
            return str(self._data.columns[section])
        else:
            return None

    def setData(self, index: QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        if role != QtCore.Qt.ItemDataRole.EditRole:
            # QtCore.Qt.EditRole
            return False
        row = index.row()
        if (row < 0) and (row >= len(self._data.values)):
            return False
        column = index.column()
        if (column < 0) and (column >= self._data.columns.size):
            return False
        if not value:
            value = 0
            return False
        self._data.values[row][column] = float(value)
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index: QModelIndex):
        flags = QtCore.Qt.ItemFlag.ItemIsEditable | QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled
        return flags
