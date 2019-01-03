from collections import  defaultdict
from PyQt5 import  QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex

from  project_metadata import Metadata


class ProjectModel(QtGui.QStandardItemModel):
    """Класс создания модели для отображения в QTreeView"""
    def __init__(self, metadata, parent=None):
        # вызываем родительский конструктор
        super(ProjectModel, self).__init__(parent)
        self.metadata = metadata
        #метод заполнения модели
        self.get_contents()

    def get_contents(self):
        # очищаем модель. Необходимо для открытия другого проекта
        self.clear()
        # D - более короткая запись self.metadata
        D = self.metadata
        # выбрасываем "version" из метаданных
        D.pop("version", None)
        # получаем корневой элемент дерева
        root = self.invisibleRootItem()
        # перебираем ключи верхнего уровня в метадате
        for i1, k1 in enumerate(D.keys()):
            # Если ключе не "version"
            if k1 != "version":
                # установим его элементом первого уровня
                root.setChild(i1, QtGui.QStandardItem(k1))
                # создаем элементы второго уровня
                u2 = root.child(i1)
                # перебираем ключи второго уровня
                for i2, k2 in enumerate(D[k1].keys()):
                    # если это DSET(содержит DSET в названии)
                    if k2.find("DSET") != -1:
                        # добавляем этот ключ в элемент второго уровня
                        u2.setChild(i2, QtGui.QStandardItem(k2))


class ProjectTree(QtWidgets.QTreeView):
    """ Класс заполнени и обработки QTreeView"""
    def __init__(self, metadata_path="", parent=None):
        super().__init__(parent)
        # если при вызове указан путь к метафайлу проекта
        if metadata_path:
            self.meta_path = metadata_path
            # вызываем функцию заполнения дерева на виджете
            self.fill_treeview(self.meta_path)
        # вешаем событие щелчка по элементу QTreeView
        self.clicked.connect(self.set_current_dataset)

    def _create_model(self):
        """Метод создания модели"""
        # создаем экземпляр класса Metadata где хранятся
        # все данные о метаданных текущего открытого проекта
        self.metadata_instance = Metadata(self.meta_path)
        #получаем весь словарь с метаданными вычитанными из h5geo
        self.metadata = self.metadata_instance.get_metadata()
        # возвращаем экземпляр созданной модели на основе словаря метаданных
        return ProjectModel(self.metadata)

    def _set_model(self):
        """Метод установки модели"""
        self.setModel(self.model)

    def fill_treeview(self, cur_meta_path):
        """Метод заполнения дерева на виджете
        cur_meta_path - путь к метафайлу проекта
        заменяется т.к. метод вызывается снаружи класса
        """

        # заменяем путь к метафайлу проекта
        self.meta_path = cur_meta_path
        # создание модели
        self.model = self._create_model()
        # применяем модель
        self._set_model()
        # развернуть все дерево в QTreeView
        self.expandAll()

    def set_current_dataset(self, index: QModelIndex):
        """Метод вызывается при нажатии на элемент QTreeView"""
        # получаем имя файла
        file = index.parent().data()
        # и имя датасета
        dataset = index.data()
        # если получены оба(нажато по элементу второго уровня т.е. датастету)
        if file and dataset:
            # очищаем метаданные о "устаревшем" датасете
            Metadata.current_dataset_metadata=defaultdict(dict)
            # и добавляем метаданные о текущем датасете
            Metadata.current_dataset_metadata[file][dataset] = self.metadata[file][dataset]

    def update_metadata(self, cur_meta_path):
        """метод обновления метаданных"""
        self.fill_treeview(cur_meta_path)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    meta_path = r"HDF_FILES\geosim.meta"
    w = ProjectTree()
    w.fill_treeview(meta_path)
    w.show()

    sys.exit(app.exec_())
