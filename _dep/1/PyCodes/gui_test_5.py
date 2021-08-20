import csv
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QInputDialog, QLineEdit, QFileDialog, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QListWidget, QAbstractItemView, QListWidgetItem
from visual_configuration import *

def get_filepath_to_read():
    app = QApplication(sys.argv)
    fpath = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
    return fpath
    # sys.exit(app.exec_())
    app.exec()

fpath = get_filepath_to_read()
reader = csv.reader(open(fpath))

fx_elements = {}
for row in reader:
    key = row[0]
    if key in fx_elements:
        # implement your duplicate row handling here
        pass
    fx_elements[key] = row[1:]
    
lst = sorted(fx_elements.keys())
app = QApplication(sys.argv)
listWidget = QListWidget()
listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
for k in lst:
    item = QListWidgetItem(k)
    listWidget.addItem(item)





# def populate():
#     fpath = get_filepath_to_read()
#     with open(fpath, 'rt') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             item = QTreeWidgetItem(self.treeWidgetLog, row)
#
#
# populate()
