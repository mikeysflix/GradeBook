from data_configuration import *

## specify directory to save figures
savedir = '/Users/mikeyshmikey/Desktop/Hub/Programming/GitHubRepos/GradeBook/Figures/' # None

## specify filepath of data
readdir = '/Users/mikeyshmikey/Desktop/Hub/Programming/GitHubRepos/GradeBook/Data/'
readname = 'data.csv'
readpath = '{}{}'.format(readdir, readname)

## specify row/column indices and weights
kwargs = {
    'index_type' : 'column',
    'name_index' : 0,
    'id_index' : 1,
    # 'email_index' : ,
    'homework_index' : np.arange(3, 13, 1).astype(int),
    'homework_weight' : 10,
    'exam_index' : (13, 14),
    'exam_weight' : (30, 45),
    # 'extra_credit_index' : ,
    # 'extra_credit_weight' : ,
    'ace_score' : 170,
    'fail_score' : 100,
    'flat_curve' : 2.5,
    'homework_curve' : 1,
    'exam_curve' : 1,
    'decimals' : 2
            }

def main():
    GB = GradeBook(savedir)
    GB.initialize(readpath, **kwargs)

    ## view distribution histograms
    GB.view_distribution_histogram(sources=('homework', 'exam', 'grade'), percents=[0, 50, 75, 100], show_statistics=True, figsize=(12,7), save=True)
    GB.view_distribution_histogram(sources='curve', show_statistics=True, figsize=(12,7), save=True)
    GB.view_distribution_histogram(headers='total', percents=[0, 50, 75, 100], show_statistics=True, figsize=(12,7), save=True)

    ## view distribution stacks
    GB.view_distribution_stacks(sources=('homework', 'exam', 'curve'), percents=[0, 50, 75, 100], edgecolor='k', figsize=(12,7), save=True)
    GB.view_distribution_stacks(sources=('homework', 'exam', 'curve'), percents=[0, 50, 75, 100], differentiate_sources=True, identifier_label='id number', figsize=(12,7), save=True)

    ## view distribution heatmaps
    GB.view_distribution_heatmap('grade', show_dissimilarity=True, show_ticklabels=True, mask_diagonal=True, figsize=(12,7), save=True)
    GB.view_distribution_heatmap(sources=('homework', 'exam', 'curve'), figsize=(12,7), save=True)
    GB.view_distribution_heatmap(headers='total', mask_diagonal=True, figsize=(12,7), save=True)

    ## view distribution box-plotss
    GB.view_distribution_boxplots(sources=('homework', 'exam'), showmeans=True, showfliers=True, figsize=(12,7), save=True)
    GB.view_distribution_boxplots('curve', group_by_points=True, figsize=(12,7), save=True)

    ## get students per missing/zero assignments
    missed_scores = GB.get_students_per_missing_score()
    print(missed_scores)

    ## read data for select students
    student = GB.select_student_by_prompt(identifiers=('id number', 'name')) # '11111', 'Rick Sanchez'
    # student = GB.select_student_by_prompt()
    student.reveal(show_identifiers=True, show_assignments=True, show_grade=True, show_rank=True)

    ## email students
    attachments = GB.get_all_attachments()
    GB.email_students(attachments=attachments)

if __name__ == "__main__":
    main()

##
