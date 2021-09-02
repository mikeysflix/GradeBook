from backend_methods import *

## initialize path to data file
fpath = '.../Gradebook/data.csv'
# fpath = '.../Gradebook/data.txt'
# fpath = '.../Gradebook/data.xlsx'

## initialize path to save figures
savedir = '.../GradeBook/Figures/'
save = True

if __name__ == '__main__':

    ## initialize back-end
    backend = GradeBookVisualizer()
    backend.initialize_raw_data(
        fpath=fpath)
    backend.finalize_raw_data(
        index_by='column')
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
    backend.initialize_grade_counter()
    backend.initialize_network_graph()
    backend.visual_configuration.update_save_directory(
        savedir=savedir)

    ## view distribution histograms
    backend.view_distribution_histogram(
        headers='total',
        percents=[0, 50, 75, 100],
        show_statistics=True,
        figsize=(12,7),
        save=save)
    backend.view_distribution_histogram(
        sources=('homework', 'exam', 'grade'),
        percents=[0, 50, 75, 100],
        show_statistics=True,
        figsize=(12,7),
        save=save)
    backend.view_distribution_histogram(
        sources='curve',
        show_statistics=True,
        figsize=(12,7),
        save=save)

    ## view distribution stacks
    backend.view_distribution_stacks(
        sources=('homework', 'exam', 'curve'),
        percents=[0, 50, 75, 100],
        edgecolor='k',
        figsize=(12,7),
        save=save)
    backend.view_distribution_stacks(
        sources=('homework', 'exam', 'curve'),
        percents=[0, 50, 75, 100],
        differentiate_sources=True,
        identifier_label='id number',
        figsize=(12,7),
        save=save)

    ## view distribution heatmaps
    backend.view_distribution_heatmap(
        'grade',
        show_dissimilarity=True,
        show_ticklabels=True,
        mask_diagonal=True,
        figsize=(12,7),
        save=save)
    backend.view_distribution_heatmap(
        sources=('homework', 'exam', 'curve'),
        figsize=(12,7),
        save=save)
    backend.view_distribution_heatmap(
        headers='total',
        mask_diagonal=True,
        figsize=(12,7),
        save=save)

    ## view distribution box-plots
    backend.view_distribution_boxplots(
        sources=('homework', 'exam'),
        showmeans=True,
        showfliers=True,
        figsize=(12,7),
        save=save)
    backend.view_distribution_boxplots(
        'curve',
        group_by_points=True,
        figsize=(12,7),
        save=save)

    ## view pie-charts
    backend.view_pie_chart_of_grades_distribution(
        show_annulus=False,
        save=save)
    backend.view_pie_chart_of_grades_distribution(
        show_annulus=True,
        save=save)

    ## view network diagrams
    for layout_id in ('bipartite', 'circular'):
        for scheme in ('plain', 'plain +', 'classic', 'classic +', 'color-matching', 'color-matching +'):
            backend.view_network_graph_of_grades_distribution(
                layout_id=layout_id,
                scheme=scheme,
                figsize=(12,7),
                save=save)

    ## get students per missing/zero assignments
    missed_scores = backend.get_students_per_missing_score()
    print(missed_scores)

    ## view student info by prompt
    student = backend.select_student_by_prompt(identifiers=('id number', 'name')) # '11111', 'Rick Sanchez'


##
