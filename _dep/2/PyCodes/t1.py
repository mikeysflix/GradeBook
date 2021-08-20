import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QLineEdit, QFileDialog, QPushButton, QMessageBox, QMainWindow, QTableView
from PyQt5.QtGui import QIcon
import numpy as np
from collections import OrderedDict

class FileSelectionWidget(QtWidgets.QWidget):

    """
    This class allows the user to select the input
    data file to be read via gui.
    """

    def __init__(self, parent=None):
        self._fpath = None
        super().__init__(parent)
        button = QtWidgets.QPushButton("Click here and select the data file you want to read")
        button.clicked.connect(self.on_clicked)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(button)

    @property
    def fpath(self):
        return self._fpath

    def on_clicked(self):
        self.prompt_input_file()
        self.prompt_verification()

    def prompt_input_file(self):
        dialog = QtWidgets.QFileDialog(
            self,
            "Select input file",
            "path",
            "*.csv",
            supportedSchemes=["file"],
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        fpath = dialog.getOpenFileName(None, 'Open file', '/home')[0]
        self._fpath = fpath
        self.close()

    def prompt_verification(self):
        alert = QMessageBox()
        alert.setText('The input filepath you selected is: \n{}'.format(self.fpath))
        alert.exec()

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

    ## initialize application
    app = QtWidgets.QApplication(sys.argv)

    ## select path of input data file
    file_selection_widget = FileSelectionWidget()
    file_selection_widget.show()

    





    ## view data file
    window = TableWindow(self.raw_data.tolist())
    window.show()



    ## exit application
    sys.exit(app.exec_())


##



##
