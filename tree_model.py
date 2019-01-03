from collections import OrderedDict
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex

import project_metadata


class MyModel(QtGui.QStandardItemModel):
    def __init__(self, metadata, parent=None):
        super(MyModel, self).__init__(parent)
        self.metadata = metadata

        self.get_contents()

    def get_contents(self):
        self.clear()
        D = self.metadata
        print(D.pop("version", None))
        print(D)
        root = self.invisibleRootItem()
        for i1, k1 in enumerate(D.keys()):
            if k1 != "version":
                root.setChild(i1, QtGui.QStandardItem(k1))
                u2 = root.child(i1)
                for i2, k2 in enumerate(D[k1].keys()):
                    if k2.find("DSET") != -1:
                        u2.setChild(i2, QtGui.QStandardItem(k2))


class ProjectTree(QtWidgets.QTreeView):
    def __init__(self, meta_path="", parent=None):
        super().__init__(parent)
        if meta_path:
            self.meta_path = meta_path
            self.fill_treeview(self.meta_path)
        self.clicked.connect(self._show_dataset)

    def create_model(self):
        self.metadata_instance = project_metadata.Metadata(self.meta_path)
        self.metadata = self.metadata_instance.get_metadata()
        return MyModel(self.metadata)

    def set_model(self):
        self.setModel(self.model)

    def fill_treeview(self, cur_meta_path):
        self.meta_path = cur_meta_path
        self.model = self.create_model()
        self.set_model()
        self.expandAll()

    def _show_dataset(self, index: QModelIndex):
        file = index.parent().data()
        dataset = index.data()
        if file and dataset:
            project_metadata.Metadata.current_dataset_metadata[file][dataset] = self.metadata[file][dataset]


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    meta_path = r"HDF_FILES\geosim.meta"
    w = ProjectTree()
    w.fill_treeview(meta_path)
    w.show()

    sys.exit(app.exec_())
