import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import Normalize

class VisualConfiguration():

    def __init__(self, ticksize=7, labelsize=8, textsize=5, titlesize=9, headersize=10, bias='left'):
        """

        """
        super().__init__()
        self._savedir = None
        self.ticksize = ticksize
        self.labelsize = labelsize
        self.textsize = textsize
        self.titlesize = titlesize
        self.headersize = headersize
        self.empty_label = '  '

    @property
    def savedir(self):
        return self._savedir

    @staticmethod
    def select_facecolors(counts, cmap=None, default_color='darkorange'):
        """

        """
        if cmap is None:
            return [default_color]*counts.size
        elif isinstance(cmap, (tuple, list, np.ndarray)):
            nc = len(cmap)
            if nc != counts.size:
                raise ValueError("{} colors for {} bins".format(nc, counts.size))
            return list(cmap)
        else:
            norm = Normalize(vmin=np.min(counts), vmax=np.max(counts))
            f = plt.get_cmap(cmap)
            return f(norm(counts))

    @staticmethod
    def get_number_of_legend_columns(labels):
        """

        """
        if isinstance(labels, int):
            n = labels
        else:
            n = len(labels)
        if n > 2:
            if n % 3 == 0:
                ncol = 3
            else:
                ncol = n // 2
        else:
            ncol = n
        return ncol

    @staticmethod
    def get_empty_handle(ax):
        """

        """
        empty_handle = ax.scatter([np.nan], [np.nan], color='none', alpha=0)
        return empty_handle

    @staticmethod
    def select_percents(percents):
        """

        """
        if isinstance(percents, (int, float)):
            percents = np.array([percents])
        elif isinstance(percents, (tuple, list)):
            percents = np.array(percents)
        elif not isinstance(percents, np.ndarray):
            raise ValueError("invalid type(percents): {}".format(type(percents)))
        if np.any(percents < 0):
            raise ValueError("percents must be non-negative")
        if np.any(percents > 100):
            raise ValueError("percents cannot exceed 100")
        return percents

    @staticmethod
    def get_histogram_edges_from_weight(wt):
        """

        """
        if wt <= 5:
            edges = np.linspace(0, wt, wt*2 +1)
        elif 5 < wt <= 10:
            edges = np.arange(0, wt+1, 1).astype(int)
        elif 10 < wt <= 20:
            edges = np.arange(0, wt+5, 5).astype(int)
        else:
            if (wt % 5 == 0):
                edges = np.arange(0, wt+5, 5).astype(int)
            else:
                edges = np.arange(0, wt+10, 10).astype(int)
        return edges

    def update_save_directory(self, savedir):
        self._savedir = savedir

    def update_legend_design(self, leg, title=None, textcolor=None, facecolor=None, edgecolor=None, borderaxespad=None):
        """

        """
        if title:
            leg.set_title(title, prop={'size': self.labelsize, 'weight' : 'semibold'})
            if textcolor:
                leg.get_title().set_color(textcolor)
            # leg.get_title().set_ha("center")
        leg._legend_box.align = "center"
        frame = leg.get_frame()
        if facecolor:
            frame.set_facecolor(facecolor)
        if edgecolor:
            frame.set_edgecolor(edgecolor)
        if textcolor:
            for text in leg.get_texts():
                text.set_color(textcolor)
        return leg

    def subview_legend(self, fig, handles, labels, empty_handle=None, title=''):
        """

        """
        if len(labels) == 1:
            ncol = 3
            handles = [empty_handle, handles[0], empty_handle]
            labels = [self.empty_label, labels[0], self.empty_label]
        else:
            ncol = self.get_number_of_legend_columns(labels)
        fig.subplots_adjust(bottom=0.2)
        leg = fig.legend(handles=handles, labels=labels, ncol=ncol, loc='lower center', mode='expand', borderaxespad=0.1, fontsize=self.labelsize)
        leg = self.update_legend_design(leg, title=title, textcolor='darkorange', facecolor='k', edgecolor='steelblue')

    def subview_statistics(self, fig, ax, statistics, loc=None, decimals=2):
        """

        """
        handles, labels = [], []
        empty_handle = self.get_empty_handle(ax)
        for key, value in statistics.items():
            if key == 'mode':
                ...
            else:
                if loc is None:
                    label = r'{}: ${:.2f}$'.format(key, np.round(value, decimals=decimals))
                else:
                    label = r'{}: ${:.2f}$'.format(key, np.round(value[loc], decimals=decimals))
                labels.append(label)
                handles.append(empty_handle)
        self.subview_legend(fig, handles, labels, empty_handle, title='Statistics')

    def subview_percents(self, ax, percents, ploc, mirror_axis, limit=None):
        """

        """
        ## apply percent labels
        plabels = np.core.defchararray.add(percents.astype(str), [' %']*percents.size)
        if mirror_axis == 'x':
            if limit is None:
                xlim = ax.get_xlim()
            else:
                xlim = limit
            ax_xmirror = ax.twiny()
            ax_xmirror.set_xlim(xlim)
            ax_xmirror.set_xticks(ploc)
            ax_xmirror.set_xticklabels(plabels, fontsize=self.ticksize)
            ax_xmirror.tick_params(axis="x", direction="in", pad=-15)
            ylim = ax.get_ylim()
            ax.set_ylim([0, ylim[-1] * 1.125])
        else:
            if limit is None:
                ylim = ax.get_ylim()
            else:
                ylim = limit
            ax_ymirror = ax.twinx()
            ax_ymirror.set_ylim(ylim)
            ax_ymirror.set_yticks(ploc)
            ax_ymirror.set_yticklabels(plabels, fontsize=self.ticksize)
            ax_ymirror.tick_params(axis="y", direction="out", pad=15)

    def subview_histogram(self, edges, counts, cmap, default_color, title, **kwargs):
        """

        """
        ## get bin parameters
        midpoints = (edges[1:] + edges[:-1])/2
        width = np.diff(edges)
        facecolors = self.select_facecolors(counts, cmap, default_color)
        ## get y-axis parameters
        yticks = np.arange(0, np.max(counts)+2).astype(int)
        ylim = [0, yticks[-1]]
        ## initialize plot
        fig, ax = plt.subplots(**kwargs)
        handle = ax.bar(midpoints, counts, width=width, color=facecolors)
        ## initialize axis ticks
        ax.set_xticks(edges)
        ax.set_yticks(yticks[::2])
        ax.set_yticks(yticks[1::2], minor=True)
        ax.set_ylim(ylim)
        ax.tick_params(axis='both', labelsize=self.ticksize)
        ax.grid(color='k', linestyle=':', alpha=0.3)
        ## initialize axis labels
        ax.set_xlabel('Student Score', fontsize=self.labelsize)
        ax.set_ylabel('Number of Students', fontsize=self.labelsize)
        ax.set_title(title, fontsize=self.titlesize)
        return fig, ax, midpoints, facecolors

    def display_image(self, fig, savename=None, dpi=800, bbox_inches='tight', pad_inches=0.1, extension='.png', **kwargs):
        """

        """
        if savename is None:
            plt.show()
        elif isinstance(savename, str):
            if self.savedir is None:
                raise ValueError("cannot save plot; self.savedir is None")
            savepath = '{}{}{}'.format(self.savedir, savename, extension)
            fig.savefig(savepath, dpi=dpi, bbox_inches=bbox_inches, pad_inches=pad_inches, **kwargs)
        else:
            raise ValueError("invalid type(savename): {}".format(type(savename)))
        plt.close(fig)

