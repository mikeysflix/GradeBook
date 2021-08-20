import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QLineEdit, QFileDialog, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
from visual_configuration import *

class TableModel(QtCore.QAbstractTableModel):

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

    def __init__(self, data):
        super().__init__()
        self.table = QtWidgets.QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

class GradeBookInterface(GradeBookVisualizer):

    def __init__(self):
        """

        """
        fpath = self.get_filepath_to_read()
        savedir = self.get_directory_to_save()
        super().__init__(
            bias='left',
            savedir=savedir)

        self.initialize_raw_data(fpath=fpath)

        self.view_raw_data_table()

        # index_by = ... # 'column'
        # self.initialize_raw_data(
        #     fpath=fpath,
        #     index_by=index_by)
        #
        # name_loc = ... # 0
        # id_loc = ... # 1
        # email_loc = ... # None
        # self.initialize_identifiers(
        #     name_loc=name_loc,
        #     id_loc=id_loc,
        #     email_loc=email_loc)
        #
        # homework_loc = ... # np.arange(3, 13).astype(int)
        # homework_weight = ... # 10
        # extra_credit_loc = ... # None
        # extra_credit_weight = ... # None
        # exam_loc = ... # (13, 14)
        # exam_weight = ... # (30, 45)
        # self.initialize_weighted_points(
        #     homework_loc=homework_loc,
        #     homework_weight=homework_weight,
        #     extra_credit_loc=extra_credit_loc,
        #     extra_credit_weight=extra_credit_weight,
        #     exam_loc=exam_loc,
        #     exam_weight=exam_weight)
        #
        # fail_score = ... # 100
        # ace_score = ... # 170
        # decimals = ... # 2
        # self.initialize_grading_criteria(
        #     fail_score=fail_score,
        #     ace_score=ace_score,
        #     decimals=decimals)
        #
        # flat_curve = ... # 2.5
        # homework_curve = ... # 1
        # exam_curve = ... # 1
        # extra_credit_curve = ... # None
        # self.initialize_curves(
        #     flat_curve=flat_curve,
        #     homework_curve=homework_curve,
        #     exam_curve=exam_curve,
        #     extra_credit_curve=extra_credit_curve)
        # self.initialize_grade_points()
        # self.initialize_grade_ranks()
        # self.initialize_students()


    @staticmethod
    def get_filepath_to_read():
        app = QApplication(sys.argv)
        label = QLabel('Select the data file you would like to read from')
        label.show()
        fpath = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
        return fpath
        # sys.exit(app.exec_())
        app.exec()

    @staticmethod
    def get_directory_to_save():
        app = QApplication(sys.argv)
        label = QLabel('Select the directory in which you would like to save files')
        label.show()
        savedir = QFileDialog.getExistingDirectory(None, "Select Directory")
        return savedir
        # sys.exit(app.exec_())
        app.exec()

    @staticmethod
    def select_data_index_by():
        index_by = ...
        return index_by

    def view_raw_data_table(self):
        app = QApplication(sys.argv)
        window = TableWindow(self.raw_data.tolist())
        window.show()
        QMessageBox.about(self, "Title", "Message")
        # sys.exit(app.exec_())
        app.exec_()






class FileSelectionWidget(QtWidgets.QWidget):

    """

    """

    def __init__(self, parent=None):
        super().__init__(parent)
        app = QApplication(sys.argv)
        button = QtWidgets.QPushButton(caption)
        button.clicked.connect(self.on_clicked)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(button)

    @QtCore.pyqtSlot()
    def on_clicked(self):
        fpath = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
        return fpath
        sys.exit(app.exec_())



##
