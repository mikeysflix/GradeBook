from PyQt5 import *

class Ui_Dialog(object):
    def __init__(self, dbConnection):
        QtGui.QDialog.__init__(self)
        global c
        c = dbConnection

# class Ui_MainWindow(object):
#     def __init__(self, dbConnection):
#         global c
#         c = dbConnection
#
#     def launchEditWindow(self):
#         print "DEBUG: Launch edit window"
#         dialog = QtGui.QDialog()
#         dialogui = Ui_Dialog(c)
#         dialogui = setupUi(dialog)
#         dialogui.show()

class Ui_MainWindow(QtGui.QMainWindow):
    ''' some stuff '''
    def on_Button_clicked(self, checked=None):
        if checked==None: return
        dialog = QDialog()
        dialog.ui = Ui_MyDialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        conn = sqlite3.connect('meds.sqlite')
        c = conn.cursor()
        self.ui = Ui_MainWindow(c)
        self.ui.setupUi(self)

def main():
    app = QtGui.QApplication(sys.argv)
    program = StartQT4()
    program.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
