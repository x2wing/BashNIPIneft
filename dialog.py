import os, sys
from PyQt5.QtWidgets import (QWidget, QFileDialog, QApplication)


class File_Dialog(QWidget):
    """Класс вывода диалогов "Сохранить",  "Загрузить" и получения путей из них"""
    @staticmethod
    def get_save_filepath(self):
        description = 'Сохранить hdf5' # заголовок окна диалога
        default_path = os.path.dirname(os.path.abspath(__file__)) # дефолтный путь диалогового окна
        filter = "Таблицы hdf5  (*.hdf5)" # фильтр расширения
        # получаем путь к файлу
        path, _ = QFileDialog.getSaveFileName(self, description, default_path, filter)
        return path

    def get_load_filepath(self):
        description = 'Загрузить hdf5' # заголовок окна диалога
        default_path = os.path.dirname(os.path.abspath(__file__)) # дефолтный путь диалогового окна
        filter = "Таблицы hdf5  (*.hdf5)" # фильтр расширения
        # получаем путь к файлу
        path, _ = QFileDialog.getOpenFileName(self, description, default_path, filter)
        return path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    File_Dialog.get_save_filepath(window)
    window.show()
    sys.exit(app.exec_())

