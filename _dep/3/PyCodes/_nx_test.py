import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import nxviz as nxv



letters = (
    'A+',
    'A',
    'A-',
    'B+',
    'B',
    'B-',
    'C+',
    'C',
    'C-',
    'D+',
    'D',
    'D-',
    'F')

np.random.seed(0)
n = 50 ## number of students
indices = np.arange(50, dtype=int) # index of student
grades = np.random.choice(letters, size=n)

G = nx.Graph()
G.add_nodes_from(letters, group_id=0)
for i, grade in enumerate(grades):
    G.add_node(i, group_id=1)
    edge = (i, grade)
    G.add_edge(*edge)


# for edge in G.edges():
#     print(edge)

for node in G.nodes():
    print(node)


fig, ax = plt.subplots()
node_color = None
# pos = nx.bipartite_layout(G, [node for node in G.nodes() if isinstance(node, int)])
pos = nx.bipartite_layout(G, [node for node in G.nodes() if isinstance(node, int)], align='horizontal')
nx.draw(G, pos=pos, node_color=node_color) # with_labels=True,
plt.show()
plt.close(fig)

fig, ax = plt.subplots()
c = nxv.CircosPlot(G)
c.draw()
plt.show()
plt.close(fig)

# fig, ax = plt.subplots()
# a = nxv.ArcPlot(G, node_color='group_id', node_grouping='group_id')
# a.draw()
# # nxv.arc(G, node_color_by="group_id", group_by="group_id")
# # nxv.annotate.arc_group(G, group_by="group_id")
# # nxv.circos(G, group_by="group_id", node_color_by="group_id")
# # nxv.annotate.circos_group(G, group_by="group_id")
# plt.show()
# plt.close(fig)
#






##


class Old():


    def view_network_graph(self, facecolors=None, cmap=None, save=False, **kwargs):
        fig, ax = plt.subplots()
        if facecolors is None:
            node_color = None
        else:
            if len(facecolors) >= 2:
                ...





    def view_network_graph(self, design=None, facecolors=None, cmap=None, save=False, **kwargs):
        """

        """
        if facecolors is None:
            node_color = None
        else:

            ## vertex colors

            if len(facecolors) >= 2:
                # x = nx.get_node_attributes(self.graph, 'graph_id')





                node_color = []
                for node in self.graph.nodes:
                    print("\n .. NODE ({}):\n{}\n".format(type(node), node))
                    print("\n .. GRAPH @ NODE ({}):\n{}\n".format(type(self.graph[node]), self.graph[node]))
                    print("-"*10)
                    if isinstance(self.graph[node], (int, np.int64)):
                        node_color.append(facecolors[0])
                    else:
                        node_color.append(facecolors[1])
            else:
                node_color = [facecolors for node in self.graph.nodes]
        fig, ax = plt.subplots(**kwargs)
        nx.draw(self.graph, with_labels=True, node_color=node_color) # node_color=['green','green','green','green','blue','blue','blue']
        # nx.draw_circular(self.graph) # node_color=['green','green','green','green','blue','blue','blue']
        plt.show()
        plt.close(fig)
