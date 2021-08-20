import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np

class BackEnd():

    def __init__(self):
        super().__init__()
        # ...
        nrows, ncols = 50, 10
        self.data = np.arange(nrows * ncols).reshape((nrows, ncols)).astype(str)

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
    This class is used to view the raw data file via gui.
    """

    def __init__(self, data):
        super().__init__()
        self.table = QtWidgets.QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
        self.setWindowTitle("Select 'row' if each student corresponds to a row; otherwise, select 'column'")

# back_end = BackEnd()
#
# ## initialize application
# app = QtWidgets.QApplication(sys.argv)
#
# ## view data file
# window = TableWindow(back_end.data.tolist())
# window.show()
#
# ## exit application
# sys.exit(app.exec_())


class MainWindow(QtWidgets.QMainWindow):


    """
    This class contains all GUI methods.
    """

    def __init__(self):
        self._backend = BackEnd()
        self._fpath = None
        super().__init__()
        self.initialize_ui()

    @property
    def backend(self):
        return self._backend

    @property
    def fpath(self):
        return self._fpath

    def initialize_ui(self):
        self.select_input_data_file()
        self.verify_input_data_file()
        # self.close()
        self.interact_with_table()

    def select_input_data_file(self):
        dialog = QtWidgets.QFileDialog(
            self,
            "Select input file",
            "path",
            "",
            supportedSchemes=["file"],
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        fpath = dialog.getOpenFileName(None, 'Open file', '/home')[0]
        self._fpath = fpath
        # dialog.close()
        # dialog = None

    def verify_input_data_file(self):
        alert = QtWidgets.QMessageBox()
        alert.setText('The input filepath you selected is: \n{}'.format(self.fpath))
        alert.exec_()
        # alert.close()
        # alert = None

    def interact_with_table(self):
        self.close()
        # window = TableWindow(self.backend.data.tolist())
        # window.show()
        self.table_window = TableWindow(self.backend.data.tolist())
        self.table_window.show()
        # self.close()


## initialize application
app = QtWidgets.QApplication(sys.argv)

## view data file
window = MainWindow()
# window.show()

## exit application
sys.exit(app.exec_())

##