class NetworkColorConfiguration(VisualConfiguration):

    def __init__(self, graph, letters):
        super().__init__()
        self.graph = graph
        self.letters = letters
        ## vi --> set of grades (F through A+), vj --> set of students

    def get_single_color_by_single_color_vertices(self, vi_facecolor, vj_facecolor):
        labels = dict()
        node_color = []
        for node in self.graph.nodes():
            if isinstance(node, (int, np.int64)): ## set of unique students
                node_color.append(vj_facecolor)
                labels[node] = ""
            else:
                node_color.append(vi_facecolor)
                labels[node] = node
        return labels, node_color

    def get_multi_color_by_single_color_vertices(self, vi_cmap, vj_facecolor):
        labels = dict()
        node_color = []
        colors_from_cmap = self.select_facecolors(
            counts=np.arange(self.letters.size, dtype=int),
            cmap=vi_cmap)
        grade_to_color = dict(zip(self.letters, colors_from_cmap))
        for node in self.graph.nodes():
            if isinstance(node, (int, np.int64)): ## set of unique students
                node_color.append(vj_facecolor)
                labels[node] = ""
                d = dict(self.graph[node])
                keys = list(d.keys())
                grade = keys[0]
                color_from_grade = grade_to_color[grade]
            else: ## set of unique grades
                labels[node] = node
                color_from_grade = grade_to_color[node]
                node_color.append(color_from_grade)
        return labels, node_color

    def get_matching_multiple_color_vertices(self, cmap):
        labels = dict()
        node_color = []
        colors_from_cmap = self.select_facecolors(
            counts=np.arange(self.letters.size, dtype=int),
            cmap=cmap)
        grade_to_color = dict(zip(self.letters, colors_from_cmap))
        for node in self.graph.nodes():
            if isinstance(node, (int, np.int64)): ## set of unique students
                labels[node] = ""
                d = dict(self.graph[node])
                keys = list(d.keys())
                grade = keys[0]
                color_from_grade = grade_to_color[grade]
            else: ## set of unique grades
                labels[node] = node
                color_from_grade = grade_to_color[node]
            node_color.append(color_from_grade)
        return labels, node_color

    def get_edge_colors(self, cmap=None, facecolor=None):
        if facecolor is None:
            facecolor = 'k'
        edge_color = []
        colors_from_cmap = self.select_facecolors(
            counts=np.arange(self.letters.size, dtype=int),
            cmap=cmap,
            default_color=facecolor)
        for edge in self.graph.edges():
            for i, letter in enumerate(self.letters):
                if letter in edge:
                    edge_color.append(colors_from_cmap[i])
        return edge_color

    def get_color_schematic(self, scheme, cmap='jet'):
        if scheme in ('plain', 'plain +'):
            labels, node_color = self.get_single_color_by_single_color_vertices(
                vi_facecolor='darkorange',
                vj_facecolor='steelblue')
            if scheme == 'plain':
                edge_color = self.get_edge_colors(
                    facecolor='silver')
            else:
                edge_color = self.get_edge_colors(
                    cmap=cmap)
        elif scheme in ('classic', 'classic +'):
            labels, node_color = self.get_multi_color_by_single_color_vertices(
                vi_cmap=cmap,
                vj_facecolor='silver')
            if scheme == 'classic':
                edge_color = self.get_edge_colors(
                    facecolor='k')
            else:
                edge_color = self.get_edge_colors(
                    cmap=cmap)
        elif scheme in ('color-matching', 'color-matching +'):
            labels, node_color = self.get_matching_multiple_color_vertices(
                cmap=cmap)
            if scheme == 'color-matching':
                edge_color = self.get_edge_colors(
                    facecolor='gray')
            else:
                edge_color = self.get_edge_colors(
                    cmap=cmap)
        else:
            raise ValueError("invalid scheme: {}".format(scheme))
        return labels, node_color, edge_color
##
