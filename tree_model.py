from collections import OrderedDict
from PyQt5 import QtCore, QtGui, QtWidgets

import project_metadata

class MyModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super(MyModel, self).__init__(parent)
        self.metadata = project_metadata.Metadata(r"HDF_FILES\geosim.meta")
        self.get_contents()


    def get_contents(self):
        self.clear()

        D = OrderedDict([('DSET0.h5geo', {
            'DSET': {'dset create in': 1546060327.3476002, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.3476002}), ('DSET1.h5geo', {
            'DSET': {'dset create in': 1546060327.364146, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.364146}), ('DSET2.h5geo', {
            'DSET': {'dset create in': 1546060327.3811069, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.3811069}), ('DSET3.h5geo', {
            'DSET': {'dset create in': 1546060327.400054, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.400054}), ('DSET4.h5geo', {
            'DSET': {'dset create in': 1546060327.420993, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.420993}), ('DSET5.h5geo', {
            'DSET': {'dset create in': 1546060327.4419138, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.4419138}), ('DSET6.h5geo', {
            'DSET': {'dset create in': 1546060327.465877, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.465877}), ('DSET7.h5geo', {
            'DSET': {'dset create in': 1546060327.4959016, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.4959016}), ('DSET8.h5geo', {
            'DSET': {'dset create in': 1546060327.522838, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.522838}), ('DSET9.h5geo', {
            'DSET': {'dset create in': 1546060327.5517552, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.5517552}), ('DSETBIG.h5geo', {
            'DSET0': {'dset create in': 1546060327.5796828, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'DSET1': {'dset create in': 1546060327.6096065, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'DSET2': {'dset create in': 1546060327.6395245, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'DSET3': {'dset create in': 1546060327.669414, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'DSET4': {'dset create in': 1546060327.7003314, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'DSET5': {'dset create in': 1546060327.7342405, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'DSET6': {'dset create in': 1546060327.7701468, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'DSET7': {'dset create in': 1546060327.807046, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'DSET8': {'dset create in': 1546060327.8469596, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'DSET9': {'dset create in': 1546060327.887829, 'max': 'y', 'min': 'x', 'shape': (100, 100, 100)},
            'file create in': 1546060327.5796828})])
        D = self.metadata.get_metadata()
        print(D)
        root = self.invisibleRootItem()
        for i1, k1 in enumerate(D.keys()):
            if k1 != "version":
                c = root.setChild(i1, QtGui.QStandardItem(k1))
                print(f'child object {c})')
                u2 = root.child(i1)
                for i2, k2 in enumerate(D[k1].keys()):
                    print("i2 k2",i2, k2)
                    if k2.find("DSET")!= -1:
                        u2.setChild(i2, QtGui.QStandardItem(k2))


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QTreeView()
    model = MyModel(w)
    w.setModel(model)
    w.show()
    w.expandAll()
    sys.exit(app.exec_())