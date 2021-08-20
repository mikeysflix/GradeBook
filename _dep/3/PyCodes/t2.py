import sys

from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow,
                             QMessageBox, QPushButton, QVBoxLayout,
                             QWidget)


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        self.button = QPushButton(parent=self, text="Click Me!")
        self.button.clicked.connect(self.button_clicked_kill)
        self.text = QLabel(parent=self, text='')

        layout.addWidget(self.button)
        layout.addWidget(self.text)

    def button_clicked_kill(self):
        reply = QMessageBox.question(self, 'Title', 'You lost! Continue?')
        if reply == QMessageBox.Yes:
            self.text.setText('User answered yes')
        if reply == QMessageBox.No:
            self.text.setText('User answered no')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MyApp()
    gui.show()
    sys.exit(app.exec_())
