from data_processing import *

## select directory to save to (and optionally email from) and path of data file
savedir = '/Users/mikeyshmikey/Desktop/Hub/Programming/GitHubRepos/GradeBook/Figures/'
fpath = '/Users/mikeyshmikey/Desktop/Hub/Programming/GitHubRepos/GradeBook/Data/data.csv'

if __name__ == '__main__':

    ## initialize instance of class
    grade_book = GradeBook(
        fpath=fpath,
        savedir=savedir,
        index_by='column',
        name_loc=0,
        id_loc=1,
        homework_loc=np.arange(3, 13).astype(int),
        homework_weight=10,
        # extra_credit_loc=...,
        # extra_credit_weight=...,
        exam_loc=(13, 14),
        exam_weight=(30, 45))

    ## update grade-book
    # grade_book()
    grade_book(
        ace_score=170,
        fail_score=100,
        flat_curve=2.5,
        homework_curve=1,
        exam_curve=1,
        decimals=2)

    ## read data for select students
    student = grade_book.select_student_by_prompt(identifiers=('id number', 'name')) # '11111', 'Rick Sanchez'
    # student = grade_book.select_student_by_prompt()
    print(student)

    ## get students per missing/zero assignments
    missed_scores = grade_book.get_students_per_missing_score()
    print(missed_scores)

    ## email students
    # attachments = grade_book.get_all_attachments()
    # grade_book.email_students(attachments=attachments)

    ## view distribution histograms
    grade_book.view_distribution_histogram(
        headers='total',
        percents=[0, 50, 75, 100],
        show_statistics=True,
        figsize=(12,7),
        save=True)
    grade_book.view_distribution_histogram(
        sources=('homework', 'exam', 'grade'),
        percents=[0, 50, 75, 100],
        show_statistics=True,
        figsize=(12,7),
        save=True)
    grade_book.view_distribution_histogram(
        sources='curve',
        show_statistics=True,
        figsize=(12,7),
        save=True)

    ## view distribution stacks
    grade_book.view_distribution_stacks(
        sources=('homework', 'exam', 'curve'),
        percents=[0, 50, 75, 100],
        edgecolor='k',
        figsize=(12,7),
        save=True)
    grade_book.view_distribution_stacks(
        sources=('homework', 'exam', 'curve'),
        percents=[0, 50, 75, 100],
        differentiate_sources=True,
        identifier_label='id number',
        figsize=(12,7),
        save=True)

    ## view distribution heatmaps
    grade_book.view_distribution_heatmap(
        'grade',
        show_dissimilarity=True,
        show_ticklabels=True,
        mask_diagonal=True,
        figsize=(12,7),
        save=True)
    grade_book.view_distribution_heatmap(
        sources=('homework', 'exam', 'curve'),
        figsize=(12,7),
        save=True)
    grade_book.view_distribution_heatmap(
        headers='total',
        mask_diagonal=True,
        figsize=(12,7),
        save=True)

    ## view distribution box-plots
    grade_book.view_distribution_boxplots(
        sources=('homework', 'exam'),
        showmeans=True,
        showfliers=True,
        figsize=(12,7),
        save=True)
    grade_book.view_distribution_boxplots(
        'curve',
        group_by_points=True,
        figsize=(12,7),
        save=True)







##
