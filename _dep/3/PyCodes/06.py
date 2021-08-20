import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QLineEdit, QFileDialog, QPushButton, QMessageBox, QMainWindow, QTableView
from PyQt5.QtGui import QIcon
import numpy as np
from collections import OrderedDict

def get_data():
    nrows = 50
    ncols = 5
    return np.arange(nrows * ncols).reshape((nrows, ncols)).astype(str)

class TableModel(QtCore.QAbstractTableModel):

    """
    An instance of this class is created inside the constructor
    of the class 'TableWindow'.
    """

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class TableWindow(QMainWindow):

    """
    This class is used to view the raw data file via gui.
    """

    def __init__(self, data):
        super().__init__()
        self.table = QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
        self.setWindowTitle("Select 'row' if each student corresponds to a row; otherwise, select 'column'")

if __name__ == '__main__':

    data = get_data()

    ## initialize application
    app = QtWidgets.QApplication(sys.argv)

    ## view data file
    window = TableWindow(data.tolist())
    window.show()

    ## exit application
    sys.exit(app.exec_())
