import yaml
from iof import Save, Load
import numpy as np
from collections import OrderedDict


class YAML_config():
    config_data = OrderedDict()

    def __init__(self, config_path):
        self._get_config_data(config_path)

    def _is_file_exist(self, file_path):
        import os.path
        return os.path.isfile(file_path)

    def _rw_yaml_config(self, file_path, data=None, mode='r'):
        with open(file_path, mode, encoding='utf-8') as stream:
            if mode == 'r':
                return yaml.load(stream)
            elif mode == 'w':
                yaml.dump(data, stream, default_flow_style=False, allow_unicode=True)

    def _get_config_data(self, config_path):
        YAML_config.config_data = self._rw_yaml_config(config_path, data=None, mode='r')

    def save(self, file_path, data_item):
        YAML_config.config_data.update(data_item)
        self._rw_yaml_config(file_path, YAML_config.config_data, mode='w')

    def load(self, file_path):
        if self._is_file_exist(file_path):
            self._get_config_data(file_path)
            return YAML_config.config_data
        else:
            print(__name__, __class__)
            raise OSError


if __name__ == '__main__':
    conf = YAML_config()

    data = np.random.randint(-100, 100, (8, 12))
    config_data = OrderedDict({r'db2.hdf5': (8, 9)})
    fpath = r'config.yaml'
    # conf.save(fpath, config_data)
    conf.load(fpath)
    print(conf.save(fpath, config_data))
    # if is_file_exist(fpath):
    #     result = rw_yaml_config(fpath)
    #     print(result.keys())
    # else:
    #     rw_yaml_config(fpath, config_data, 'w')
    #
    # print(Load()(data, filepath=list(result.keys())[0]))
