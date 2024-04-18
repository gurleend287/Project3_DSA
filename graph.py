from node import Node
from sklearn.metrics.pairwise import cosine_similarity

class Graph:
    def __init__(self, threshold_map):
        self.adj_list = {}
        self.threshold_map = threshold_map
    
    # helper function
    # returns similarity score used to determine if two nodes should be connected
    def find_similarity(self, node1: Node, node2: Node):
        features1 = [node1.danceability, node1.energy, node1.valence, node1.tempo]
        features2 = [node2.danceability, node2.energy, node2.valence, node2.tempo]
        
        # reshape
        features1 = [features1]
        features2 = [features2]
        
        return cosine_similarity(features1, features2)[0][0]
    
    # add edge between nodes if similarity score theshold is met
    # similary score is weight of edge
    def add_edge(self, node1: Node, node2: Node):
        sim_score = self.find_similarity(node1, node2)
        # print(sim_score)
        # getting high similarity scores for most nodes
        # 0.9999995 is good threshold for sparse graph - obtained through trial and error
        if sim_score >= 0.9999995:
            key1 = (node1.track_id, node1)
            key2 = (node2.track_id, node2)
            self.adj_list[key1].append((key2, sim_score))
            self.adj_list[key2].append((key1, sim_score))
    
    # add node to graph based on mood theshold criteria and connect edges
    def add_node(self, node: Node, cols: list[str]):
        for col in cols:
            if getattr(node, col) < self.threshold_map[col][0] or getattr(node, col) > self.threshold_map[col][1]:
                return # node not added
        
        key = (node.track_id, node)
        if node.track_id not in self.adj_list:
            self.adj_list[key] = []