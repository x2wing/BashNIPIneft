import yaml
import os.path
from collections import OrderedDict


class YAML_config():
    """Класс для работы с конфигом"""

    def __init__(self, config_path, default_config_data):
        """ заполнение хранилища данными"""

        # хранилище десериализованных данных конфига
        self.config_data = OrderedDict({})
        # если файл не пустой данные берутся из конфига
        try:
            self._get_config_data(config_path)
        # если пустой данные берутся из дефолтного файла и его метаданных
        except:
            self.add(config_path, default_config_data)

    def _is_file_exist(self, file_path):
        """ проверка файла на существование"""

        return os.path.isfile(file_path)

    def _rw_yaml_config(self, file_path, data=None, mode='r'):
        """ вспомогательный метод чтения записи yaml файла"""

        with open(file_path, mode, encoding='utf-8') as stream:
            # если режим чтение, возвращаем десериализованные данные из yaml-файла
            if mode == 'r':
                return yaml.load(stream)
            # если режим запись, сериализуем данные в файл
            elif mode == 'w':
                yaml.dump(data, stream, default_flow_style=False, allow_unicode=True)

    def _get_config_data(self, config_path):
        """ первоначальное заполнение хранилища """
        self.config_data.update(self._rw_yaml_config(config_path, data=None, mode='r'))
        # если конфиг пустой выбрасываем исключение
        assert self.config_data, 'Файл конфигурации пуст'

    def add(self, file_path, data_item):
        """ добавление данных(dict) в конфиг """
        self.config_data.update(data_item)
        self._rw_yaml_config(file_path, self.config_data, mode='w')

    def get_str_paths_list(self):
        """ возвращает список строк путей и метаданных """
        return [f'{key} {value}' for key, value in self.config_data.items()]

    def get_paths_list(self):
        """ возвращает список всех путей"""
        return list(self.config_data.keys())

    def get_path(self, index):
        """ возвращает путь по индексу(номеру записи в виджете списка начиная с 0) """
        return self.get_paths_list()[index]


if __name__ == '__main__':
    conf = YAML_config
    fpath = r'config.yaml'
    config_data = OrderedDict({r'db2.hdf5': (8, 8)})
    conf.add(conf, file_path=fpath, data_item=config_data)

    # data = np.random.randint(-100, 100, (8, 12))
    # # conf.save(fpath, config_data)
    # conf.load(fpath)
    # print(conf.save(fpath, config_data))
    # if is_file_exist(fpath):
    #     result = rw_yaml_config(fpath)
    #     print(result.keys())
    # else:
    #     rw_yaml_config(fpath, config_data, 'w')
    #
    # print(Load()(data, filepath=list(result.keys())[0]))
