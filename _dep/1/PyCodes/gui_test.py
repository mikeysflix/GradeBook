import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class InterFaceTest():

    def __init__(self):
        """

        """
        super().__init__()
        self.app = QApplication([])

    def select_read_path(self):
        # label = QLabel('Select the data file you would like to read from')
        # label.show()
        fpath = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
        return fpath

    def select_save_path(self):
        """

        """
        # app = QApplication([])
        savedir = QFileDialog.getExistingDirectory(None, "Select Directory")
        print("\n .. SAVEDIR:\n{}\n".format(savedir))
        # savedir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        # app.exec()
        return savedir

    def rw(self):
        """

        """
        fpath = self.select_read_path()
        savedir = self.select_save_path()
        return fpath, savedir



if __name__ == '__main__':

    interface = InterFaceTest()
    fpath, savedir = interface.rw()
    print(" .. FPATH:\n{}\n".format(fpath))
    print(" .. SAVEDIR:\n{}\n".format(savedir))


    interface.app.exec()






# from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog
#
# # from tkinter.filedialog import askopenfilename
# # # filename = askopenfilename()
#
# app = QApplication([])
#
# # label = QLabel('Hello World')
# # label.show()
#
# fname = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
# print(fname)
# print(fname[0])
#
# app.exec()
