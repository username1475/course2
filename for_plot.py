from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np
from scipy.interpolate import interp1d, CubicSpline
import approximations as approx


class Graph:
    def __init__(self, data, methods):
        self._data = data
        self._plot = None
        self._methods = methods
        self.interpolate()

    def interpolate(self):
        x = self._data['x'].tolist()
        y = self._data['y'].tolist()
        sorted_indices = np.argsort(x)
        x = np.take(x, sorted_indices)
        y = np.take(y, sorted_indices)

        self._plot = pg.PlotWidget()
        self._plot.addLegend(offset=(500, 10))

        self._plot.plot(x, y, name='data points', pen=pg.mkPen(color=(255, 245, 250)),
                        symbol="d", symbolSize=15,  symbolBrush=(245, 132, 192))

        x_new = np.linspace(np.min(x), np.max(x), 1000)

        for method in self._methods:
            print(method)
            match method:
                case 'lagrange':
                    pen = pg.mkPen(color=(242, 53, 88), width=1.5)
                    y_new = [approx.Lagranz(x, y, i) for i in x_new]
                    self.plot_line('Лагранж', x_new, y_new, pen)

                case 'newton':
                    pen = pg.mkPen(color=(69, 53, 242), width=1.5)
                    a_s = approx.divided_diff(x, y)[0, :]
                    y_new = approx.newton_poly(a_s, x, x_new)
                    self.plot_line('Ньютон', x_new, y_new, pen)
                case 'lsm':
                    pen = pg.mkPen(color=(48, 189, 26), width=1.5)
                    coefficients = np.polyfit(x, y, 2)
                    poly = np.poly1d(coefficients)
                    y_new = poly(x_new)
                    self.plot_line('мнк', x_new, y_new, pen)
                case 'linear_spline':
                    pen = pg.mkPen(color=(47, 192, 244), width=1.5)
                    y_linear = interp1d(x, y)
                    y_new = y_linear(x_new)
                    self.plot_line('лин сплайн', x_new, y_new, pen)
                case 'quadratic_spline':
                    pen = pg.mkPen(color=(136, 47, 204), width=1.5)
                    y_linear = interp1d(x, y, kind='quadratic')
                    y_new = y_linear(x_new)
                    self.plot_line('кв сплайн', x_new, y_new, pen)
                case 'cubic_spline':
                    pen = pg.mkPen(color=(235, 168, 0), width=1.5)
                    y_linear = interp1d(x, y, kind='cubic')
                    y_new = y_linear(x_new)
                    self.plot_line('куб сплайн', x_new, y_new, pen)
                case 'cubic_spline_BC':
                    pen = pg.mkPen(color=(0, 0, 0), width=1.5)
                    y_linear = CubicSpline(x, y, bc_type='natural')
                    y_new = y_linear(x_new)
                    self.plot_line('куб сплайн2', x_new, y_new, pen)

    def plot_line(self, name, x, y, pen):
        self._plot.plot(
            x,
            y,
            name=name,
            pen=pen,
            style=QtCore.Qt.PenStyle
        )
