import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

def get_filepath_to_read():

    # app = QApplication([])
    app = QApplication(sys.argv)

    fpath = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]

    return fpath

    # sys.exit(app.exec_())
    app.exec()


def get_filedir_to_save():

    # app = QApplication([])
    app = QApplication(sys.argv)

    savedir = QFileDialog.getExistingDirectory(None, "Select Directory")

    return savedir

    # sys.exit(app.exec_())
    app.exec()




if __name__ == '__main__':

    fpath = get_filepath_to_read()
    print("\n .. FPATH:\n{}\n".format(fpath))

    savedir = get_filedir_to_save()
    print("\n .. SAVEDIR:\n{}\n".format(savedir))







##
