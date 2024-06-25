import networkx as nx
from networkx import Graph

from database.DAO import DAO


class Model:
    def __init__(self):
        self.genes = DAO.get_all_genes()
        self.genes_map = {g.GeneID: g for g in self.genes}
        self.graph = None

    def build_graph(self):
        self.graph = nx.Graph()
        nodes = DAO.get_all_nodes(self.genes_map)
        self.graph.add_nodes_from(nodes)
        edges = DAO.get_all_edges(self.genes_map)
        for e in edges:
            self.graph.add_edge(e[0], e[1])
        pesi = DAO.get_all_pesi(self.genes_map)
        for p in pesi:
            self.graph[p[0]][p[1]]['weight'] = p[2]

    def get_graph_details(self):
        return len(self.graph.nodes), len(self.graph.edges)

    def get_sorted_neighbors(self, chosen_gene):
        sorted_neighbors = [(n, self.graph[chosen_gene][n]["weight"]) for n in self.graph.neighbors(chosen_gene)]
        sorted_neighbors.sort(key=lambda t: t[1], reverse=True)
        return sorted_neighbors
