# from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import (Qt, QVariant, QAbstractTableModel, QModelIndex, QObject, pyqtSignal)


class Communicate(QObject):
    """ класс сигнала изменения данных"""
    data_changed = pyqtSignal(QModelIndex, QModelIndex)


class Overflow(QObject):
    overflow = pyqtSignal(QModelIndex, QModelIndex)


class Model(QAbstractTableModel):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.c = Communicate()
        self.overflow = Overflow()
        # генератор списка названий заголовков столбцов
        # ['Column 1', 'Column 2', 'Column 3', ...] +
        # ['Сумма строки', 'Накопленная сумма']
        self.header_labels = [f'Data {col_num}'
                              for col_num in range(1, self.table.shape[1] - 1)] \
                             + ['Сумма строки', 'Накопленная сумма']

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # отрисовка заголовков стобцов
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.table.shape[0]  # свойство numpy array shape - кортеж размерностей (длина, ширина)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.table.shape[1]  # свойство numpy array shape - кортеж размерностей (длина, ширина)

    def flags(self, index):
        # установим флаги модели редактриуемость, включенность, выделяемость
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index: QModelIndex, role: int) -> QVariant:
        # проверка значения на валидность
        if not index.isValid():
            return QVariant()
        # номер строки и столца
        r = index.row()
        c = index.column()
        # получаем значения из исходного numpy array
        value = str(self.table[r][c])

        # раскраска ячеек функция fill_color выводи цвет ячейки
        # красный - отрицательное  желтый - 0 зеленый - положительное
        if role == Qt.BackgroundColorRole:
            return self.fill_color(value)

        # выдаем значение в модель из исходного numpy array
        if role == Qt.DisplayRole:
            return QVariant(str(self.table[index.row()][index.column()]))

    def setData(self, index: QModelIndex, value: QVariant, role: int) -> bool:
        # при изменении значения в таблице записываем значени в исходный numpy array
        if role == Qt.EditRole:
            # сохраним текущее значение
            temp_data = self.table[index.row()][index.column()]
            try:
                self.table[index.row()][index.column()] = float(value)
            except ValueError:
                self.table[index.row()][index.column()] = temp_data  # при не валидном значении вернем временное
            except OverflowError:
                self.overflow.overflow.emit(index, index)  # выкинем сигнал о слишко большом введеном значении
                self.table[index.row()][index.column()] = temp_data  # при не валидном значении вернем временное
            self.c.data_changed.emit(index, index)
        return True

    def fill_color(self, value):

        """ функция возвращает значение цвета в зависимости от значения value
            красный - отрицательное,
            желтый - 0,
            зеленый - положительное
        """

        if float(value) < 0:
            return QVariant(QColor(Qt.red))
        elif float(value) == 0:
            return QVariant(QColor(Qt.yellow))
        else:
            return QVariant(QColor(Qt.green))
