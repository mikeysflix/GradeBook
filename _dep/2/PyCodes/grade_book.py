from interface_configuration import *

if __name__ == '__main__':

    ## initialize application
    app = QtWidgets.QApplication(sys.argv)
    grade_book = GradeBookVisualizer()

    ## select path of input data file
    file_selection_widget = FileSelectionWidget(grade_book)
    file_selection_widget.show()

    ## exit application
    sys.exit(app.exec_())
