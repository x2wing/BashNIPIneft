from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QWidget, QVBoxLayout


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        """ начальная настройка и размещение на форме"""

        super(MatplotlibWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)

    def draw_plot(self, x, y):
        """ функция отрисовка графика"""

        # очищаем график
        self.axis.clear()
        # устанавливаем значения для рисования
        self.axis.plot(x, y)
        # отрисовка графика
        self.canvas.draw()
