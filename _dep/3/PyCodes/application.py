# from frontend_methods import *
from _frontend_methods import *

if __name__ == '__main__':

    ## initialize application
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    # window.show()

    ## exit application
    sys.exit(app.exec_())
