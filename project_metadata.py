import yaml
import os.path
from collections import OrderedDict, defaultdict


class Metadata():

    current_dataset_metadata = {}

    def __init__(self, metafile_path: str):
        data = {"version": 0.1}
        if not self._get_metadata(metafile_path):
            self._rw_yaml_config(metafile_path, data=data, mode='w')
        self.metafile_path = metafile_path

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
        try:
            return self._rw_yaml_config(metafile_path, mode='r')
        except:
            return None

    def get_metadata(self):
        return self._get_metadata(self.metafile_path)

    def save_metadata(self, new_metadata: dict):
        metadata_from_file = self._get_metadata(self.metafile_path)
        if metadata_from_file:
            metadata = OrderedDict({})
            metadata.update(metadata_from_file)
            # вытаскиваем ключ из добавляемого словаря
            new_key = next(iter(new_metadata.keys()))
            if new_key in metadata:
                print(new_metadata)
                print(metadata)
                print(metadata['DSET0.h5geo'])
                for key, value in new_metadata[new_key].items():
                    metadata[new_key].setdefault(key, value)
            else:
                metadata.update(new_metadata)
            self._rw_yaml_config(self.metafile_path, metadata, mode='w')
        else:
            assert False, "файл не прочитан, пуст или не существует"


if __name__ == '__main__':
    Meta = Metadata(r"D:\projects\BashNIPIneft-dev\HDF_FILES\geosim.meta")
    print(
        Meta.get_metadata()
    )
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
