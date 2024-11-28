import sys
import pandas as pd

from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtWidgets import QMessageBox

from PandasModel_new import PandasModel, SortFilterProxyModel
from MainWindow_new import Ui_MainWindow
from dialog import Dialog
from for_plot import Graph

import numpy as np
import approximations as approx


class App(QtWidgets.QMainWindow):
    dialog_params = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.changeSkinPink()
        self._ui.tableView.setSortingEnabled(True)
        self._data = pd.read_excel('2.xlsx')
        self.__set_table()
        self.__add_callbacks()

    def __set_table(self):
        self._model = PandasModel(self._data)

        proxy_model = SortFilterProxyModel()
        proxy_model.setSourceModel(self._model)

        # print(self._model._data)
        # self._data = self._model._data
        self._ui.tableView.setModel(proxy_model)

    def __add_callbacks(self):
        self._ui.filter_button.clicked.connect(self.__open_filter_dialog)
        self.dialog_params.connect(self.__get_params_from_dialog)
        self._ui.lineEdit.returnPressed.connect(self.__read_source)
        self._ui.filter_button2.clicked.connect(self.__read_dot)
        self._ui.button_plus_row.clicked.connect(self.__plus_row)
        self._ui.button_minus_row.clicked.connect(self.__minus_row)

    def __get_params_from_dialog(self, value):
        print(value)

    def __open_filter_dialog(self):
        x = self._data['x'].tolist()
        y = self._data['y'].tolist()
        if len(set(x)) != len(x):
            msg = QMessageBox()
            msg.setWindowTitle("внимание °˖𓍢ִ໋🌷͙֒✧°.🎀༘⋆")
            msg.setText("табличная функция выглядит неправильно :(")
            app_icon = QtGui.QIcon("hamster.jpeg")
            msg.setWindowIcon(app_icon)
            X = msg.exec_()
        else:
            self.__read_methods()
            self._graph = Graph(self._data, self._methods)
            self._graph.interpolate()
            self.dialog = Dialog(self.dialog_params, self._graph)
            self.dialog.show()
        self._data = self._model._data
        self.__set_table()

    def __plus_row(self):
        self._model.insertRows(int(self._model.rowCount())-1, 1)
        self._data = self._model._data
        # self._model.insertColumns(int(self._model.columnCount())-1, 1)
        # self._model.removeRows(int(self._model.rowCount()), 1)
        # self._model.removeColumns(int(self._model.columnCount()), 1)
        # self.__set_table()

    def __minus_row(self):
        # self._model.insertRows(int(self._model.rowCount())-1, 1)
        # self._model.insertColumns(int(self._model.columnCount())-1, 1)
        self._model.removeRows(int(self._model.rowCount()), 1)
        # self._model.removeColumns(int(self._model.columnCount()), 1)
        self._data = self._model._data
        # self.__set_table()

    def __read_source(self):
        print(self._ui.lineEdit.text())
        new_data = self._ui.lineEdit.text()
        if isinstance(new_data, str) and new_data.endswith('.xlsx'):
            self._data = pd.read_excel(new_data)
            self.__set_table()

    def __read_dot(self):
        special_dot = None
        special_dot_2 = None
        try:
            special_dot = float(self._ui.lineEdit_for_dot.text())
        except ValueError:
            self._ui.lineEdit_for_dot.setText('цифру напишите >:(')
        method = self._ui.comboBox.currentText()  # здесь другое мб лучше
        x = self._data['x'].tolist()
        y = self._data['y'].tolist()
        if len(set(x)) != len(x):
            msg = QMessageBox()
            msg.setWindowTitle("внимание")
            msg.setText("табличная функция выглядит неправильно :(")
            app_icon = QtGui.QIcon("hamster.jpeg")
            msg.setWindowIcon(app_icon)
            X = msg.exec_()
        else:
            match method:
                case '  полиномом Лагранжа':
                    special_dot_2 = approx.Lagranz(x, y, special_dot)
                case '  полиномом Ньютона':
                    a_s = approx.divided_diff(x, y)[0, :]
                    special_dot_2 = approx.newton_poly(a_s, x, special_dot)
                case "  метод наименьших квадратов":
                    coefficients = np.polyfit(x, y, 2)
                    poly = np.poly1d(coefficients)
                    special_dot_2 = poly(special_dot)

            self._ui.label_for_dot.setText(str(special_dot_2))

    def __read_methods(self):
        self._methods = []
        if self._ui.checkBox_lagrange.isChecked():
            self._methods.append('lagrange')
        if self._ui.checkBox_newton.isChecked():
            self._methods.append('newton')
        if self._ui.checkBox_lsm.isChecked():
            self._methods.append('lsm')
        if self._ui.checkBox_linear_spline.isChecked():
            self._methods.append('linear_spline')
        if self._ui.checkBox_quadratic_spline.isChecked():
            self._methods.append('quadratic_spline')
        if self._ui.checkBox_cubic_spline.isChecked():
            self._methods.append('cubic_spline')
        if self._ui.checkBox_cubic_spline_BC.isChecked():
            self._methods.append('cubic_spline_BC')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = App()
    main_window.show()
    app.exec()
