import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QLineEdit, QFileDialog, QPushButton, QMessageBox, QMainWindow, QTableView
from PyQt5.QtGui import QIcon
from visual_configuration import *

class FileSelectionWidget(QtWidgets.QWidget):

    """
    This class allows the user to select the input
    data file to be read via gui.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        button = QtWidgets.QPushButton("Click here and select the data file you want to read")
        button.clicked.connect(self.on_clicked)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(button)
        self._fpath = None

    @property
    def fpath(self):
        return self._fpath

    def on_clicked(self):
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

class DirectorySelectionWidget(QtWidgets.QWidget):

    """
    This class allows the user to select the directory
    to save files into via gui.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        button = QtWidgets.QPushButton("Click here and select the directory \nin which you would like to save files")
        button.clicked.connect(self.on_clicked)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(button)
        self._savedir = None

    @property
    def savedir(self):
        return self._savedir

    def on_clicked(self):
        dialog = QtWidgets.QFileDialog()
        savedir = dialog.getExistingDirectory(None, "Select directory")
        self._savedir = savedir
        self.close()

class GradeBookInterface(GradeBookVisualizer):

    def __init__(self):
        """

        """
        self.select_data_file()
        self.select_save_directory()

    def select_data_file(self):
        app = QtWidgets.QApplication(sys.argv)
        file_selection_widget = FileSelectionWidget()
        file_selection_widget.show()
        sys.exit(app.exec_())

    def select_save_directory(self):
        app = QtWidgets.QApplication(sys.argv)
        directory_selection_widget = DirectorySelectionWidget()
        directory_selection_widget.show()
        sys.exit(app.exec_())
















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



#
