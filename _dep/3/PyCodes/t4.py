import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np


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

class TableWindow(QtWidgets.QMainWindow):

    """
    This class is used to view the a data table via gui.
    """

    def __init__(self, data):
        super().__init__()
        self.table = QtWidgets.QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
        self.setWindowTitle("Data Table")

class MainWindow(QtWidgets.QMainWindow):


    """
    This class contains all GUI methods.
    """

    def __init__(self):
        self.table_window = None
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        nrows = 50
        ncols = 10
        data = np.arange(nrows * ncols).reshape((nrows, ncols)).astype(str)
        self.table_window = TableWindow(data.tolist())
        self.table_window.show()






if __name__ == '__main__':

    # nrows = 50
    # ncols = 10
    # data = np.arange(nrows * ncols).reshape((nrows, ncols)).astype(str)

    ## initialize application
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()

    # window = TableWindow(data.tolist())
    # window.show()

    ## exit application
    sys.exit(app.exec_())
