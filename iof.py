import h5py
from pprint import pprint


class Save:
    """ сохранить данные в файл hdf5"""

    def __call__(self, data, filepath, dataset_name='default'):
        """ функция __call__ для передачи в обработчик события PyQt,
            чтобы не загромождать код в main.py

            data - numpy array которы будет записан в файл
            filepath - путь к файлу
            dataset_name - имя датасет в hdf5
        """

        with h5py.File(filepath, 'w') as f:
            f.create_dataset(dataset_name, data=data)


class Load:
    """ загрузит данные из hdf5"""

    def __call__(self, data, filepath, dataset_name='default'):
        """ функция __call__ для передачи в обработчик события PyQt,
         чтобы не загромождать код в main.py

         data - ссылка на numpy array которая будет перезаписана данными из файла
         filepath - путь к файлу
         dataset_name - имя датасет в hdf5

         """

        with h5py.File(filepath, 'r') as f:
            data[:] = f[dataset_name][:]
            return data


if __name__ == '__main__':
    import numpy as np

    arr = Load()()
    np.set_printoptions(suppress=True, precision=3)
    # arr = np.random.randint(1, 100, 1000)
    # Save()(arr)
    print(arr)

    #
    #
    # arr = np.random.randn(1000)
    # arr = np.array([[0, 0, 0, 0, 0],
    #                 [1, 1, 1, 1, 1]])
    # file = 'random.hdf5'
    # dataset_name = "default"
    #
    #
    # def write_hdf5(file_name, data, dataset_name, operation='w'):
    #     with h5py.File(file_name, operation) as f:
    #         return f.create_dataset(dataset_name, data=data, dtype=float)
    #
    #
    # write_hdf5(file, arr, dataset_name)
