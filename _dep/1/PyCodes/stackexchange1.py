import sys
from PyQt5 import QtWidgets # QtGui, QtCore

class FileSelectionWidget(QtWidgets.QDialog):

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
        fpath, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Select input file', '/home', '*.csv')
            # options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if fpath:
            ## check file extension
            self._fpath = fpath
            self.close()
        # print(self.fpath) # verify

class DirectorySelectionWidget(QtWidgets.QDialog):

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
        savedir = QtWidgets.QFileDialog.getExistingDirectory(
            None, "Select directory")
            # options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if savedir:
            self._savedir = savedir
            self.close()
        else:
            self.close()
        # print(self.savedir) # verify

class BackEnd():

    def __init__(self):
        super().__init__()

    # data processing functions

class Interface(BackEnd):

    def __init__(self):
        """

        """
        super().__init__()

        file_selection_widget = FileSelectionWidget()
        file_selection_widget.exec()
        # print(file_selection_widget.fpath)
        # file_selection_widget.close()

        directory_selection_widget = DirectorySelectionWidget()
        directory_selection_widget.exec()
        # print(directory_selection_widget.savedir)






        # directory_selection_widget.close()

        # self.select_data_file()
        # self.select_save_directory()
        # ... # more back-end things

    # def select_data_file(self):
    #     file_selection_widget = FileSelectionWidget()
    #     file_selection_widget.exec()
    #
    # def select_save_directory(self):
    #     directory_selection_widget = DirectorySelectionWidget()
    #     directory_selection_widget.exec()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    interface = Interface()
    sys.exit(app.exec_())

    # setQuitOnLastWindowClosed(False)
