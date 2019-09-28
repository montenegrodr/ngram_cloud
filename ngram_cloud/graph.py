# source: https://www.bogotobogo.com/python/python_graph_data_structures.php
import io
import matplotlib
import networkx as nx
import matplotlib.pyplot as plt

matplotlib.use('agg')


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    @staticmethod
    def from_associations(associations):
        g = Graph()
        for a in associations:
            g.add_edge(
                frm=a.word1,
                to=a.word2,
                cost=a.occurrences
            )
        return g

    def to_json(self):
        j = {}
        for vertex in self:
            word = vertex.get_id().word
            j[word] = dict(
                (k.id.word, w) for (k, w) in
                self.vert_dict[vertex.get_id()].adjacent.items()
            )
        return j

    def to_img_bytes(self):
        img = io.BytesIO()
        G = nx.Graph()
        for word, neighbors in self.to_json().items():
            for neighbor, weight in neighbors.items():
                G.add_edge(word, neighbor, weight=weight)

        edges = [(u, v) for (u, v, d) in G.edges(data=True)]
        pos = nx.spring_layout(G)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='#00b4d9')

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=1, alpha=0.5)

        # labels
        nx.draw_networkx_labels(G, pos, font_size=7, font_family='sans-serif')

        plt.axis('off')
        plt.savefig(img, format='png', dpi=300)
        plt.close()
        img.seek(0)
        return img
