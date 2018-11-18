from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph as pg

# импорт модулей проекта
from delegate import Delegate
from model import Model
from backend import Backend
from iof import Save, Load
from config import YAML_config
from dialog import File_Dialog

# генерация исходных данных
np.set_printoptions(suppress=True, precision=3)
raw_data = np.random.randint(-100, 100, (8, 8))
row_n = raw_data.shape[0]  # число строк в numpy массиве исходных данных
col_n = raw_data.shape[1]  # число столбцов в numpy массиве исходных данных

config_file = "config.yaml"


class Main(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # создание класса работы с конфигом
        self.config = YAML_config(config_file)
        # Варианты выбора для ячеек с Combobox
        choices = ['0', '1', '2', '3', '4', '5']
        # номер столбца с QComboBox
        cbox_column = 1

        # Получение данные через класс Backend
        self.backend = Backend(raw_data, row_n - 1, col_n - 3)
        # Вычисление столбца суммы и накопления
        self.backend.recalculate()
        # Получение ссылки на numpy array
        self.backend_data = self.backend.get_data()

        # Создание модели
        self.model = Model(self.backend_data)
        # изменение данных в модели вызывет перерасчет через метод recalc
        self.model.c.data_changed.connect(self.recalc)
        self.model.overflow.overflow.connect(self.overflow)

        # создание виджетов таблицы
        self.table_data = QtWidgets.QTableView()
        # изменение значеняи ячейки одинарным щелчком
        self.table_data.setEditTriggers(QtWidgets.QAbstractItemView.CurrentChanged)
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

        # создаем виджет графика graph - виджет на форме plot - график отрисованный на виджете
        graph = pg.PlotWidget(nama='graph')  # pyqtgraph
        self.plot = graph.plot()

        # Создать кнопки и повесить на них события
        btnLoad = QtWidgets.QPushButton('Load')
        btnSave = QtWidgets.QPushButton('Save')
        # Кнопка выбора загружаемого hdf5 файла
        btnLoadFromFile = QtWidgets.QPushButton('Load from file')
        # Кнопка выбора загружаемого hdf5 из списка
        btnLoadFromList = QtWidgets.QPushButton('Load from list')
        # Кнопак выбора пути сохранения файла
        btnSaveToFile = QtWidgets.QPushButton('Save to file')

        btnLoad.clicked.connect(self.load_data)
        btnSave.clicked.connect(lambda: Save()(self.backend_data))
        btnSaveToFile.clicked.connect(self.save_to_file)
        # Список рабочих hdf5 файлов
        cmbFilesList = QtWidgets.QComboBox(self)
        # создаем лайаут для вертикального размещения виджетов
        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        # добавляем виджеты в лайаут
        self.layoutVertical.addWidget(self.table_data)
        self.layoutVertical.addWidget(btnLoad)
        self.layoutVertical.addWidget(btnSave)
        self.layoutVertical.addWidget(btnLoadFromFile)
        self.layoutVertical.addWidget(btnLoadFromList)
        self.layoutVertical.addWidget(btnSaveToFile)
        self.layoutVertical.addWidget(cmbFilesList)

        self.layoutVertical.addWidget(graph)

        self.setWindowTitle('Тестовое задание')
        self.setGeometry(50, 50, 1000, 800)
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
            self.plot.setData(x, y)

    def recalc(self):

        """ перерасчет столбца сумм и накопления в исходном numpy array"""

        self.backend.recalculate()

    def load_data(self):
        Load()(self.backend_data)
        # self.model.dataChanged()
        self.model.endResetModel()

    def overflow(self):
        QtWidgets.QMessageBox.information(self, 'Переполнение', "Слишком большое значение. Необходимо исправить")

    def save_to_file(self):

        path = File_Dialog.get_save_filepath(self)
        print(path, config_file, row_n, col_n)
        self.config.save(config_file, {path: (row_n, col_n)})


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    app.exec_()
