import os, sys
from PyQt5.QtWidgets import (QWidget, QFileDialog, QApplication)


class File_Dialog(QWidget):
    @staticmethod
    def get_save_filepath(self):
        description = 'Сохранить hdf5'
        default_path = os.path.dirname(os.path.abspath(__file__))
        filter = "Таблицы hdf5  (*.hdf5)"
        path, _ = QFileDialog.getSaveFileName(self, description, default_path, filter)
        print(path)
        return path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    File_Dialog.get_save_filepath(window)
    window.show()
    sys.exit(app.exec_())

