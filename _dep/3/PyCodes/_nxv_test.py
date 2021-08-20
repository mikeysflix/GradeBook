import numpy as np
import matplotlib.pyplot as plt

from matplotlib import patches

# set the points
x1, y1 = (0., 0.)
x2, y2 = (1., 0.)

# calculate the arc
mxmy = mx, my = [(x1 + x2) / 2, (y1 + y2) / 2]
r = np.sqrt((x1 - mx)**2 + (y1 - my)**2)
width = 2 * r
height = 2 * r
start_angle = np.arctan2(y1 - my, x1 - mx) * 180 / np.pi
end_angle = np.arctan2(my - y2, mx - x2) * 180 / np.pi

# draw
arc = patches.Arc(mxmy, width, height, start_angle, end_angle)

fig, ax = plt.subplots(1,1)
ax.add_patch(arc)
ax.set_xlim(-0.1, 1.1) # you need to set the appropriate limits explicitly!
ax.set_ylim(-0.1, 1.1)
plt.show()
plt.close()

class XYZ():


    def view_bipartite_network_graph(self, design='classic', facecolors=None, cmap=None, save=False, **kwargs):
        fig, ax = plt.subplots()
        labels = dict()
        if facecolors is None:
            node_color = None
            for node in self.graph.nodes():
                if isinstance(node, (int, np.int64)):
                    labels[node] = ""
                else:
                    labels[node] = node
        else:
            if len(facecolors) >= 2:
                node_color = []
                for node in self.graph.nodes():
                    if isinstance(node, (int, np.int64)):
                        node_color.append(facecolors[0])
                        labels[node] = ""
                    else:
                        node_color.append(facecolors[1])
                        labels[node] = node
            else:
                node_color = [facecolors for node in self.graph.nodes()]
                for node in self.graph.nodes():
                    if isinstance(node, (int, np.int64)):
                        labels[node] = ""
                    else:
                        labels[node] = node
        if cmap is None:
            edge_color = None
        else:
            colors_from_cmap = self.visual_configuration.select_facecolors(
                counts=np.arange(self.letters.size, dtype=int),
                cmap=cmap)
            edge_color = []
            for edge in self.graph.edges():
                for i, letter in enumerate(self.letters):
                    if letter in edge:
                        edge_color.append(colors_from_cmap[i])
        if design == 'classic':
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
        elif design == 'circular':
            pos=nx.circular_layout(self.graph)
            nx.draw_networkx_labels(
                self.graph,
                pos=pos)
                # labels=labels)
            nx.draw(
                self.graph,
                pos=pos,
                node_color=node_color,
                edge_color=edge_color,
                labels=labels,
                with_labels=True)
        elif design == 'arc':
            ...
        else:
            raise ValueError("invalid design: {}".format(design))
        ## show/save figure
        savename = 'bipartite_grade_distribution_{}'.format(design) if save else None
        self.visual_configuration.display_image(fig, savename)


    # for color_nodes in (True, False):
    #     for color_edges in (True, False):
    #         for facecolors in (None, ['red', 'blue']):
    #             for cmap in (None, 'jet'):
    #                 print("\n .. COLOR NODES:\n\t{}".format(color_nodes))
    #                 print("\n .. COLOR EDGES:\n\t{}".format(color_edges))
    #                 print("\n .. FACECOLORS:\n\t{}".format(facecolors))
    #                 print("\n .. CMAP:\n\t{}".format(cmap))
    #                 backend.view_bipartite_network_graph(
    #                     facecolors=facecolors,
    #                     cmap=cmap,
    #                     color_nodes=color_nodes,
    #                     color_edges=color_edges)


    # backend.view_bipartite_network_graph(
    #     facecolors=('red', 'blue'))
    # backend.view_bipartite_network_graph(
    #     cmap='jet')
    # backend.view_bipartite_network_graph(
    #     facecolors=('red', 'blue'),
    #     cmap='plasma')
    # backend.view_bipartite_network_graph(
    #     facecolors=('red', 'blue'))
    # backend.view_bipartite_network_graph(
    #     design='circular',
    #     facecolors=('red', 'blue'))
    # backend.view_bipartite_network_graph(
    #     cmap='viridis')
    # backend.view_bipartite_network_graph(
    #     cmap='viridis',
    #     facecolors=('red', 'blue'))
