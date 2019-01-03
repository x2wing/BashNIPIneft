import yaml
import os.path
from collections import OrderedDict, defaultdict
import numpy as np
import time


class Metadata():
    """ Класс работы с метаданными проекта"""

    cur_filename = ""  # имя текущего hdf5-файла(без пути)
    cur_dataset = ""  # имя текущего датасета

    # current_datafile_path = "" #

    current_project_dir = ""  # путь к папке текущего проекта
    # метаданные текущего выбранного(в QTreeView) датасета
    current_dataset_metadata = defaultdict(dict)

    def __init__(self, metafile_path: str):
        data = {"version": 0.1}
        # если файл метаданных проекта пустой
        if not self._get_metadata(metafile_path):
            # запишем в него версию
            self._rw_yaml_config(metafile_path, data=data, mode='w')
        self.metafile_path = metafile_path
        # сохраним путь к папке текущего проекта
        Metadata.current_project_dir = os.path.dirname(self.metafile_path)

    def _rw_yaml_config(self, file_path: str, data=None, mode='r'):
        """ вспомогательный метод чтения записи yaml файла"""

        with open(file_path, mode, encoding='utf-8') as stream:
            # если режим чтение, возвращаем десериализованные данные из yaml-файла
            if mode == 'r':
                return yaml.load(stream)
            # если режим запись, сериализуем данные в файл
            elif mode == 'w':
                yaml.dump(data, stream, default_flow_style=False, allow_unicode=True)

    def _get_metadata(self, metafile_path):
        """ если данные корректные метод возвращает словарь метаданных
        в противном случае возвращает None"""
        try:
            return self._rw_yaml_config(metafile_path, mode='r')
        except:
            return None

    def get_metadata(self):
        """ public метод получения метаданных"""
        return self._get_metadata(self.metafile_path)

    def save_metadata(self, new_metadata: dict):
        """Добавление\обновление метаданных в файл метаданных"""
        # получаем все метаданные из файла
        metadata_from_file = self._get_metadata(self.metafile_path)
        # если метаданные получены
        if metadata_from_file:
            # создаем пустой словарь
            metadata = OrderedDict({})
            # и копируем туда данные
            metadata.update(metadata_from_file)
            # вытаскиваем ключ(один) из добавляемого словаря
            new_key = next(iter(new_metadata.keys()))
            # если такой ключ существует в существующем словаре
            if new_key in metadata:
                # перебираем данные(ключ и значение) второго уровня
                for key, value in new_metadata[new_key].items():
                    # metadata[new_key].setdefault(key, value)
                    # добавляем новые данные под старый ключ
                    metadata[new_key].update(new_metadata[new_key])
            else:
                # если такого ключа не существует просто добавляем весь словарь
                metadata.update(new_metadata)
            # записывем измененный словарь в метафайл проекта
            self._rw_yaml_config(self.metafile_path, metadata, mode='w')
        else:
            # если метаданные не получны выбросим исключение
            assert False, f"файл {self.metafile_path} не прочитан, пуст или не существует"

    def set_metadata(self, n_data: np.ndarray):
        """Метод создания текущего элемента метаданных """
        # словарь с метаданными
        metadata = OrderedDict({
            # текущее имя файла
            Metadata.cur_filename:
                {
                    # время создания файла
                    'file create at': time.time(),
                    # имя текущего датасета
                    Metadata.cur_dataset: {

                        'dset create at': time.time(), #время создания датасета
                        'shape': n_data.shape, # размерность датасета
                        'min': n_data.min(), # минимальное значение датасета
                        'max': n_data.max(), # максимальное значение датасета
                    }
                }
        })
        # сохраняем метаданные
        self.save_metadata(metadata)
        # обновляем метаданные текущего элемента QTreeView
        Metadata.current_dataset_metadata = metadata

    # статический метод получения метаданных текущего датасета
    @staticmethod
    def get_current_dataset_metadata(filename, dataset):
        return Metadata.current_dataset_metadata[filename][dataset]


if __name__ == '__main__':
    Meta = Metadata(r"D:\projects\BashNIPIneft-dev\HDF_FILES\geosim.meta")
    # print(
    #     Meta.get_metadata()
    # )
    # Meta.save_metadata({
    #     'DSET0.h5geo':
    #         {
    #             'file create in': 1232,
    #             "RRR45": {
    #                 'dset create in': 123123,
    #                 'shape': 123,
    #                 'min': 'x',
    #                 'max': 'y',
    #             }
    #         }
    # })
    # print(Meta.get_metadata()['DSET0.h5geo'])
