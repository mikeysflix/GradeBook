import sys
from PyQt5 import QtWidgets # QtGui, QtCore

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

class BinaryDirectoryWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self._savedir = None
        self.initUI()

    @property
    def savedir(self):
        return self._savedir

    def initUI(self):
        buttonReply = QtWidgets.QMessageBox.question(self, 'ssss', "Would you like to save any figures/files?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        self.close()
        if buttonReply == QtWidgets.QMessageBox.Yes:
            directory_selection_widget = DirectorySelectionWidget()
            directory_selection_widget.show()
            self._savedir = directory_selection_widget.savedir
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    file_selection_widget = FileSelectionWidget()
    file_selection_widget.show()
    binary_widget = BinaryDirectoryWidget()
    binary_widget.show()

    # directory_selection_widget = DirectorySelectionWidget()
    # directory_selection_widget.show()

    sys.exit(app.exec_())





##
