from data_processing import *
from visual_configuration import *

class GradeBookVisualizer(StudentInteractionMethods):

    def __init__(self, bias='left'):
        """

        """
        super().__init__(bias=bias)
        self.visual_configuration = VisualConfiguration()

    def get_histogram(self, arr, edges):
        """

        """
        if self.bias == 'left':
            counts, edges = np.histogram(arr, edges)
        else:
            counts = np.zeros(len(edges) - 1, dtype=int)
            for idx, val in zip(*np.unique(np.searchsorted(edges, arr, side='left'), return_counts=True)):
                counts[idx - 1] = val
        return counts, edges

    def view_grades_distribution_histogram(self, show_statistics=False, percents=None, cmap='Greens', default_color='darkorange', bin_width=None, save=False, **kwargs):
        """

        """
        ## get x-axis parameters
        if bin_width is None: ## bin by grade
            counts, edges = self.get_histogram(self.final['score'], self.grading_criteria['edges'])
            xticks = np.arange(edges.size).astype(int)
            xticklabels = np.round(edges, decimals=2)
            xticklabels[0] = 0
            xticklabels[-1] = np.inf
        else: ## customized bins
            ymax, ymin = np.max(self.final['score']), np.min(self.final['score'])
            edges = np.arange(ymin - bin_width, ymax + bin_width + 1, bin_width)
            counts, edges = self.get_histogram(self.final['score'], edges)
            xticks = edges.copy()
            xticklabels = None
        title = 'Distribution of Grades (n=${}$)'.format(self.number_of_students)
        fig, ax, midpoints, facecolors = self.visual_configuration.subview_histogram(
            edges=xticks,
            counts=counts,
            cmap=cmap,
            default_color=default_color,
            title=title,
            **kwargs)
        ## show grades above bars
        if xticklabels is not None: # cannot use custom bin-size
            for x,y,s,c in zip(midpoints, counts, self.letters, facecolors):
                ax.text(x, y +0.325, s, fontsize=self.visual_configuration.labelsize, color=c, ha='center')
            ax.set_xticklabels(xticklabels, rotation=15)
        if percents is not None:
            percents = self.visual_configuration.select_percents(percents)
            if bin_width is None:
                ploc = percents * self.total_weight / 100
                fscore = np.round(self.grading_criteria['fail'], decimals=2)
                ascore = np.round(self.grading_criteria['ace'], decimals=2)
                ## account for unequal bin-spacing (fail scores cover multiple bins)
                for i, (p, loc) in enumerate(zip(percents, ploc)):
                    test_score = p * self.total_weight / 100
                    if test_score > fscore:
                        xloc = np.max(np.where(test_score >= xticklabels[:-1])[0])
                        xp = xticklabels[xloc]
                        if test_score == xp:
                            ploc[i] = xloc
                        else:
                            dp = xp * 100 / self.grading_criteria['ace']
                            dx = xp - xticklabels[xloc-1]
                            ploc[i] = xloc + (p - dp) * dx / 100
                    else:
                        xloc = np.where(xticklabels == fscore)[0]
                        if test_score == fscore:
                            ploc[i] = xloc
                        else:
                            ploc[i] = test_score / self.grading_criteria['fail'] * xloc
            else:
                ploc = percents * self.total_weight / 100
            self.visual_configuration.subview_percents(ax, percents, ploc, mirror_axis='x', limit=None)
        ## show statistics via legend
        if show_statistics:
            self.visual_configuration.subview_statistics(fig, ax, self.final['statistics'], loc=None, decimals=2)
        ## show/save figure
        savename = 'histogram_distribution_grade' if save else None
        self.visual_configuration.display_image(fig, savename)

    def view_assignment_distribution_histogram(self, source, header, loc, score=None, show_statistics=False, percents=None, cmap='Greens', default_color='darkorange', bin_width=None, save=False, **kwargs):
        """

        """
        if score is None: ## by header
            is_total = False
            ## get scores
            score = self.points[source]['score'][:, loc[0]]
            ## unweighted scores
            if source == 'curve':
                wts = (np.ceil(score / 10.0)).astype(int) * 10
                weight = np.max(wts)
            ## weighted scores
            else:
                weight = self.points[source]['weight'][loc[0]]
            ## get statistics
            statistics = self.points[source]['statistics']
        else: ## by source total
            is_total = True
            if source == 'curve':
                wts = (np.ceil(score / 10.0)).astype(int) * 10
                weight = np.max(wts)
            else:
                weight = np.sum(self.points[source]['weight'])
            statistics = self.get_statistics(score)
        ## automatic bin-size
        if bin_width is None:
            edges = self.visual_configuration.get_histogram_edges_from_weight(weight)
        ## customized bin-size
        else:
            edges = np.arange(-0.5, weight + bin_width + 1, bin_width)
        ## get histogram parameters
        xticks = edges.copy()
        edges[0] = -1 ## edge-case: score of zero with right-bias
        edges[-1] = weight * 1000 ## edge-case: maximum score with left-bias
        counts, edges = self.get_histogram(score, edges)
        ## initialize plot
        if is_total:
            title = '{} {} Points (n=${}$)'.format(header.title(), source.title(), self.number_of_students)
        else:
            if source == 'curve':
                title = '{}-Curve Points (n=${}$)'.format(header.title(), self.number_of_students)
            else:
                title = '{} Points (n=${}$)'.format(header, self.number_of_students)
        fig, ax, _, _ = self.visual_configuration.subview_histogram(
            edges=xticks,
            counts=counts,
            cmap=cmap,
            default_color=default_color,
            title=title,
            **kwargs)
        ## show percents
        if percents is not None:
            percents = self.visual_configuration.select_percents(percents)
            ploc = percents * weight / 100
            self.visual_configuration.subview_percents(ax, percents, ploc, mirror_axis='x', limit=None)
        ## show statistics
        if show_statistics:
            i = None if is_total else loc[0]
            self.visual_configuration.subview_statistics(fig, ax, statistics, i, decimals=2)
        ## show/save figure
        if save:
            savename = 'histogram_distribution_{}_{}'.format(source.replace(' ', '_'), header.replace(' ', '_'))
        else:
            savename = None
        self.visual_configuration.display_image(fig, savename)

    def view_distribution_histogram(self, sources=None, headers=None, show_statistics=False, percents=None, cmap='Greens', default_color='darkorange', bin_width=None, save=False, **kwargs):
        """

        """
        ## view by sources
        if headers is None:
            ## group sources into iterable container
            if sources is None:
                raise ValueError("input sources OR headers")
            if isinstance(sources, str):
                sources = [sources]
            if not isinstance(sources, (tuple, list, np.ndarray)):
                raise ValueError("invalid type(sources): {}".format(type(sources)))
            for source in sources:
                if source == 'grade':
                    self.view_grades_distribution_histogram(show_statistics, percents, cmap, default_color, bin_width, save, **kwargs)
                elif source in ('homework', 'exam', 'extra credit', 'curve'): ## recursive, view per header
                    for header in self.points[source]['header']:
                        self.view_distribution_histogram(None, header, show_statistics, percents, cmap, default_color, bin_width, save, **kwargs)
                else:
                    raise ValueError("invalid element in sources: {}".format(source))
        ## view by headers
        else:
            ## group headers into iterable container
            if sources is not None:
                raise ValueError("input sources OR headers")
            if isinstance(headers, str):
                headers = [headers]
            if not isinstance(headers, (tuple, list, np.ndarray)):
                raise ValueError("invalid type(headers): {}".format(type(headers)))
            ## get source per header
            for header in headers:
                for source in ('homework', 'exam', 'extra credit', 'curve'):
                    if source in list(self.points.keys()):
                        if header == 'total':
                            self.view_assignment_distribution_histogram(source, header, None, self.points[source]['total'], show_statistics, percents, cmap, default_color, bin_width, save, **kwargs)
                        else:
                            condition = (self.points[source]['header'] == header)
                            if np.any(condition):
                                if (source == 'curve') and (percents is not None):
                                    raise ValueError("curved points cannot be converted into percentages (ie, how to define 100%)")
                                ## get index of corresponding scores
                                loc = np.nonzero(condition)[0]
                                if loc.size > 1:
                                    raise ValueError("multiple {}s share the same header: {}".format(source, header))
                                self.view_assignment_distribution_histogram(source, header, loc, None, show_statistics, percents, cmap, default_color, bin_width, save, **kwargs)

    def subview_heatmap(self, source, header, distance_matrix, distance_metric, norm, show_dissimilarity=False, show_ticklabels=False, cmap='Oranges', textcolors=('white', 'k'), interpolation='nearest', title=None, save=False, **kwargs):
        """

        """
        ## initialize plot
        fig, ax = plt.subplots(**kwargs)
        handle = ax.imshow(distance_matrix, cmap=cmap, norm=norm, interpolation=interpolation, origin='upper')
        ## configure ticks
        tick_locations = np.arange(self.number_of_students).astype(int)
        ax.set_xticks(tick_locations)
        ax.set_yticks(tick_locations)
        ## configure ticklabels
        if show_ticklabels:
            if 'id number' in list(self.identifiers.keys()):
                ax.set_xticklabels(self.identifiers['id number'], rotation=90)
                ax.set_yticklabels(self.identifiers['id number'], rotation=0)
                ax.set_xlabel('ID number', fontsize=self.visual_configuration.labelsize)
                ax.set_ylabel('ID number', fontsize=self.visual_configuration.labelsize)
            else:
                raise ValueError("cannot show ticklabels without id numbers")
        else:
            ax.set_xticklabels([], rotation=90)
            ax.set_yticklabels([], rotation=0)
        ## show dis-similarity
        if show_dissimilarity:
            text_values = np.round(distance_matrix, decimals=1)
            kws = dict(ha='center', va='center', weight='semibold', fontsize=self.visual_configuration.textsize)
            for c in range(distance_matrix.shape[1]):
                for r in range(distance_matrix.shape[0]):
                    if r == c:
                        ax.text(r, c, '', **kws)
                    else:
                        value = text_values[r, c]
                        kws['color'] = textcolors[0] if norm(value) >= 0.5 else textcolors[1]
                        ax.text(r, c, r'${}$'.format(value), **kws)
        ax.tick_params(axis='both', labelsize=self.visual_configuration.ticksize)
        ## show color-bar
        cbar = fig.colorbar(handle, ax=ax, orientation='vertical', shrink=0.5, pad=0.1, extend='max') # cmap=cmap, norm=norm,
        cbar.ax.tick_params(labelsize=self.visual_configuration.ticksize)
        cbar.ax.set_title('Dis-Similarity\nof Scores\n({} Distance)'.format(distance_metric.title()), fontsize=self.visual_configuration.labelsize)
        ## show title
        if title is not None:
            ax.set_title(title, fontsize=self.visual_configuration.titlesize)
        ## show/save plot
        if save:
            savename = 'heatmap_{}'.format(source.replace(' ', '_'))
            if header is not None:
                savename += '_{}'.format(header.replace(' ', '_'))
        else:
            savename = None
        self.visual_configuration.display_image(fig, savename)

    def view_distribution_heatmap(self, sources=None, headers=None, distance_metric='manhattan', show_dissimilarity=False, show_ticklabels=False, cmap='Oranges', textcolors=('white', 'k'), mask_diagonal=False, interpolation='nearest', save=False, **kwargs):
        """

        """
        ## view by sources
        if headers is None:
            ## group sources into iterable container
            if sources is None:
                raise ValueError("input sources OR headers")
            if isinstance(sources, str):
                sources = [sources]
            if not isinstance(sources, (tuple, list, np.ndarray)):
                raise ValueError("invalid type(sources): {}".format(type(sources)))
            for source in sources:
                if source == 'grade':
                    matrix_gen = DistanceMatrix()
                    matrix_gen.update_distance_metric(distance_metric=distance_metric)
                    distance_matrix = matrix_gen.get_distance_matrix(self.final['score'], mask_diagonal)
                    norm = Normalize(vmin=0, vmax=np.nanmax(distance_matrix))
                    title = 'Heat-Map of Grade Differences (n=${}$)'.format(self.number_of_students)
                    self.subview_heatmap(source, None, distance_matrix, distance_metric, norm, show_dissimilarity, show_ticklabels, cmap, textcolors, interpolation, title, save, **kwargs)
                elif source in ('homework', 'exam', 'extra credit', 'curve'): ## recursive, view per header
                    for header in self.points[source]['header']:
                        self.view_distribution_heatmap(None, header, distance_metric, show_dissimilarity, show_ticklabels, cmap, textcolors, mask_diagonal, interpolation, save, **kwargs)
                else:
                    raise ValueError("invalid element in sources: {}".format(source))
        ## view by headers
        else:
            ## group headers into iterable container
            if sources is not None:
                raise ValueError("input sources OR headers")
            if isinstance(headers, str):
                headers = [headers]
            if not isinstance(headers, (tuple, list, np.ndarray)):
                raise ValueError("invalid type(headers): {}".format(type(headers)))
            ## get source per header
            for header in headers:
                for source in ('homework', 'exam', 'extra credit', 'curve'):
                    if source in list(self.points.keys()):
                        if header == 'total':
                            scores = self.points[source]['total']
                            title = 'Heat-Map of Total {} Point Differences (n=${}$)'.format(source.title(), self.number_of_students)
                            matrix_gen = DistanceMatrix()
                            matrix_gen.update_distance_metric(distance_metric=distance_metric)
                            distance_matrix = matrix_gen.get_distance_matrix(scores, mask_diagonal)
                            norm = Normalize(vmin=0, vmax=np.nanmax(distance_matrix))
                            self.subview_heatmap(source, header, distance_matrix, distance_metric, norm, show_dissimilarity, show_ticklabels, cmap, textcolors, interpolation, title, save, **kwargs)
                        else:
                            condition = (self.points[source]['header'] == header)
                            if np.any(condition):
                                ## get index of corresponding scores
                                loc = np.nonzero(condition)[0]
                                if loc.size > 1:
                                    raise ValueError("multiple {}s share the same header: {}".format(source, header))
                                scores = self.points[source]['score'][:, loc[0]]
                                matrix_gen = DistanceMatrix()
                                matrix_gen.update_distance_metric(distance_metric=distance_metric)
                                distance_matrix = matrix_gen.get_distance_matrix(scores, mask_diagonal)
                                norm = Normalize(vmin=0, vmax=np.nanmax(distance_matrix))
                                if source == 'curve':
                                    title = 'Heat-Map of {}-Curve Point Differences (n=${}$)'.format(header.title(), self.number_of_students)
                                else:
                                    title = 'Heat-Map of {} Point Differences (n=${}$)'.format(header, self.number_of_students)
                                self.subview_heatmap(source, header, distance_matrix, distance_metric, norm, show_dissimilarity, show_ticklabels, cmap, textcolors, interpolation, title, save, **kwargs)

    def subview_stacks(self, ax, x, bottom, source, header, facecolor, label=None, edgecolor=None, width=0.8):
        """

        """
        if header == 'total':
            y = self.points[source]['total']
        else:
            condition = (self.points[source]['header'] == header)
            if np.any(condition):
                loc = np.nonzero(condition)[0]
                if loc.size > 1:
                    raise ValueError("multiple {}s share the same header: {}".format(source, header))
                y = self.points[source]['score'][:, loc[0]]
        ax.bar(x, y, bottom=bottom, label=label, color=facecolor, edgecolor=edgecolor, width=width)
        bottom = np.nansum([bottom, y], axis=0)
        return ax, bottom

    def view_distribution_stacks(self, sources=None, headers=None, percents=None, identifier_label=None, cmap='jet', edgecolor=None, width=0.8, differentiate_sources=False, save=False, **kwargs):
        """

        """
        ## initialize y-coordinates of bottoms of stacked bars
        bottom = np.zeros(self.number_of_students)
        ## initialize x-coordinate midpoints
        x = np.arange(self.number_of_students)
        ## initialize plot
        fig, ax = plt.subplots(**kwargs)
        ## view by sources
        if headers is None:
            ## group sources into iterable container
            if sources is None:
                raise ValueError("input sources OR headers")
            if isinstance(sources, str):
                sources = [sources]
            if not isinstance(sources, (tuple, list, np.ndarray)):
                raise ValueError("invalid type(sources): {}".format(type(sources)))
            ## get savename
            if save:
                savename = 'stacked_' + '_'.join(sources)
                if differentiate_sources:
                    savename += '_diff'
            else:
                savename = None
            ## get facecolors
            if differentiate_sources:
                nstacks = len(sources)
            else:
                nstacks = 0
                for source in sources:
                    if source in list(self.points.keys()):
                        nstacks += self.points[source]['header'].size
                    else:
                        raise ValueError("invalid source: {}".format(source))
            facecolors = iter(self.visual_configuration.select_facecolors(np.arange(nstacks), cmap, default_color=None))
            ## iteratively plot
            for source in sources:
                if differentiate_sources:
                    ax, bottom = self.subview_stacks(ax, x, bottom, source, 'total', next(facecolors), source.title(), edgecolor, width)
                else:
                    for header in self.points[source]['header']:
                        ax, bottom = self.subview_stacks(ax, x, bottom, source, header, next(facecolors), header, edgecolor, width)
        ## view by headers
        else:
            ## group headers into iterable container
            if sources is not None:
                raise ValueError("input sources OR headers")
            if percents is not None:
                raise ValueError("points from individual headers cannot be converted into percentages (ie, how to define 100%)")
            if differentiate_sources:
                raise ValueError("differentiate_sources can be set to True only when inputting sources")
            if isinstance(headers, str):
                headers = [headers]
            if not isinstance(headers, (tuple, list, np.ndarray)):
                raise ValueError("invalid type(headers): {}".format(type(headers)))
            ## get savename
            if save:
                savename = 'stacked_' + '_'.join(headers)
            else:
                savename = None
            ## get facecolors
            nstacks = len(headers)
            facecolors = iter(self.visual_configuration.select_facecolors(np.arange(nstacks), cmap, default_color=None))
            for header in headers:
                for source in ('homework', 'exam', 'extra credit', 'curve'):
                    condition = (self.points[source]['header'] == header)
                    if np.any(condition):
                        ## get index of corresponding scores
                        loc = np.nonzero(condition)[0]
                        if loc.size > 1:
                            raise ValueError("multiple {}s share the same header: {}".format(source, header))
                        ax, bottom = self.subview_stacks(ax, x, bottom, source, header, next(facecolors), header, edgecolor, width)
        ## configure xticks, xticklabels, and xlabel
        ax.set_xticks(x)
        if identifier_label is None:
            ax.set_xticklabels([], fontsize=self.visual_configuration.ticksize)
            ax.set_xlabel('Students', fontsize=self.visual_configuration.labelsize)
        else:
            if not isinstance(identifier_label, str):
                raise ValueError("invalid type(identifier_label): {}".format(type(identifier_label)))
            if identifier_label not in list(self.identifiers.keys()):
                raise ValueError("invalid identifier_label: {}".format(identifier_label))
            xticklabels = np.char.replace(self.identifiers[identifier_label], ' ', '\n')
            ax.set_xticklabels(xticklabels, fontsize=self.visual_configuration.ticksize, rotation=15)
            if identifier_label == 'id number':
                ax.set_xlabel('Student ID Number'.format(identifier_label), fontsize=self.visual_configuration.labelsize)
            else:
                ax.set_xlabel('Student {}'.format(identifier_label.title()), fontsize=self.visual_configuration.labelsize)
        ## configure y-axis
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        ylim = ax.get_ylim()
        ylim_prime = [0, ylim[-1] * 1.25]
        ax.set_ylim(ylim_prime)
        ax.set_ylabel('Points', fontsize=self.visual_configuration.labelsize)
        ## show percents
        if percents is not None:
            percents = self.visual_configuration.select_percents(percents)
            ploc = percents * self.total_weight / 100
            self.visual_configuration.subview_percents(ax, percents, ploc, mirror_axis='y', limit=ylim_prime)
        ## finalize plot
        ax.tick_params(axis='both', labelsize=self.visual_configuration.ticksize)
        ax.grid(color='k', linestyle=':', alpha=0.3)
        # ax.set_title(title, fontsize=self.visual_configuration.titlesize)
        handles, labels = ax.get_legend_handles_labels()
        self.visual_configuration.subview_legend(fig, handles, labels, self.visual_configuration.get_empty_handle(ax), title='Distribution of Points')
        ## show/save figure
        self.visual_configuration.display_image(fig, savename)

    def view_distribution_boxplots(self, sources, percentiles=(25, 75), showmeans=False, showfliers=False, group_by_points=False, save=False, **kwargs):
        """

        """
        ## group input sources
        if isinstance(sources, str):
            sources = [sources]
        if not isinstance(sources, (tuple, list, np.ndarray)):
            raise ValueError("invalid type(sources): {}".format(type(sources)))
        ## verify percentiles
        if not isinstance(percentiles, (tuple, list, np.ndarray)):
            raise ValueError("invalid type(percentiles): {}".format(type(percentiles)))
        percentiles = np.array([np.min(percentiles), np.max(percentiles)])
        if np.any(percentiles < 0):
            raise ValueError("percentiles cannot be less than 0")
        if np.any(percentiles > 100):
            raise ValueError("percentiles cannot be greater than 100")
        npercs = len(percentiles)
        if npercs != 2:
            raise ValueError("{} percentiles were given but 2 are required".format(npercs))
        ## by source
        for source in sources:
            ## get all assignment headers
            headers = self.points[source]['header']
            ## get statistics
            statistics = self.points[source]['statistics']
            ## get weights
            if source == 'curve':
                if not group_by_points: ## group by percentage of total weight
                    raise ValueError("curved points cannot be converted into percentages (ie, how to define 100%)")
            else:
                weights = self.points[source]['weight']
            ## get coordinates
            x = np.arange(headers.size)
            y = []
            for i, header in enumerate(headers):
                ## get scores
                scores = self.points[source]['score'][:, i]
                ## get percentiles
                qs = np.nanpercentile(scores, q=percentiles)
                ## get outliers
                out_condition = ((scores > qs[-1]) | (scores < qs[0]))
                out_indices = np.nonzero(out_condition)[0]
                nan_condition = np.isnan(scores)
                nan_indices = np.nonzero(nan_condition)[0]
                condition = np.setdiff1d(out_indices, nan_indices)
                outliers = scores[condition]
                if len(outliers) == 0:
                    outliers = [] ## FIX ME! DRAW BOX IF SCORES CONTAINS NAN
                yi = {
                    'med' : statistics['median'][i], ## median
                    'q1' : qs[0], ## first quartile by default
                    'q3' : qs[1], ## third quartile by default
                    'whislo' : statistics['minimum'][i], ## minimum whisker
                    'whishi' : statistics['maximum'][i], ## maximum whisker,
                    'mean' : statistics['mean'][i], ## *optional
                    'fliers' : outliers, ## outliers, *optional
                    'label' : header ## 'xticklabel', *optional
                        }
                if not group_by_points: ## group by percentage of total weight
                    for key, value in yi.items():
                        if key != 'label':
                            yi[key] = value * 100 / weights[i]
                y.append(yi)
            ## initialize plot
            fig, ax = plt.subplots(**kwargs)
            ax.bxp(y, x, showmeans=showmeans, showfliers=showfliers)
            ## axis ticks
            if not group_by_points:
                yticks = np.arange(0, 101, 20).astype(int)
                ax.set_yticks(yticks)
                yticklabels = np.core.defchararray.add(yticks.astype(str), [' %']*yticks.size)
                ax.set_yticklabels(yticklabels, fontsize=self.visual_configuration.ticksize)
            ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
            ax.tick_params(axis='both', labelsize=self.visual_configuration.ticksize)
            ax.grid(color='k', linestyle=':', alpha=0.3)
            ## initialize axis labels
            ax.set_xlabel('Source of Points', fontsize=self.visual_configuration.labelsize)
            if group_by_points:
                ax.set_ylabel('Student Score', fontsize=self.visual_configuration.labelsize)
            else:
                ax.set_ylabel('Percentage of\nStudent Score', fontsize=self.visual_configuration.labelsize)
            title = 'Box-Plot of {} Points'.format(source.title())
            ax.set_title(title, fontsize=self.visual_configuration.titlesize)
            ## show/save figure
            savename = 'boxplot_{}'.format(source.replace(' ', '_')) if save else None
            self.visual_configuration.display_image(fig, savename)

    def view_pie_chart_of_grades_distribution(self, cmap='Oranges', text_color='gray', show_annulus=False, save=False, **kwargs):
        title = 'Pie-Chart of Grade Distribution'
        fig, ax = plt.subplots(**kwargs)
        facecolors = self.visual_configuration.select_facecolors(
            counts=np.arange(self.letters.size, dtype=int),
            cmap=cmap)
        explode = np.zeros(self.letters.size, dtype=float)
        explode[-3:] = 0.1
        counts_per_grade = [self.grade_counter[letter] for letter in self.letters]
        pctdistance = 0.85 if show_annulus else 0.6
        wedgeprops = {
            "edgecolor" : "k",
            'linewidth': 1,
            'linestyle': 'solid',
            'antialiased': True}
        patches, texts, autotexts = ax.pie(
            counts_per_grade,
            colors=facecolors,
            labels=self.letters,
            autopct='%1.1f%%',
            startangle=90,
            # shadow=True,
            explode=explode,
            pctdistance=pctdistance,
            wedgeprops=wedgeprops)
        for text in texts:
            text.set_color(text_color)
        for autotext in autotexts:
            autotext.set_color(text_color)
        if show_annulus:
            circle = plt.Circle(
                (0,0),
                0.70,
                fc=ax.get_facecolor()) # 'white'
            # ax.add_patch(circle)
            fig.gca().add_artist(circle)
            if save:
                savename = 'pie_annular_chart_grade_distribution'
            else:
                savename = None
        else:
            title = 'Annular {}'.format(title)
            if save:
                savename = 'pie_circular_chart_grade_distribution'
            else:
                savename = None
        ax.set_title(title, fontsize=self.visual_configuration.titlesize)
        ax.axis('equal')
        self.visual_configuration.display_image(fig, savename)

    def view_network_graph_of_grades_distribution(self, layout_id, scheme, cmap='jet', save=False, **kwargs):
        if layout_id not in ('bipartite', 'circular'): #, 'arc'):
            raise ValueError("invalid layout_id: {}".format(layout_id))
        cls = NetworkColorConfiguration(
            graph=self.graph,
            letters=self.letters)
        labels, node_color, edge_color = cls.get_color_schematic(
                scheme=scheme,
                cmap=cmap)
        ## initialize plot
        fig, ax = plt.subplots(**kwargs)
        if layout_id == 'bipartite':
            pos = nx.bipartite_layout(
                self.graph,
                [node for node in self.graph.nodes() if isinstance(node, (int, np.int64))],
                align='horizontal')
            nx.draw(
                self.graph,
                pos=pos,
                node_color=node_color,
                edge_color=edge_color,
                labels=labels,
                with_labels=True)
        elif layout_id == 'circular':
            pos=nx.circular_layout(self.graph)
            nx.draw_networkx_labels(
                self.graph,
                pos=pos,
                labels=labels)
            nx.draw(
                self.graph,
                pos=pos,
                node_color=node_color,
                edge_color=edge_color,
                labels=labels,
                with_labels=True)
        # elif layout_id == 'arc':
        #     raise ValueError("not yet implemented")
        else:
            raise ValueError("invalid layout_id: {}".format(layout_id))
        title = 'Network Diagram of Grade Distribution'
        ax.set_title(title, fontsize=self.visual_configuration.titlesize)
        ## show/save figure
        _scheme = scheme.replace(' ', '_').replace('-', '_')
        if '+' in _scheme:
            _scheme = _scheme.replace('+', 'v2')
        else:
            _scheme = '{}_v1'.format(_scheme)
        savename = 'network_diagram_grade_distribution_{}_{}'.format(layout_id, _scheme) if save else None
        self.visual_configuration.display_image(fig, savename)




##
