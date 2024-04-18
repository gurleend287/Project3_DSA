from node import Node
from sklearn.metrics.pairwise import cosine_similarity

class Graph:
    def __init__(self, threshold_map):
        self.adjacency_list = {}
        self.threshold_map = threshold_map
    
    # helper function
    # returns similarity score used to determine if two nodes should be connected
    def find_similarity(node1: Node, node2: Node):
        features1 = [node1.danceability, node1.energy, node1.valence, node1.tempo]
        features2 = [node2.danceability, node2.energy, node2.valence, node2.tempo]
        
        # reshape
        features1 = [features1]
        features2 = [features2]
        
        return cosine_similarity(features1, features2)[0][0]
    
    # def add_node(self, node: Node, cols: list[str]):
        