from PyQt5 import QtWidgets
import numpy as np
# import h5py


# импорт модулей проекта
from delegate import Delegate
from model import Model
from MatplotlibWidget import MatplotlibWidget
from backend import Backend
from iof import Save, Load

# генерация исходных данных
np.set_printoptions(suppress=True, precision=3)
raw_data = np.random.randint(-100, 100, (8, 7))


class Main(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Варианты выбора для ячеек с Combobox
        choices = ['0', '1', '2', '3', '4', '5']
        # номер столбца с QComboBox
        cbox_column = 1

        # Получение данные через класс Backend
        self.backend = Backend(raw_data, 8, 4)
        # Вычисление столбца суммы и накопления
        self.backend.recalculate()
        # Получение ссылки на numpy array
        self.backend_data = self.backend.get_data()

        # Создание модели
        self.model = Model(self.backend_data)
        # изменение данных в модели вызывет перерасчет через метод recalc
        self.model.c.data_changed.connect(self.recalc)

        # создание виджетов таблицы
        self.table_data = QtWidgets.QTableView()
        # подключиние модели к таблице
        self.table_data.setModel(self.model)
        # Установка делегата на второй столбец таблицы
        self.table_data.setItemDelegateForColumn(cbox_column, Delegate(self, choices))
        # получаем модель выделения
        self.selectionModel = self.table_data.selectionModel()
        # событие происходящее выделением столбца целчком по шапке таблицы
        self.table_data.horizontalHeader().sectionClicked.connect(self.draw_graph)

        # сделать Combobox редактируемым одним щелчком во 2(1) столбце
        for row in range(self.backend_data.shape[0]):
            self.table_data.openPersistentEditor(self.model.index(row, cbox_column))

        # создаем виджет графика
        self.matplotlib_widget = MatplotlibWidget(self)

        # Создать кнопки и повесить на них события
        btnLoad = QtWidgets.QPushButton('Load')
        btnSave = QtWidgets.QPushButton('Save')
        btnSave.clicked.connect(lambda: Save()(self.backend_data))
        btnLoad.clicked.connect(self.load_data)

        # btnSave.clicked.connect(app.exit)
        # создаем лайаут для вертикального размещения виджетов
        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        # добавляем виджеты в лайаут
        self.layoutVertical.addWidget(self.table_data)
        self.layoutVertical.addWidget(btnLoad)
        self.layoutVertical.addWidget(btnSave)

        self.layoutVertical.addWidget(self.matplotlib_widget)
        # x = [1, 2, 3, 4, 5]
        # y = [10, 20, 30, 40, 50]
        # self.matplotlib_widget.draw_plot(x, y)

        self.setWindowTitle('Тестовое задание')
        self.setGeometry(50, 50, 800, 800)
        self.show()

    def draw_graph(self):

        """Фильтрует выделение и вызывает отрисовку """

        # Получение индексов выделенных столбцов
        indexes = self.selectionModel.selectedIndexes()
        # Получаем множество из уникальных номеров столбцов
        indexes_selected_column = set((int(data.column()) for data in indexes))
        # Если выделено ровно 2 столбца то вытаскиваем их
        #  данные из numpy array и передаем в отрисовщик
        if len(indexes_selected_column) == 2:
            c1, c2 = sorted(indexes_selected_column)
            x = self.backend_data[..., c1]
            y = self.backend_data[..., c2]
            self.matplotlib_widget.draw_plot(x, y)

    def recalc(self):

        """ перерасчет столбца сумм и накопленя в исходном numpy array"""

        self.backend.recalculate()

    def load_data(self):
        Load()(self.backend_data)
        # self.model.dataChanged()
        self.model.endResetModel()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    app.exec_()
