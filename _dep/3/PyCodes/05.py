import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Screen(QWidget):
    def __init__(self):
        super(Screen, self).__init__()
        self.setLayout(QVBoxLayout())

        widget1 = QPushButton("Text1", self)
        widget3 = QLabel("Text3", self)

        self.widget2_layout = QHBoxLayout()
        self.change_widget2()

        self.layout().addWidget(widget1)
        self.layout().addLayout(self.widget2_layout)
        self.layout().addWidget(widget3)

        widget1.clicked.connect(self.change_widget2)

    def clearLayout(self, layout):
        item = layout.takeAt(0)
        while item:
            w = item.widget()
            if w:
                w.deleteLater()
            lay = item.layout()
            if lay:
                self.clearLayout(item.layout())
            item = layout.takeAt(0)

    def change_widget2(self):
        self.clearLayout(self.widget2_layout)

        # change the widget.
        import random
        widgets = [QLabel, QLineEdit, QPushButton]
        widget2 = widgets[random.randint(0, len(widgets)-1)]("widget2", self)

        self.widget2_layout.addWidget(widget2)

app = QApplication(sys.argv)
Gui = Screen()
sys.exit(app.exec_())



# class ClickableWidget(QWidget):
#     clicked = pyqtSignal(int)
#     def  __init__(self, n=5, parent=None):
#         QWidget.__init__(self, parent)
#         self.hlayout = QVBoxLayout(self)
#         for i in range(n):
#             label = QLabel("btn {}".format(i), self)
#             label.setProperty("index", i)
#             self.hlayout.addWidget(label)
#             label.installEventFilter(self)
#
#     def eventFilter(self, obj, event):
#         if isinstance(obj, QLabel) and event.type() == QEvent.MouseButtonPress:
#             i = obj.property("index")
#             self.clicked.emit(i)
#         return QWidget.eventFilter(self, obj, event)
#
# class DynamicWidget(QWidget):
#     def  __init__(self, parent=None):
#         QWidget.__init__(self, parent)
#         self.hlayout = QVBoxLayout(self)
#
#     def changeWidget(self, n):
#         def clearLayout(layout):
#             item = layout.takeAt(0)
#             while item:
#                 w = item.widget()
#                 if w:
#                     w.deleteLater()
#                 lay = item.layout()
#                 if lay:
#                     clearLayout(item.layout())
#                 item = layout.takeAt(0)
#
#         clearLayout(self.hlayout)
#         for i in range(n):
#             label = QLabel("btn {}".format(i), self)
#             self.hlayout.addWidget(label)
#
#
# class Screen(QWidget):
#     def __init__(self):
#         super(Screen, self).__init__()
#         self.layout = QHBoxLayout(self)
#         c = ClickableWidget(6, self)
#         d = DynamicWidget(self)
#         c.clicked.connect(d.changeWidget)
#         self.layout.addWidget(c)
#         self.layout.addWidget(d)
#
# app = QApplication(sys.argv)
# Gui = Screen()
# sys.exit(app.exec_())
