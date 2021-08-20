import sys
from PyQt5 import QtWidgets, QtGui, QtCore
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QLineEdit, QFileDialog, QPushButton, QMessageBox, QMainWindow, QTableView
# from PyQt5.QtGui import QIcon
from backend_methods import *

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
        self._include_names = False
        self._include_id_numbers = False
        self._include_email_addresses = False
        self._include_homework = False
        self._include_exam = False
        self._include_extra_credit = False
        super().__init__()
        self.table = QtWidgets.QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
        self.setWindowTitle("Data Table")
        # self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

    @property
    def include_names(self):
        return self._include_names

    @property
    def include_id_numbers(self):
        return self._include_id_numbers

    @property
    def include_email_addresses(self):
        return self._include_email_addresses

    @property
    def include_homework(self):
        return self._include_homework

    @property
    def include_exam(self):
        return self._include_exam

    @property
    def include_extra_credit(self):
        return self._include_extra_credit

class IdentifiersSelectionPrompt(QtWidgets.QWidget):

    def __init__(self, data_table, index_by):
        self.data_table = data_table
        self.index_by = index_by
        super().__init__()
        self.setWindowTitle("Select student identifiers")
        self.name_checkbox = QtWidgets.QCheckBox("include student names")
        self.id_number_checkbox = QtWidgets.QCheckBox("include student ID numbers")
        self.email_address_checkbox = QtWidgets.QCheckBox("include student email addresses")
        self.enter_box = QtWidgets.QPushButton("enter")
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(self.name_checkbox)
        lay.addWidget(self.id_number_checkbox)
        lay.addWidget(self.email_address_checkbox)
        lay.addWidget(self.enter_box)
        self.setLayout(lay)
        self.name_checkbox.stateChanged.connect(self.select_name_checkbox)
        self.id_number_checkbox.stateChanged.connect(self.select_id_number_checkbox)
        self.email_address_checkbox.stateChanged.connect(self.select_email_address_checkbox)
        self.enter_box.clicked.connect(self.select_identifiers_from_table)

    def select_name_checkbox(self, toggle):
        if toggle == QtCore.Qt.Checked:
            self.data_table._include_names = True
        else:
            self.data_table._include_names = False

    def select_id_number_checkbox(self, toggle):
        if toggle == QtCore.Qt.Checked:
            self.data_table._include_id_numbers = True
        else:
            self.data_table._include_id_numbers = False

    def select_email_address_checkbox(self, toggle):
        if toggle == QtCore.Qt.Checked:
            self.data_table._include_email_addresses = True
        else:
            self.data_table._include_email_addresses = False

    def select_identifiers_from_table(self):
        if not any([self.data_table.include_names, self.data_table.include_id_numbers, self.data_table.include_email_addresses]):
            raise ValueError("at least one checkbox must be selected")

        if self.data_table.include_names:
            alert = QtWidgets.QMessageBox()
            alert.setText("From the data table, select any one cell of the {} containing names.".format(self.index_by))
            alert.exec_()
            # ...
            # self._name_index = ...

            #

            # rows = sorted(set(index.row() for index in self.data_table.selectedIndexes()))
            # print(rows)

            # if self.index_by == 'row':
            #     row = self.data_table.currentRow()
            #     print(row)
            # else:
            #     col = self.data_table.indexAt(clickme.parent().pos())
            #     print(col)

        if self.data_table.include_id_numbers:
            alert = QtWidgets.QMessageBox()
            alert.setText("From the data table, select any one cell of the {} containing ID numbers.".format(self.index_by))
            alert.exec_()
            # ...
            # self._id_number_index = ...

        if self.data_table.include_email_addresses:
            alert = QtWidgets.QMessageBox()
            alert.setText("From the data table, select any one cell of the {} containing email addresses.".format(self.index_by))
            alert.exec_()
            # ...
            # self._email_address_index = ...
        self.close()

class PointSourcesSelectionPrompt(QtWidgets.QWidget):

    def __init__(self, data_table, index_by):
        self.data_table = data_table
        self.index_by = index_by
        super().__init__()
        self.setWindowTitle("Select sources of student points")
        self.homework_checkbox = QtWidgets.QCheckBox("include homework points")
        self.exam_checkbox = QtWidgets.QCheckBox("include exam points")
        self.extra_credit_checkbox = QtWidgets.QCheckBox("include extra credit points")
        self.enter_box = QtWidgets.QPushButton("enter")
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(self.homework_checkbox)
        lay.addWidget(self.exam_checkbox)
        lay.addWidget(self.extra_credit_checkbox)
        lay.addWidget(self.enter_box)
        self.setLayout(lay)
        self.homework_checkbox.stateChanged.connect(self.select_homework_checkbox)
        self.exam_checkbox.stateChanged.connect(self.select_exam_checkbox)
        self.extra_credit_checkbox.stateChanged.connect(self.select_extra_credit_checkbox)
        self.enter_box.clicked.connect(self.select_point_sources_from_table)

    def select_homework_checkbox(self, toggle):
        if toggle == QtCore.Qt.Checked:
            self.data_table._include_homework = True
        else:
            self.data_table._include_homework = False

    def select_exam_checkbox(self, toggle):
        if toggle == QtCore.Qt.Checked:
            self.data_table._include_exam = True
        else:
            self.data_table._include_exam = False

    def select_extra_credit_checkbox(self, toggle):
        if toggle == QtCore.Qt.Checked:
            self.data_table._include_extra_credit = True
        else:
            self.data_table._include_extra_credit = False

    def select_point_sources_from_table(self):
        if not any([self.data_table.include_homework, self.data_table.include_exam, self.data_table.include_extra_credit]):
            raise ValueError("at least one checkbox must be selected")
        if self.data_table.include_homework:
            alert = QtWidgets.QMessageBox()
            alert.setText("From the data table, select any cells of all {}s containing homework points.".format(self.index_by))
            alert.exec_()

            x = self.data_table.table.selectedIndexes()
            print(x)
            # ...
            # self._homework_indices = ...
        if self.data_table.include_exam:
            alert = QtWidgets.QMessageBox()
            alert.setText("From the data table, select any cells of all {}s containing exam points.".format(self.index_by))
            alert.exec_()
            # ...
            # self._exam_indices = ...
        if self.data_table.include_extra_credit:
            alert = QtWidgets.QMessageBox()
            alert.setText("From the data table, select any cells of all {}s containing extra credit points.".format(self.index_by))
            alert.exec_()
            # ...
            # self._extra_credit_indices = ...
        self.close()

