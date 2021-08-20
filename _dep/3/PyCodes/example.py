from frontend_methods import *

if __name__ == '__main__':

    backend = GradeBookVisualizer(bias='left')

    backend.initialize_raw_data(fpath='/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Data/data.csv')
    # backend.initialize_raw_data(fpath='/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Data/data.txt')
    # backend.initialize_raw_data(fpath='/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Data/data.xlsx')
    backend.finalize_raw_data(index_by='column')

    backend.initialize_identifiers(
        name_loc=0,
        id_loc=1,
        email_loc=None)

    backend.initialize_weighted_points(
        homework_loc=np.arange(3, 13).astype(int),
        homework_weight=10,
        extra_credit_loc=None,
        extra_credit_weight=None,
        exam_loc=(13, 14),
        exam_weight=(30, 45))

    backend.initialize_grading_criteria(
        fail_score=100,
        ace_score=170,
        decimals=2)

    backend.initialize_curves(
        flat_curve=2.5,
        homework_curve=1,
        exam_curve=1,
        extra_credit_curve=None)

    backend.initialize_grade_points()
    backend.initialize_grade_ranks()
    backend.initialize_students()
    backend.initialize_network_graph()

    for layout_id in ('classic', 'circular'):
        for scheme in ('plain v1', 'plain v1 +', 'plain v2', 'plain v2 +', 'color-matching', 'color-matching +'):
            backend.view_bipartite_network_graph(
                layout_id=layout_id,
                scheme=scheme)



    backend.visual_configuration.update_save_directory(savedir='/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Figures/')

    student = backend.select_student_by_prompt(identifiers=('id number', 'name')) # '11111', 'Rick Sanchez'
    # student = grade_book.select_student_by_prompt()

    ## get students per missing/zero assignments
    missed_scores = backend.get_students_per_missing_score()
    print(missed_scores)







    # ## view distribution histograms
    # backend.view_distribution_histogram(
    #     headers='total',
    #     percents=[0, 50, 75, 100],
    #     show_statistics=True,
    #     figsize=(12,7),
    #     save=True)
    # backend.view_distribution_histogram(
    #     sources=('homework', 'exam', 'grade'),
    #     percents=[0, 50, 75, 100],
    #     show_statistics=True,
    #     figsize=(12,7),
    #     save=True)
    # backend.view_distribution_histogram(
    #     sources='curve',
    #     show_statistics=True,
    #     figsize=(12,7),
    #     save=True)
    #
    # ## view distribution stacks
    # backend.view_distribution_stacks(
    #     sources=('homework', 'exam', 'curve'),
    #     percents=[0, 50, 75, 100],
    #     edgecolor='k',
    #     figsize=(12,7),
    #     save=True)
    # backend.view_distribution_stacks(
    #     sources=('homework', 'exam', 'curve'),
    #     percents=[0, 50, 75, 100],
    #     differentiate_sources=True,
    #     identifier_label='id number',
    #     figsize=(12,7),
    #     save=True)
    #
    # ## view distribution heatmaps
    # backend.view_distribution_heatmap(
    #     'grade',
    #     show_dissimilarity=True,
    #     show_ticklabels=True,
    #     mask_diagonal=True,
    #     figsize=(12,7),
    #     save=True)
    # backend.view_distribution_heatmap(
    #     sources=('homework', 'exam', 'curve'),
    #     figsize=(12,7),
    #     save=True)
    # backend.view_distribution_heatmap(
    #     headers='total',
    #     mask_diagonal=True,
    #     figsize=(12,7),
    #     save=True)
    #
    # ## view distribution box-plots
    # backend.view_distribution_boxplots(
    #     sources=('homework', 'exam'),
    #     showmeans=True,
    #     showfliers=True,
    #     figsize=(12,7),
    #     save=True)
    # backend.view_distribution_boxplots(
    #     'curve',
    #     group_by_points=True,
    #     figsize=(12,7),
    #     save=True)

#




##
