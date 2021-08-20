import sys
from PyQt5 import QtWidgets #, QtGui, QtCore

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
        fpath, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Select input file', '/home', '',
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self._fpath = fpath
        self.close()

    def prompt_verification(self):
        alert = QtWidgets.QMessageBox()
        alert.setText('The input filepath you selected is: \n{}'.format(self.fpath))
        alert.exec()

if __name__ == '__main__':

    ## initialize application
    app = QtWidgets.QApplication(sys.argv)

    ## select path of input data file
    file_selection_widget = FileSelectionWidget()
    file_selection_widget.show()

    print("\n .. FPATH:\n{}\n".format(file_selection_widget.fpath))

    ## ... back end loads data file and processes data
    ## ... more gui

    ## exit application
    sys.exit(app.exec_())




##
