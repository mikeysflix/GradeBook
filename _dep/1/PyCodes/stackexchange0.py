import sys
from PyQt5 import QtWidgets # QtGui, QtCore

class FileSelectionWidget(QtWidgets.QWidget):

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
        print(self.fpath) # verify

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
        print(self.savedir) # verify

class BackEnd():

    def __init__(self):
        super().__init__()

    # data processing functions

class Interface(BackEnd):

    def __init__(self):
        """

        """
        super().__init__()
        self.select_data_file()
        self.select_save_directory()
        ... # more back-end things

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

if __name__ == '__main__':
    interface = Interface()
