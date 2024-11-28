from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import numpy as np


class Dialog(QtWidgets.QDialog):
    def __init__(self, params_signal, graph_data):
        super().__init__()
        self.setWindowTitle('посмотрите на картинку!!')
        app_icon = QtGui.QIcon("smile.png")
        self.setWindowIcon(app_icon)
        self.setWhatsThis('ну предположительно это график..')
        self.setSizeGripEnabled(True)
        self.setModal(True)

        self.dialog_layout = QtWidgets.QVBoxLayout(self)

        self.plot = graph_data._plot
        self.plot.setBackground((255, 245, 250))
        self.plot.getAxis('bottom').setPen(pg.mkPen(color=(245, 132, 192)))
        self.plot.showGrid(x=True, y=True,)

        self.dialog_layout.addWidget(self.plot)

        self.btn = QtWidgets.QPushButton('похоже?? ну да.. ну и все')
        # self.btn.setFixedWidth(400)
        self.dialog_layout.addWidget(self.btn)

        self.setLayout(self.dialog_layout)
        self.params_signal = params_signal
        self.__add_callbacks()

    def __add_callbacks(self):
        self.btn.clicked.connect(self.__end_dialog)

    def __end_dialog(self):
        self.params_signal.emit('Hello')
        self.accept()
