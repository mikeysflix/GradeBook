import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton

class FileBrowserWindow(QMainWindow):

    """

    """

    def __init__(self):
        app = QApplication(sys.argv)
        super().__init__()
        # self.setWindowTitle("GradeBook")
        button = QPushButton("Select the data file you want to read")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)
        app.exec_()

    def button_clicked(self, s):
        fpath = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
        return fpath

# class DirectoryBrowserWindow(QMainWindow):
#
#     """
#
#     """
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("GradeBook")
#         button = QPushButton("Select the directory to save files in")
#         button.clicked.connect(self.button_clicked)
#         self.setCentralWidget(button)
#
#     def button_clicked(self, s):
#         savedir = QFileDialog.getExistingDirectory(None, "Select Directory")
#         return savedir

if __name__ == '__main__':


    read_window = FileBrowserWindow()
    # read_window.show()

    # save_window = DirectoryBrowserWindow()
    # # save_window.show()
