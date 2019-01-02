from pprint import pprint

import h5py
import numpy as np
import os
import time

import project_metadata
from profiler import profile

# from hdf5client import hdf5_Client


def timer(foo):
    """ декоратор. выводит время выполнения методов"""

    def wrapper(self, *args, **kargs):
        tm = time.time()
        result = foo(self, *args, **kargs)
        print(f"ВРЕМЯ ВЫПОЛНЕНИЯ {foo.__name__}", time.time() - tm)
        return result

    return wrapper


class Generator_HDF5_Hierarchy():

    def __init__(self, dimensions: tuple, num: int, path: str,
                 dir_name="HDF_FILES", file_name_template="DSET", dataset_template="DSET"):

        """
        класс генерации файлов проекта (hdf5 файлов)

        dimensions - кортеж размерности генерируемого numpy массива
        num - число генерируемых файлов
        path - путь где будет сохранена папка проекта(папка со сгенерируемыми файлами)
        dir_name - имя папки проекта
        file_name_template - имя генерируемого файла (к нему будет добавлено расширение .h5geo)
        dataset_template - имя датасета по-умолчанию
        """

        self.dimensions = dimensions
        self.num = num
        self.dir_name = dir_name
        self.file_name_template = file_name_template
        self.dataset_template = dataset_template

        self.current_dir_path = os.getcwd()
        self.dir_path = os.path.join(self.current_dir_path,
                                     self.dir_name)
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            pass
        metadata = {}
        self.metadata_save = project_metadata.Metadata(self.dir_path + '\geosim.meta')

    def get_numpy_data(self, dimensions: tuple):
        return np.random.random(dimensions)

    # @timer
    def set_metadata(self, dset_name, n_data: np.ndarray, file_path):
        metadata_path = os.path.dirname(file_path) + '\geosim.meta'
        print(metadata_path)
        metadata = {
            os.path.basename(file_path):
                {
                    'file create at': time.time(),
                 dset_name: {
                     'dset create at': time.time(),
                     'shape': n_data.shape,
                     'min': n_data.min(),
                     'max': n_data.max(),
                 }
                 }
        }
        # pprint(metadata)

        self.metadata_save.save_metadata(metadata)

    def create_dataset_wrapper(self, f, dset_name, file_path, n_data):
        try:
            f.create_dataset(dset_name, data=n_data)
        except Exception  as err:
            print(err)
        else:
            # return
            self.set_metadata(dset_name, n_data, file_path)

    # @timer
    @profile
    def generate_many(self):
        for i in range(self.num):
            file_name = f"{self.file_name_template}{i}"
            # dataset_name = f"{self.dataset_template}{i}"

            file_path = os.path.join(self.dir_path,
                                     file_name + '.h5geo')
            print(file_path)
            data = self.get_numpy_data(self.dimensions)
            with h5py.File(file_path, mode='w') as f:
                self.create_dataset_wrapper(f, self.dataset_template, file_path, n_data=data)

    # @timer
    @profile
    def generate_one_big(self):

        file_path = os.path.join(self.dir_path,
                                 self.file_name_template + 'BIG.h5geo')
        print(file_path)
        with h5py.File(file_path, mode='w') as f:
            for i in range(self.num):
                data = self.get_numpy_data(self.dimensions)
                dataset_name = f"{self.dataset_template}{i}"
                self.create_dataset_wrapper(f, dataset_name, file_path, n_data=data)

    # пока не реализовано
    # @timer
    # def generate_to_server(self):
    #     domain = 'priobka_geo1.public.h5.svr'
    #     client = hdf5_Client(domain, "http://h5.svr:5000", mode='r+')


if __name__ == '__main__':
    dim = (150, 150)
    numbers = 10
    gen = Generator_HDF5_Hierarchy(dim, numbers, None)
    gen.generate_many()
    gen.generate_one_big()
    # gen.generate_to_server