class MainWindow(QtWidgets.QMainWindow):


    """
    This class contains all GUI methods.

    (1)
        The user is prompted to select the input data file. A pop-up will
        display the selected filepath to the user. Using this filepath, the
        raw data will be loaded into the back-end.

    (2)
        The raw data is displayed to the user in a table format. A pop-up
        will prompt the user to index the table by row or column.

    (3)
        The user selects the rows or columns that corresponds to identifiers.
        Identifiers include name, ID number, and email address.

    (4)
        The user selects the rows or columns that corresponds to point sources.
        Point sources include homework, exams, and extra credit. The user
        must also select corresponding weights for point sources.

    (5)
        The user selects the grading criteria.

    (6)
        The user selects the curving criteria.

    (7)
        The back-end runs its analyis. The analysis includes assigning grades,
        calculating statistics, and initializing student data.

    (8)
        The user selects a save directory, in which figures can be saved.

    (9)
        The user can now save images, have students see their progress through
        automated pop-ups (with student verification methods), log grades, and
        email students. Figures include heat-maps of point differences between
        students, stacked and unstacked histograms for point distributions, and
        box-plots showing various statistics.
    """

    def __init__(self):
        self._backend = GradeBookVisualizer(bias='left')
        self._fpath = None
        self._data_table_window = None
        self._index_by = None
        self._identifiers_selection_prompt = None
        self._point_sources_selection_prompt = None
        self._name_index = None
        self._id_number_index = None
        self._email_address_index = None
        self._homework_indices = []
        self._exam_indices = []
        self._extra_credit_indices = []
        super().__init__()
        self.text = QtWidgets.QLabel(parent=self, text='')
        self.initialize_ui()

    @property
    def backend(self):
        return self._backend

    @property
    def fpath(self):
        return self._fpath

    @property
    def data_table_window(self):
        return self._data_table_window

    @property
    def index_by(self):
        return self._index_by

    @property
    def identifiers_selection_prompt(self):
        return self._identifiers_selection_prompt

    @property
    def point_sources_selection_prompt(self):
        return self._point_sources_selection_prompt

    @property
    def name_index(self):
        return self._name_index

    @property
    def id_number_index(self):
        return self._id_number_index

    @property
    def email_address_index(self):
        return self._email_address_index

    @property
    def homework_indices(self):
        return self._homework_indices

    @property
    def exam_indices(self):
        return self._exam_indices

    @property
    def extra_credit_indices(self):
        return self._extra_credit_indices

    def initialize_ui(self):
        self.select_input_data_file()
        self.verify_input_data_file()
        self.show_data_table()
        self.select_data_table_index_method()
        self.select_student_identifiers()
        # self.select_point_sources()

    def view_clicked_identifiers_cell(self, clickedIndex):
        row=clickedIndex.row()
        model=clickedIndex.model()

    def view_clicked_points_cell(self, clickedIndex):
        row=clickedIndex.row()
        model=clickedIndex.model()

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
        extension = Path(self.fpath).suffix
        if extension not in self.backend.allowed_fpath_extensions:
            raise ValueError("invalid file extension: {}; allowed filepath extensions are: {}".format(extension, self.backend.allowed_fpath_extensions))
        alert = QtWidgets.QMessageBox()
        alert.setText('The input filepath you selected is: \n{}'.format(self.fpath))
        alert.exec_()
        # alert.close()
        # alert = None

    def show_data_table(self):
        self._backend.initialize_raw_data(self.fpath)
        self._data_table_window = TableWindow(self.backend.raw_data.tolist())
        self._data_table_window.show()

    def select_data_table_index_method(self):
        prompt_header = "select method to index data table"
        prompt_text = "Is the data table indexed by column (as opposed to row)? If each row corresponds to a unique student, then select 'yes'. Otherwise, select 'no'."
        reply = QtWidgets.QMessageBox.question(self, prompt_header, prompt_text)
        if reply == QtWidgets.QMessageBox.Yes:
            self.text.setText('index by column')
            self._index_by = 'column'
        elif reply == QtWidgets.QMessageBox.No:
            self.text.setText('index by row')
            self._index_by = 'row'
        else:
            raise ValueError("invalid reply: {}".format(reply))
        self._backend.finalize_raw_data(self.index_by)

    def select_student_identifiers(self):
        self.data_table_window.table.clicked.connect(self.view_clicked_identifiers_cell)
        # self.data_table_window.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self._identifiers_selection_prompt = IdentifiersSelectionPrompt(
            index_by=self.index_by,
            data_table=self.data_table_window)
        self._identifiers_selection_prompt.show()

    # def select_point_sources(self):
    #     self._point_sources_selection_prompt = PointSourcesSelectionPrompt(
    #         index_by=self.index_by,
    #         data_table=self.data_table_window)
    #     self._point_sources_selection_prompt.show()













##
