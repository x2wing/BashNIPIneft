from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import numpy as np
import pyqtgraph as pg
import os
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeView, QAbstractItemView, QTableWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime

# импорт модулей проекта
from backend import Backend
from config import YAML_config
from delegate import Delegate
from dialog import File_Dialog
from generator import Generator_HDF5_Hierarchy
from model import Model
from iof import Save, Load
from project_metadata import Metadata
from tree_model import ProjectTree

# генерация исходных данных
np.set_printoptions(suppress=True, precision=3)
# raw_data = np.random.randint(-100, 100, (50, 50))
row_num = 8  # число строк в numpy массиве исходных данных
col_num = 8  # число столбцов в numpy массиве исходных данных
# путь к конфигу
config_file = 'config.yaml'
# абсолютный путь к hdf5 файлу по умолчанию для случая если конфиг пустой
default_db_filepath = os.path.abspath('db.hdf5')
# даные для записи в конфиг если он пуст
default_config_data = {default_db_filepath: (row_num, col_num)}

raw_data = np.zeros((row_num, col_num), dtype=float)


class Main(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # создание класса работы с конфигом
        self.config = YAML_config(config_file, default_config_data)
        # создание виджета таблицы
        self.table_data = QtWidgets.QTableView()
        # инициализация исходных данных модели и таблицы
        # вынесено в отдельную функцию для возможности именения размерности таблицы в runtime
        self.init_data_model_and_table((row_num, col_num))

        # Получение данные через класс Backend depricated
        # self.backend = Backend(raw_data, row_n - 1, col_n - 3)
        # Вычисление столбца суммы и накопления

        # Получение ссылки на numpy array depricated
        # self.backend_data = self.backend.get_data()

        # # Создание модели depricated
        # self.model = Model(self.backend_data)
        # # изменение данных в модели вызывет перерасчет через метод recalc depricated
        # self.model.c.data_changed.connect(self.recalc)
        # self.model.overflow.overflow.connect(self.overflow)

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
        # Кнопка выбора пути сохранения файла
        btnSaveToFile = QtWidgets.QPushButton('Save to file')
        btnModelChange = QtWidgets.QPushButton('Change model')

        btnGenerate = QtWidgets.QPushButton('Сгенерировать hdf5')
        btnOpenProject = QtWidgets.QPushButton('Открыть проект')
        btn_load_dset = QtWidgets.QPushButton('Открыть dataset')
        #  события нажатия кнопок
        btnLoad.clicked.connect(lambda: self.load_data())
        btnSave.clicked.connect(lambda: Save()(self.backend_data, default_db_filepath))
        btnSaveToFile.clicked.connect(self.save_to_file)
        btnLoadFromFile.clicked.connect(self.load_from_file)
        btnLoadFromList.clicked.connect(self.load_from_list)
        btnModelChange.clicked.connect(lambda: self.init_data_model_and_table((16, 16)))
        btn_load_dset.clicked.connect(self.load_dset)
        btnGenerate.clicked.connect(self.generate_datafiles)
        # Создаем раскрывающийся список рабочих hdf5 файлов
        self.cmbFilesList = QtWidgets.QComboBox(self)
        # заполняем раскрывающийся список значениями из конфига
        self.cmbFilesList.addItems(self.config.get_str_paths_list())
        # создаем иерархический список
        tv = self.fill_QTreeView()
        # создаем метку под таблицей
        self.lbl_log = QtWidgets.QLabel()
        # создаем QTableWidget для отображения методанных
        self.tw_metadata = QtWidgets.QTableWidget()
        self.tw_metadata.setColumnCount(2)

        # создаем лайауты для  размещения виджетов
        self.layoutVerticalLeft = QtWidgets.QVBoxLayout()
        self.layoutVerticalCenter = QtWidgets.QVBoxLayout()
        self.layoutVerticalRight = QtWidgets.QVBoxLayout()
        self.layoutHorizontal = QtWidgets.QHBoxLayout(self)

        # добавляем виджеты в лайаут
        self.layoutVerticalLeft.addWidget(tv)
        self.layoutVerticalLeft.addWidget(btnGenerate)
        self.layoutVerticalLeft.addWidget(btnOpenProject)

        self.layoutVerticalCenter.addWidget(self.table_data)
        self.layoutVerticalCenter.addWidget(self.lbl_log)
        self.layoutVerticalCenter.addWidget(btn_load_dset)
        self.layoutVerticalCenter.addWidget(graph)

        self.layoutVerticalRight.addWidget(self.tw_metadata, alignment=Qt.AlignBottom)
        self.layoutVerticalRight.addWidget(btnLoad)
        self.layoutVerticalRight.addWidget(btnSave)
        self.layoutVerticalRight.addWidget(btnLoadFromFile)
        self.layoutVerticalRight.addWidget(btnLoadFromList)
        self.layoutVerticalRight.addWidget(btnSaveToFile)
        self.layoutVerticalRight.addWidget(self.cmbFilesList)
        self.layoutVerticalRight.addWidget(btnModelChange)

        # добавляем вертикальные лайауты в горизонтальные
        self.layoutHorizontal.addLayout(self.layoutVerticalLeft)
        # self.layoutHorizontal.setStretch(1, 1000)
        self.layoutHorizontal.addLayout(self.layoutVerticalCenter)
        self.layoutHorizontal.addLayout(self.layoutVerticalRight)

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

        """ Перерасчет столбца сумм и накопления в исходном numpy array"""

        self.backend.recalculate()

    def load_data(self, filepath=default_db_filepath, dataset_name='default'):
        """ Загрузка данных из файла в nympy массив"""
        # загружаем данные из hdf5  файла в numpy массив self.backend_data
        Load()(self.backend_data, filepath, dataset_name=dataset_name)
        # получаем размерности таблицы
        dimension = (self.backend_data.shape[0], self.backend_data.shape[1])
        # заполнение таблицы
        self.init_data_model_and_table(dimension)
        # операция полного сброса модели для привентривной перересовки
        # http://doc.qt.io/qt-5/qabstractitemmodel.html#endResetModel
        self.model.endResetModel()
        # self.model.dataChanged()

    def overflow(self):
        """ вызов сообщения о некорректном введенном значении """
        QtWidgets.QMessageBox.information(self, 'Переполнение', "Слишком большое значение. Необходимо исправить")

    def save_to_file(self):
        """ Загрузка данных в произвольный файл по выбору"""
        # получаем путь к файлу
        save_path = File_Dialog.get_save_filepath(self)
        # если путь получен
        if save_path:
            # добавляем путь и метаданные в конфиг
            self.config.add(config_file, {save_path: (self.row_n, self.col_n)})
            # сохраняем данные из numpy массива в файл
            Save()(self.backend_data, filepath=save_path)
            # добавляем запись о данном файле в виджет списка
            self.cmbFilesList.addItem(save_path + f' ({self.row_n}, {self.col_n})')

    def load_from_file(self):
        """ Слот загрузки данных из произвольного файла в nympy массив"""

        # получаем путь на файл, откуда будут загружаются данные
        load_path = File_Dialog.get_load_filepath(self)

        if load_path:
            # вызываем функцию загрузки и сброса данных в модель
            self.load_data(load_path)

    def load_from_list(self):
        """ Слот загрузки данных из файла путь которого указан в виджете списка"""
        # вычисляем номер элемента в списке он совпадает с номером элемента в конфиге
        index = self.cmbFilesList.currentIndex()
        # получаем путь на файл, откуда будут загружаются данные
        load_path = self.config.get_path(index)
        if load_path:
            # вызываем функцию загрузки и сброса данных в модели
            self.load_data(load_path)

    def init_data_model_and_table(self, table_dimension: tuple):
        choices = ['0', '1', '2', '3', '4', '5']
        # номер столбца с QComboBox
        cbox_column = 1

        self.row_n = raw_data.shape[0]  # число строк в numpy массиве исходных данных
        self.col_n = raw_data.shape[1]  # число столбцов в numpy массиве исходных данных
        # Варианты выбора для ячеек с Combobox
        # Получение данные через класс Backend
        self.backend = Backend(raw_data, self.row_n - 1, self.col_n - 3)
        self.backend_data = self.backend.get_data()
        self.backend.recalculate()
        # Создание модели
        self.model = Model(self.backend_data)
        # изменение данных в модели вызывет перерасчет через метод recalc
        self.model.c.data_changed.connect(self.recalc)
        self.model.overflow.overflow.connect(self.overflow)

        # создание виджетов таблицы
        # изменение значеняи ячейки одинарным щелчком
        self.table_data.setEditTriggers(QtWidgets.QAbstractItemView.CurrentChanged)
        # подключиние модели к таблице
        self.table_data.setModel(self.model)
        self.table_data.resizeColumnsToContents()
        # Установка делегата на второй столбец таблицы
        self.table_data.setItemDelegateForColumn(cbox_column, Delegate(self, choices))
        # получаем модель выделения
        self.selectionModel = self.table_data.selectionModel()
        # событие происходящее выделением столбца целчком по шапке таблицы
        self.table_data.horizontalHeader().sectionClicked.connect(self.draw_graph)

        # сделать Combobox редактируемым одним щелчком во 2(1) столбце
        for row in range(self.backend_data.shape[0]):
            self.table_data.openPersistentEditor(self.model.index(row, cbox_column))

    def fill_QTreeView(self):
        # self.tv = QtWidgets.QTreeView()
        # sti = QStandardItemModel(parent=self)
        # rootitem1 = QStandardItem('Маленькие файлы')
        # rootitem1.appendColumn([QStandardItem(f"f{j}") for j in range(10)])
        # # for i in range(10):
        # #     rootitem1.child(i).setEditable(True)
        #
        # sti.appendRow(rootitem1)
        # rootitem2 = QStandardItem("Большие файлы")
        #
        # rootitem2.appendColumn([QStandardItem(f"BIGFILE{j}") for j in range(10)])
        # sti.appendRow(rootitem2)
        # sti.setHorizontalHeaderLabels(['Проекты',])
        # self.tv.setModel(sti)
        # создаем QTreeView
        self.tv = ProjectTree(r"HDF_FILES\geosim.meta")
        # вешаем событие нажатия на элемент дерева
        self.tv.clicked.connect(self.save_current_dataset_item)

        return self.tv

    def save_current_dataset_item(self, index: QModelIndex):
        # получаем имя hdf5 файла выбранного элемента в дереве tv
        Metadata.cur_filename = index.parent().data()
        # получаем имя выбранного датасета
        Metadata.cur_dataset = index.data()
        # если выбран датасет а не что-то другое
        if Metadata.cur_filename and Metadata.cur_dataset:
            # выводим имена файла и датасета в метку lbl_log
            self.lbl_log.setText(str(f'{Metadata.cur_dataset} {Metadata.cur_filename}'))
            #  заполняем таблицу метаданных
            self.fill_metadata_table(Metadata.cur_filename, Metadata.cur_dataset)

    def fill_metadata_table(self, filename, dataset):
        """ заполняем таблицу QTableWidjet метаданными выбранного датасета"""
        # очистка таблицы QTableWidjet
        self.tw_metadata.setRowCount(0)
        # вытаскиваем метаданные выбранного датасета
        current_metadata = Metadata.current_dataset_metadata[filename][dataset]
        # заполняем таблицу
        for index, key in enumerate(current_metadata):
            print("METADATA", Metadata.current_dataset_metadata)
            print(index, key)
            print('row count:', self.tw_metadata.rowCount())
            # вставляем строку в таблицу QTableWidjet
            self.tw_metadata.insertRow(index)
            # заносим название параметра в таблицу QTableWidjet
            self.tw_metadata.setItem(index, 0, QTableWidgetItem(str(key)))
            # преобразуем unix time в человеко понятный формат в параметре 'dset create at'
            if str(key) != "dset create at":
                value = str(current_metadata[key])
            else:
                value = str(datetime.utcfromtimestamp(current_metadata[key]).strftime('%Y-%m-%d %H:%M:%S'))
            # заносим значение параметра в таблицу QTableWidjet
            self.tw_metadata.setItem(index, 1, QTableWidgetItem(value))

    def load_dset(self):
        """функция заполнения таблицы данными из выбранного датасета"""
        # если датасет выбран  в деревер
        if Metadata.cur_filename:
            # собираем путь до файла с датасетом
            dataset_file_path = os.path.join(Metadata.current_project_dir, Metadata.cur_filename)
            # загружаем данные в numpy массив и в таблицу
            self.load_data(dataset_file_path, Metadata.cur_dataset)

    def generate_datafiles(self):
        """ функция генерации проекта(множестов мелких файлов с одним датасетом в каждом
        и один большой с нескольким датасетами )"""
        # размерность генерируемых таблиц
        dim = (150, 150)
        # число генерируемы датасетов в одном файле и файлов с одним датасетом
        numbers = 10
        # класс генератора путь к метафайлу (по умолчанию)  "HDF_FILES\geosim.meta"
        gen = Generator_HDF5_Hierarchy(dim, numbers, None)
        # создается много hdf5 файлов c одним датасетом
        gen.generate_many()
        # создается один файл с несколькими датасетами
        gen.generate_one_big()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    app.exec_()
