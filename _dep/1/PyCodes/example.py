from gradebook_configuration import *

savedir = '/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Figures/'
fpath = '/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Data/data.csv'

if __name__ == '__main__':

    grade_book = GradeBookInterface()

    ## read data for select students
    student = grade_book.select_student_by_prompt(identifiers=('id number', 'name')) # '11111', 'Rick Sanchez'
    # student = self.select_student_by_prompt()
    print(student)




#     GB = GradeBook(
#         bias='left',
#         savedir=savedir)
#     GB.initialize_raw_data(
#         fpath=fpath,
#         index_by='column')
#     GB.initialize_identifiers(
#         name_loc=0,
#         id_loc=1,
#         email_loc=None)
#     GB.initialize_weighted_points(
#         homework_loc=np.arange(3, 13).astype(int),
#         homework_weight=10,
#         extra_credit_loc=None,
#         extra_credit_weight=None,
#         exam_loc=(13, 14),
#         exam_weight=(30, 45))
#
#     GB.initialize_grading_criteria(
#         fail_score=100,
#         ace_score=170,
#         decimals=2)
#     GB.initialize_curves(
#         flat_curve=2.5,
#         homework_curve=1,
#         exam_curve=1,
#         extra_credit_curve=None)
#     GB.initialize_grade_points()
#     GB.initialize_grade_ranks()
#     GB.initialize_students()
#
#
#
#     # ## read data for select students
#     # student = GB.select_student_by_prompt(identifiers=('id number', 'name')) # '11111', 'Rick Sanchez'
#     # # student = grade_book.select_student_by_prompt()
#     # print(student)
#     #
#     # ## get students per missing/zero assignments
#     # missed_scores = GB.get_students_per_missing_score()
#     # print(missed_scores)
#
#     ## view distribution histograms
#     GB.view_distribution_histogram(
#         headers='total',
#         percents=[0, 50, 75, 100],
#         show_statistics=True,
#         figsize=(12,7),
#         save=True)
#     GB.view_distribution_histogram(
#         sources=('homework', 'exam', 'grade'),
#         percents=[0, 50, 75, 100],
#         show_statistics=True,
#         figsize=(12,7),
#         save=True)
#     GB.view_distribution_histogram(
#         sources='curve',
#         show_statistics=True,
#         figsize=(12,7),
#         save=True)
#
#     ## view distribution stacks
#     GB.view_distribution_stacks(
#         sources=('homework', 'exam', 'curve'),
#         percents=[0, 50, 75, 100],
#         edgecolor='k',
#         figsize=(12,7),
#         save=True)
#     GB.view_distribution_stacks(
#         sources=('homework', 'exam', 'curve'),
#         percents=[0, 50, 75, 100],
#         differentiate_sources=True,
#         identifier_label='id number',
#         figsize=(12,7),
#         save=True)
#
#     ## view distribution heatmaps
#     GB.view_distribution_heatmap(
#         'grade',
#         show_dissimilarity=True,
#         show_ticklabels=True,
#         mask_diagonal=True,
#         figsize=(12,7),
#         save=True)
#     GB.view_distribution_heatmap(
#         sources=('homework', 'exam', 'curve'),
#         figsize=(12,7),
#         save=True)
#     GB.view_distribution_heatmap(
#         headers='total',
#         mask_diagonal=True,
#         figsize=(12,7),
#         save=True)
#
#     ## view distribution box-plots
#     GB.view_distribution_boxplots(
#         sources=('homework', 'exam'),
#         showmeans=True,
#         showfliers=True,
#         figsize=(12,7),
#         save=True)
#     GB.view_distribution_boxplots(
#         'curve',
#         group_by_points=True,
#         figsize=(12,7),
#         save=True)
#
# #
