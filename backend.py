import numpy as np


class Backend():
    """ класс для работы с иходными данными"""
    def __init__(self, source, data_row, data_col):
        # исходный массив
        self.source = source
        # число исходных строк и столбцов по которым считается сумма,
        # накопленная сумма и т.д.(без учета столбцов вычисляемых данных)
        self.data_row = data_row
        self.data_col = data_col
        # относительный номер столбца от исходных данных
        self.sum_column_ofset_out = 1
        # относительный номер столбца от исходных данных
        self.cumsum_column_ofset_out = 2
        # абсолютный номер столбца по которому считается накопленная сумма
        self.cumsum_column_in = 0


    def get_data(self):
        """ возвращает ссылку на исходные данные"""
        return self.source

    def recalculate(self):
        # пересчет суммы и накопленной суммы
        self.source[:, self.data_col + self.sum_column_ofset_out] = self.source[:, :self.data_col + 1].sum(axis=1)
        self.source[:, self.data_col + self.cumsum_column_ofset_out] = self.source[:, self.cumsum_column_in].cumsum(
            axis=0)



if __name__ == '__main__':
    raw_data = np.array([[-1, 2, 3, -4, 0, 0, 0],
                         [6, 1, 8, 9, -10, 0, 0],
                         [11, 3, 13, 14, -15, 0, 0],
                         [0, 4, 18, -19, 20, 0, 0],
                         [-1, 2, 3, -4, 0, 0, 0],
                         [6, 1, 8, 9, -10, 0, 0],
                         [11, 3, 13, 14, -15, 0, 0],
                         [0, 4, 18, -19, 20, 0, 0]
                         ])
    dataconnector = Backend(raw_data, 8, 4)
    print_data = dataconnector.get_data()
    dataconnector.recalculate()

    print_data[0][:] = 50
    print('третий столбец', print_data[2])
    print_data[:][3] = 1250
    dataconnector.recalculate()
    print(raw_data)
