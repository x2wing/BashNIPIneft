from PyQt5 import QtWidgets, QtCore


class Delegate(QtWidgets.QItemDelegate):
    """ Делегат который вешает QComboBox на второй столбец"""

    def __init__(self, owner, choices):
        super().__init__(owner)
        self.items = choices

    def createEditor(self, parent, option, index):
        # создаем редактор в виде QComboBox на второй столбец
        self.editor = QtWidgets.QComboBox(parent)
        # заполняем значениями вариантов выбора в QComboBox
        self.editor.addItems(self.items)
        return self.editor

    # def eventFilter(self, editor, event):
    #     """ ловим события"""
    #     print(event.type())
    #     return QtWidgets.QItemDelegate.eventFilter(self, editor, event)

    def setEditorData(self, editor: QtWidgets.QComboBox, index):
        """заполняем QComboBox значениями если значения невалидные ставим 0"""
        value = index.data(QtCore.Qt.DisplayRole)
        try:
            editor.setCurrentIndex(int(value))
        except ValueError:
            editor.setCurrentIndex(0)

    def setModelData(self, editor, model, index):
        """ Передаем измененные данные в модель """
        model.setData(index, editor.currentIndex(), QtCore.Qt.EditRole)

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        print("setData", index.row(), index.column(), value)

    def updateEditorGeometry(self, editor, option, index):
        """ установка размеров делегата"""
        editor.setGeometry(option.rect)
