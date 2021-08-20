from interface_configuration import *

# class GradeBookInterface(GradeBookVisualizer):
#
#     def select_read_path(self):
#         # label = QLabel('Select the data file you would like to read from')
#         # label.show()
#         fpath = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
#         app.exec()
#         return fpath
#
#     def select_save_path(self):
#         """
#
#         """
#         app = QApplication([])
#         savedir = QFileDialog.getExistingDirectory(None, "Select Directory")
#         print("\n .. SAVEDIR:\n{}\n".format(savedir))
#         # savedir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
#         app.exec()
#         return savedir
#
#
#     def __init__(self):
#         """
#
#         """
#         bias = 'left' # ...
#         savedir = self.select_save_path()
#         super().__init__(
#             bias=bias,
#             savedir=savedir)
#
#         fpath = self.select_read_path()
#         self.initialize_raw_data(
#             fpath=fpath,
#             index_by='column')
#
#         self.initialize_identifiers(
#             name_loc=0,
#             id_loc=1,
#             email_loc=None)
#         self.initialize_weighted_points(
#             homework_loc=np.arange(3, 13).astype(int),
#             homework_weight=10,
#             extra_credit_loc=None,
#             extra_credit_weight=None,
#             exam_loc=(13, 14),
#             exam_weight=(30, 45))
#
#         self.initialize_grading_criteria(
#             fail_score=100,
#             ace_score=170,
#             decimals=2)
#         self.initialize_curves(
#             flat_curve=2.5,
#             homework_curve=1,
#             exam_curve=1,
#             extra_credit_curve=None)
#         self.initialize_grade_points()
#         self.initialize_grade_ranks()
#         self.initialize_students()
#
#     def __call__(self):
#         """
#
#         """
#         app = QApplication([])




# if __name__ == '__main__':






# fname = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
# print(fname)
# print(fname[0])
#
# app.exec()











##
